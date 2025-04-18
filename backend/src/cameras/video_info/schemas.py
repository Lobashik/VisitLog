# schemas/attendance.py
from pydantic import BaseModel
from datetime import time
from typing import List


class AttendanceItem(BaseModel):
    id: int
    userName: str
    entryTime: str  # ISO 8601
    exitTime: str   # ISO 8601
    durationMinutes: int

    class Config:
        from_attributes = True


class AttendanceMeta(BaseModel):
    totalRecords: int
    totalPages: int
    currentPage: int
    uniqueUsers: int
    averageDuration: float


class AttendanceListResponse(BaseModel):
    data: List[AttendanceItem]
    meta: AttendanceMeta


# schemas/attendance_stats.py
from pydantic import BaseModel
from typing import List


class HourlyDistribution(BaseModel):
    hour: str  # Формат: HH:mm
    count: int


class PeakHour(BaseModel):
    hour: str  # Формат: HH:mm
    count: int


class AttendanceStatsResponse(BaseModel):
    uniqueUsers: int
    totalVisits: int
    averageDuration: float
    peakHour: PeakHour
    hourlyDistribution: List[HourlyDistribution]
