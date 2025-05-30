# VisitLog Backend

## О проекте

VisitLog — это система для мониторинга посещений аудиторий и анализа активности пользователей. Этот бэкенд-модуль реализован на FastAPI с использованием асинхронной SQLAlchemy.

## API эндпоинты

### 1. GET `/api/attendance`
**Назначение:** Получение данных о посещениях с возможностью фильтрации.

**Параметры запроса:**
- `date` (YYYY-MM-DD, обязат.)
- `time_start`, `time_end` (HH:mm)
- `name` (search by name or ID)
- `min_duration_min`, `max_duration_min`
- `sort_by`: `userName`, `entryTime`, `exitTime`, `durationMinutes`
- `sort_order`: `asc`, `desc`
- `page`, `limit`

**Формат ответа:**
```json
{
  "data": [
    {
      "id": "string",
      "userName": "string",
      "entryTime": "ISO 8601",
      "exitTime": "ISO 8601",
      "durationMinutes": 0
    }
  ],
  "meta": {
    "totalRecords": 0,
    "totalPages": 0,
    "currentPage": 1,
    "uniqueUsers": 0,
    "averageDuration": 0
  }
}
```

**Коды ответа:** 200, 400, 401, 500

---

### 2. GET `/api/attendance/export`
**Назначение:** Экспорт данных в CSV, Excel или PDF

**Дополнительно:**
- `format` (csv, excel, pdf)
- Другие параметры как в `/api/attendance`

**Ответ:** файл в Content-Type соотв. формату

**Коды ответа:** 200, 400, 401, 500

---

### 3. GET `/api/attendance/stats`
**Назначение:** Агрегированная статистика по посещениям

**Параметры:**
- `date` (обязат.)
- `time_start`, `time_end`

**Формат ответа:**
```json
{
  "uniqueUsers": 0,
  "totalVisits": 0,
  "averageDuration": 0,
  "peakHour": {"hour": "HH:mm", "count": 0},
  "hourlyDistribution": [{"hour": "HH:mm", "count": 0}]
}
```

**Коды ответа:** 200, 400, 401, 500

---

### 4. GET `/api/users`
**Назначение:** Список пользователей для автозаполнения

**Параметры:**
- `query` (необяз.)
- `limit` (по умолч.: 20)

**Формат ответа:**
```json
{
  "data": [
    {"id": "string", "userName": "string"}
  ]
}
```

**Коды ответа:** 200, 401, 500

---

## Авторизация

Для доступа к защищённым ресурсам API требуется JWT-токен.

**Пример:**
```
Authorization: Bearer <token>
```

---

## Технологии
- Python 3.12+
- FastAPI
- SQLAlchemy 2.x (async)
- Pydantic 2
- PostgreSQL
- Docker + Poetry

---

## Авторы
- Проект разработан [Lobashik](https://github.com/Lobashik)