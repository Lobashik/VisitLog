### Документация фронтенда системы мониторинга посещений аудитории

## 1. Обзор проекта

### 1.1 Назначение

Фронтенд-приложение предназначено для административного мониторинга посещений аудитории на основе данных распознавания лиц. Система позволяет просматривать, фильтровать и экспортировать данные о присутствии людей в аудитории.

### 1.2 Технический стек

- **Фреймворк**: Next.js (App Router)
- **Язык программирования**: TypeScript
- **Стилизация**: Tailwind CSS
- **UI-компоненты**: shadcn/ui
- **Работа с датами**: date-fns
- **Иконки**: lucide-react


### 1.3 Архитектура приложения

Приложение построено на основе компонентной архитектуры React с использованием Next.js App Router. Основные слои приложения:

- **Компоненты UI**: Переиспользуемые компоненты интерфейса
- **Страницы**: Компоненты-страницы, соответствующие маршрутам приложения
- **Сервисы**: Модули для работы с API и бизнес-логики
- **Утилиты**: Вспомогательные функции и константы


## 2. Структура проекта

```plaintext
src/
├── app/
│   ├── api/
│   │   └── attendance/
│   │       └── route.ts       # API-маршрут для моковых данных (в реальном проекте заменяется на внешний API)
│   ├── layout.tsx             # Корневой layout приложения
│   └── page.tsx               # Главная страница с интерфейсом мониторинга
├── components/
│   ├── attendance-stats.tsx   # Компонент статистики посещений
│   ├── attendance-table.tsx   # Компонент таблицы посещений с сортировкой
│   ├── time-range-picker.tsx  # Компонент выбора временного диапазона
│   └── ui/                    # Базовые UI-компоненты из shadcn/ui
├── services/
│   ├── api.ts                 # Сервис для работы с API
│   └── auth.ts                # Сервис для аутентификации (опционально)
├── lib/
│   └── utils.ts               # Утилиты и вспомогательные функции
└── types/
    └── index.ts               # TypeScript типы и интерфейсы
```

## 3. Компоненты

### 3.1 Основные компоненты

#### AttendanceMonitoring (`app/page.tsx`)

Главный компонент приложения, который объединяет все остальные компоненты и управляет состоянием приложения.

**Ответственность**:

- Управление состоянием фильтров и данных
- Выполнение API-запросов
- Обработка экспорта данных
- Отображение UI-компонентов


**Состояние**:

- `date`: Выбранная дата (обязательный параметр)
- `searchQuery`: Строка поиска по имени/ID пользователя
- `minDuration`, `maxDuration`: Фильтры по длительности пребывания
- `timeStart`, `timeEnd`: Фильтры по временному интервалу
- `isLoading`: Флаг загрузки данных
- `attendanceData`: Массив данных о посещениях
- `error`: Сообщение об ошибке (если есть)


**Методы**:

- `handleSearch()`: Выполняет запрос к API с текущими параметрами фильтрации
- `handleExport()`: Экспортирует данные в CSV-формат
- `handleReset()`: Сбрасывает все фильтры


#### AttendanceTable (`components/attendance-table.tsx`)

Компонент для отображения таблицы посещений с возможностью сортировки.

**Пропсы**:

- `data`: Массив данных о посещениях


**Состояние**:

- `sortField`: Поле, по которому выполняется сортировка
- `sortDirection`: Направление сортировки (asc/desc)


**Методы**:

- `handleSort()`: Изменяет поле сортировки или направление
- `getSortIcon()`: Возвращает иконку для заголовка столбца в зависимости от состояния сортировки


#### AttendanceStats (`components/attendance-stats.tsx`)

Компонент для отображения статистики посещений.

**Пропсы**:

- `data`: Массив данных о посещениях
- `className`: Дополнительные CSS-классы


**Вычисляемые значения**:

- `uniqueUsers`: Количество уникальных пользователей
- `averageDuration`: Средняя длительность пребывания


#### TimeRangePicker (`components/time-range-picker.tsx`)

Компонент для выбора временного интервала.

**Пропсы**:

- `startTime`: Начальное время
- `endTime`: Конечное время
- `onStartTimeChange`: Функция обратного вызова при изменении начального времени
- `onEndTimeChange`: Функция обратного вызова при изменении конечного времени


### 3.2 UI-компоненты

Приложение использует компоненты из библиотеки shadcn/ui:

- `Button`: Кнопки различных стилей
- `Card`, `CardHeader`, `CardContent`, `CardFooter`: Компоненты карточек
- `Input`: Поля ввода
- `Label`: Метки для полей ввода
- `Popover`: Всплывающие окна
- `Calendar`: Календарь для выбора даты
- `Table`: Компоненты таблицы


## 4. Интеграция с API

### 4.1 Сервис API (`services/api.ts`)

Модуль для работы с API бэкенда.

**Основные функции**:

```typescript
// Получение данных о посещениях
export async function fetchAttendanceData(params: {
  date: string;
  time_start?: string;
  time_end?: string;
  name?: string;
  min_duration_min?: string;
  max_duration_min?: string;
}) {
  // Формирование параметров запроса и выполнение запроса к API
}

// Экспорт данных
export async function exportAttendanceData(params: {
  date: string;
  time_start?: string;
  time_end?: string;
  name?: string;
  min_duration_min?: string;
  max_duration_min?: string;
  format: 'csv' | 'excel' | 'pdf';
}) {
  // Запрос на экспорт данных
}

// Получение статистики
export async function fetchAttendanceStats(params: {
  date: string;
  time_start?: string;
  time_end?: string;
}) {
  // Запрос на получение статистики
}
```

### 4.2 Формат данных

#### Запрос данных о посещениях

**Параметры запроса**:

- `date` (обязательный, формат: YYYY-MM-DD)
- `time_start` (необязательный, формат: HH:mm)
- `time_end` (необязательный, формат: HH:mm)
- `name` (необязательный)
- `min_duration_min` (необязательный)
- `max_duration_min` (необязательный)


**Формат ответа**:

```json
{
  "data": [
    {
      "id": "string",
      "userName": "string",
      "entryTime": "string (ISO 8601)",
      "exitTime": "string (ISO 8601)",
      "durationMinutes": "number"
    }
  ],
  "meta": {
    "totalRecords": "number",
    "totalPages": "number",
    "currentPage": "number"
  }
}
```

## 5. Функциональность

### 5.1 Фильтрация данных

Приложение поддерживает следующие фильтры:

- **Дата**: Обязательный параметр, выбирается через календарь
- **Временной интервал**: Фильтрация по времени входа/выхода
- **Поиск по имени/ID**: Текстовый поиск по имени или ID пользователя
- **Длительность пребывания**: Фильтрация по минимальной и максимальной длительности


### 5.2 Сортировка

Таблица посещений поддерживает сортировку по следующим полям:

- Имя пользователя
- Время входа
- Время выхода
- Длительность пребывания


### 5.3 Экспорт данных

Приложение поддерживает экспорт данных в формате CSV. При нажатии на кнопку "Экспорт в CSV" генерируется файл с текущими отфильтрованными данными.

### 5.4 Статистика

Отображается статистика по текущим отфильтрованным данным:

- Количество уникальных пользователей
- Средняя длительность пребывания


## 6. Установка и запуск

### 6.1 Требования

- Node.js 18.x или выше
- npm 8.x или выше


### 6.2 Установка зависимостей

```shellscript
# Создание нового проекта Next.js
npx create-next-app@latest attendance-monitoring
cd attendance-monitoring

# Установка дополнительных зависимостей
npm install date-fns lucide-react

# Инициализация shadcn/ui
npx shadcn@latest init

# Установка компонентов
npx shadcn@latest add button card input label popover table calendar
```

### 6.3 Настройка переменных окружения

Создайте файл `.env.local` в корне проекта:

```plaintext
NEXT_PUBLIC_API_URL=https://your-api-url.com
```

### 6.4 Запуск в режиме разработки

```shellscript
npm run dev
```

### 6.5 Сборка для production

```shellscript
npm run build
npm start
```

## 7. Руководство по разработке

### 7.1 Добавление новых компонентов

1. Создайте новый файл в директории `components/`
2. Импортируйте необходимые зависимости
3. Определите интерфейс пропсов с использованием TypeScript
4. Реализуйте компонент
5. Экспортируйте компонент


Пример:

```typescriptreact
import { useState } from "react"
import { Button } from "@/components/ui/button"

interface MyComponentProps {
  title: string;
  onAction: () => void;
}

export function MyComponent({ title, onAction }: MyComponentProps) {
  const [isActive, setIsActive] = useState(false)
  
  return (
    <div className="p-4 border rounded">
      <h2 className="text-lg font-bold">{title}</h2>
      <Button 
        onClick={() => {
          setIsActive(!isActive)
          onAction()
        }}
      >
        {isActive ? "Активно" : "Неактивно"}
      </Button>
    </div>
  )
}
```

### 7.2 Интеграция с новыми API-эндпоинтами

1. Добавьте новую функцию в `services/api.ts`
2. Используйте функцию в компонентах


Пример:

```typescriptreact
// В services/api.ts
export async function fetchUserDetails(userId: string) {
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}`)
  if (!response.ok) {
    throw new Error(`Failed to fetch user details: ${response.status}`)
  }
  return response.json()
}

// В компоненте
import { fetchUserDetails } from "@/services/api"

// В функции компонента
const handleUserClick = async (userId: string) => {
  try {
    const userDetails = await fetchUserDetails(userId)
    setSelectedUser(userDetails)
  } catch (error) {
    console.error("Error fetching user details:", error)
  }
}
```

### 7.3 Стилизация компонентов

Приложение использует Tailwind CSS для стилизации. Основные принципы:

1. Используйте утилитарные классы Tailwind для стилизации
2. Для сложных компонентов используйте композицию классов с помощью функции `cn` из `lib/utils.ts`
3. Для условных стилей используйте тернарные операторы или функцию `cn`


Пример:

```typescriptreact
import { cn } from "@/lib/utils"

function StatusBadge({ status }: { status: "active" | "inactive" | "pending" }) {
  return (
    <span
      className={cn(
        "px-2 py-1 rounded-full text-xs font-medium",
        status === "active" && "bg-green-100 text-green-800",
        status === "inactive" && "bg-red-100 text-red-800",
        status === "pending" && "bg-yellow-100 text-yellow-800"
      )}
    >
      {status}
    </span>
  )
}
```

## 8. Расширение функциональности

### 8.1 Добавление аутентификации

Для добавления аутентификации рекомендуется использовать NextAuth.js:

1. Установите NextAuth.js:


```shellscript
npm install next-auth
```

2. Создайте файл `src/app/api/auth/[...nextauth]/route.ts` для настройки провайдеров аутентификации
3. Добавьте провайдер сессии в корневой layout
4. Используйте хук `useSession` для доступа к данным пользователя


### 8.2 Добавление пагинации

Для больших наборов данных рекомендуется добавить пагинацию:

1. Добавьте параметры `page` и `limit` в запросы API
2. Создайте компонент пагинации
3. Интегрируйте компонент в таблицу посещений


### 8.3 Добавление визуализации данных

Для визуализации статистики можно использовать библиотеки графиков:

1. Установите библиотеку (например, Chart.js или Recharts):


```shellscript
npm install recharts
```

2. Создайте компоненты для различных типов графиков
3. Интегрируйте графики в интерфейс


## 9. Решение проблем

### 9.1 Проблемы с API

**Симптом**: Данные не загружаются, в консоли ошибки CORS или 401/403.

**Решение**:

1. Проверьте URL API в переменных окружения
2. Убедитесь, что токен аутентификации передается корректно
3. Проверьте, что бэкенд разрешает CORS для вашего домена


### 9.2 Проблемы с рендерингом

**Симптом**: Компоненты не отображаются или отображаются некорректно.

**Решение**:

1. Проверьте консоль на наличие ошибок JavaScript
2. Убедитесь, что данные имеют ожидаемый формат
3. Используйте React DevTools для проверки пропсов и состояния компонентов


### 9.3 Проблемы с производительностью

**Симптом**: Интерфейс работает медленно, особенно при большом количестве данных.

**Решение**:

1. Добавьте пагинацию для больших наборов данных
2. Используйте мемоизацию для предотвращения лишних рендеров:


```typescriptreact
import { useMemo } from "react"

// В компоненте
const sortedData = useMemo(() => {
  return [...data].sort((a, b) => {
    // Логика сортировки
  })
}, [data, sortField, sortDirection])
```

3. Оптимизируйте рендеринг списков с помощью виртуализации (например, react-window)


## 10. Глоссарий

- **App Router**: Система маршрутизации в Next.js, основанная на файловой системе
- **shadcn/ui**: Библиотека UI-компонентов для React, основанная на Radix UI и Tailwind CSS
- **Tailwind CSS**: Утилитарный CSS-фреймворк
- **TypeScript**: Типизированный суперсет JavaScript
- **JWT**: JSON Web Token, стандарт для создания токенов доступа


## 11. Приложения

### 11.1 Типы данных

```typescript
// src/types/index.ts

export interface AttendanceRecord {
  id: string;
  userName: string;
  entryTime: string;
  exitTime: string;
  durationMinutes: number;
}

export interface AttendanceResponse {
  data: AttendanceRecord[];
  meta: {
    totalRecords: number;
    totalPages: number;
    currentPage: number;
    uniqueUsers: number;
    averageDuration: number;
  };
}

export interface AttendanceStats {
  uniqueUsers: number;
  totalVisits: number;
  averageDuration: number;
  peakHour: {
    hour: string;
    count: number;
  };
  hourlyDistribution: Array<{
    hour: string;
    count: number;
  }>;
}

export type SortField = "userName" | "entryTime" | "exitTime" | "durationMinutes";
export type SortDirection = "asc" | "desc";
```

### 11.2 Примеры API-запросов

#### Получение данных о посещениях

```typescript
// Пример запроса
const params = new URLSearchParams({
  date: "2023-05-15",
  time_start: "09:00",
  time_end: "18:00",
  name: "Иванов",
  min_duration_min: "30",
  max_duration_min: "120"
});

fetch(`${API_BASE_URL}/api/attendance?${params.toString()}`, {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error("Error:", error));
```

#### Экспорт данных

```typescript
// Пример запроса на экспорт
const params = new URLSearchParams({
  date: "2023-05-15",
  format: "csv"
});

fetch(`${API_BASE_URL}/api/attendance/export?${params.toString()}`, {
  headers: {
    "Authorization": `Bearer ${token}`
  }
})
.then(response => response.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "attendance_2023-05-15.csv";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
})
.catch(error => console.error("Error:", error));
```