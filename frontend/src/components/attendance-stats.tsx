import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Clock, Users } from "lucide-react"

interface AttendanceStatsProps {
  data: any[]
  className?: string
}

export function AttendanceStats({ data, className = "" }: AttendanceStatsProps) {
  // Calculate unique users
  const uniqueUsers = new Set(data.map((record) => record.userName)).size

  // Calculate average duration
  const totalDuration = data.reduce((sum, record) => sum + record.durationMinutes, 0)
  const averageDuration = data.length > 0 ? Math.round(totalDuration / data.length) : 0

  return (
    <div className={`grid gap-4 md:grid-cols-2 ${className}`}>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Уникальных пользователей</CardTitle>
          <Users className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{uniqueUsers}</div>
          <p className="text-xs text-muted-foreground">Общее количество разных людей</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Средняя длительность</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{averageDuration} мин</div>
          <p className="text-xs text-muted-foreground">Среднее время пребывания</p>
        </CardContent>
      </Card>
    </div>
  )
}
