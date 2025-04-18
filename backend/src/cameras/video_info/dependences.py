# deps/attendance_filters.py
from fastapi import Query, Depends
from typing import Optional
from datetime import date, time


class AttendanceFilterParams:
    def __init__(
        self,
        date: date = Query(..., description="Дата (обязательная)"),
        time_start: Optional[time] = Query(None),
        time_end: Optional[time] = Query(None),
        name: Optional[str] = Query(None),
        min_duration_min: Optional[int] = Query(None),
        max_duration_min: Optional[int] = Query(None),
        sort_by: Optional[str] = Query("entry_time"),
        sort_order: Optional[str] = Query("asc"),
        page: int = Query(1),
        limit: int = Query(50),
    ):
        self.date = date
        self.time_start = time_start
        self.time_end = time_end
        self.name = name
        self.min_duration_min = min_duration_min
        self.max_duration_min = max_duration_min
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.page = page
        self.limit = limit
