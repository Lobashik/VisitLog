# routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import extract, select, func, and_, or_, asc, desc
from cameras.video_info.models import Attendance
from cameras.video_info.schemas import AttendanceListResponse, AttendanceItem, AttendanceMeta, AttendanceStatsResponse, HourlyDistribution, PeakHour
from cameras.video_info.dependences import AttendanceFilterParams
from cameras.database import get_async_session


router = APIRouter()


@router.get("/api/attendance", response_model=AttendanceListResponse)
async def get_attendance(
    filters: AttendanceFilterParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Attendance).where(Attendance.date == filters.date)

        if filters.time_start:
            query = query.where(Attendance.entry_time >= filters.time_start)
        if filters.time_end:
            query = query.where(Attendance.exit_time <= filters.time_end)
        if filters.name:
            name_filter = f"%{filters.name}%"
            query = query.where(
                or_(
                    Attendance.user_name.ilike(name_filter),
                    Attendance.user_id.ilike(name_filter),
                )
            )
        if filters.min_duration_min:
            query = query.where(Attendance.duration_minutes >= filters.min_duration_min)
        if filters.max_duration_min:
            query = query.where(Attendance.duration_minutes <= filters.max_duration_min)

        sort_column = getattr(Attendance, filters.sort_by, Attendance.entry_time)
        sort_order = asc if filters.sort_order == "asc" else desc
        query = query.order_by(sort_order(sort_column))

        total_query = select(func.count()).select_from(query.subquery())
        total_result = await session.execute(total_query)
        total_records = total_result.scalar()

        offset = (filters.page - 1) * filters.limit
        query = query.offset(offset).limit(filters.limit)
        result = await session.execute(query)
        records = result.scalars().all()

        # Метаданные
        unique_users_query = (
            select(func.count(func.distinct(Attendance.user_id)))
            .where(Attendance.date == filters.date)
        )
        avg_duration_query = (
            select(func.avg(Attendance.duration_minutes))
            .where(Attendance.date == filters.date)
        )
        unique_users = (await session.execute(unique_users_query)).scalar() or 0
        average_duration = (await session.execute(avg_duration_query)).scalar() or 0.0

        return AttendanceListResponse(
            data=[
                AttendanceItem(
                    id=record.id,
                    userName=record.user_name,
                    entryTime=record.entry_time.isoformat(),
                    exitTime=record.exit_time.isoformat(),
                    durationMinutes=record.duration_minutes,
                )
                for record in records
            ],
            meta=AttendanceMeta(
                totalRecords=total_records,
                totalPages=(total_records + filters.limit - 1) // filters.limit,
                currentPage=filters.page,
                uniqueUsers=unique_users,
                averageDuration=round(average_duration, 2),
            ),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


# routers/attendance.py (добавим в этот же файл или вынеси в отдельный)
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@router.get("/api/attendance/export")
async def export_attendance(
    filters: AttendanceFilterParams = Depends(),
    format: str = Query(..., regex="^(csv|excel|pdf)$"),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        query = select(Attendance).where(Attendance.date == filters.date)

        if filters.time_start:
            query = query.where(Attendance.entry_time >= filters.time_start)
        if filters.time_end:
            query = query.where(Attendance.exit_time <= filters.time_end)
        if filters.name:
            name_filter = f"%{filters.name}%"
            query = query.where(
                or_(
                    Attendance.user_name.ilike(name_filter),
                    Attendance.user_id.ilike(name_filter),
                )
            )
        if filters.min_duration_min:
            query = query.where(Attendance.duration_minutes >= filters.min_duration_min)
        if filters.max_duration_min:
            query = query.where(Attendance.duration_minutes <= filters.max_duration_min)

        result = await session.execute(query)
        records = result.scalars().all()

        data = [
            {
                "ID": record.id,
                "User Name": record.user_name,
                "Entry Time": record.entry_time.isoformat(),
                "Exit Time": record.exit_time.isoformat(),
                "Duration (min)": record.duration_minutes,
            }
            for record in records
        ]

        df = pd.DataFrame(data)

        if format == "csv":
            buffer = StringIO()
            df.to_csv(buffer, index=False)
            buffer.seek(0)
            return StreamingResponse(
                buffer,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=attendance.csv"},
            )

        elif format == "excel":
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="Attendance")
            buffer.seek(0)
            return StreamingResponse(
                buffer,
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": "attachment; filename=attendance.xlsx"},
            )

        elif format == "pdf":
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter

            x = 40
            y = height - 40
            c.setFont("Helvetica", 10)

            for row in data:
                line = f"{row['User Name']} | {row['Entry Time']} - {row['Exit Time']} | {row['Duration (min)']} min"
                c.drawString(x, y, line)
                y -= 15
                if y < 40:
                    c.showPage()
                    y = height - 40

            c.save()
            buffer.seek(0)

            return StreamingResponse(
                buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=attendance.pdf"},
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")


router = APIRouter()


@router.get("/api/attendance/stats", response_model=AttendanceStatsResponse)
async def get_attendance_stats(
    filters: AttendanceFilterParams = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Основной запрос для фильтрации по дате и времени
        query = select(Attendance).where(Attendance.date == filters.date)

        if filters.time_start:
            query = query.where(Attendance.entry_time >= filters.time_start)
        if filters.time_end:
            query = query.where(Attendance.exit_time <= filters.time_end)

        # Подсчитываем уникальных пользователей
        unique_users_query = select(func.count(func.distinct(Attendance.user_id))).where(Attendance.date == filters.date)
        unique_users = (await session.execute(unique_users_query)).scalar() or 0

        # Подсчитываем общее количество посещений
        total_visits_query = select(func.count()).where(Attendance.date == filters.date)
        total_visits = (await session.execute(total_visits_query)).scalar() or 0

        # Средняя продолжительность посещений
        avg_duration_query = select(func.avg(Attendance.duration_minutes)).where(Attendance.date == filters.date)
        average_duration = (await session.execute(avg_duration_query)).scalar() or 0.0

        # Определяем пик по времени (час с наибольшим количеством посещений)
        peak_hour_query = (
            select(
                extract('hour', Attendance.entry_time).label('hour'),
                func.count().label('count')
            )
            .where(Attendance.date == filters.date)
            .group_by(extract('hour', Attendance.entry_time))
            .order_by(func.count().desc())
            .limit(1)
        )
        peak_hour_result = await session.execute(peak_hour_query)
        peak_hour_row = peak_hour_result.fetchone()
        peak_hour = PeakHour(hour=str(peak_hour_row.hour).zfill(2) + ":00", count=peak_hour_row.count) if peak_hour_row else None

        # Распределение по часам
        hourly_distribution_query = (
            select(
                extract('hour', Attendance.entry_time).label('hour'),
                func.count().label('count')
            )
            .where(Attendance.date == filters.date)
            .group_by(extract('hour', Attendance.entry_time))
            .order_by(extract('hour', Attendance.entry_time))
        )
        hourly_distribution_result = await session.execute(hourly_distribution_query)
        hourly_distribution = [
            HourlyDistribution(hour=str(row.hour).zfill(2) + ":00", count=row.count)
            for row in hourly_distribution_result.fetchall()
        ]

        return AttendanceStatsResponse(
            uniqueUsers=unique_users,
            totalVisits=total_visits,
            averageDuration=round(average_duration, 2),
            peakHour=peak_hour,
            hourlyDistribution=hourly_distribution,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
