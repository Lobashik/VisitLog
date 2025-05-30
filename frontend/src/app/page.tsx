"use client";

import { useEffect, useState } from "react";
import { format } from "date-fns";
import { CalendarIcon, Download, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { AttendanceTable } from "@/components/attendance-table";
import { AttendanceStats } from "@/components/attendance-stats";
import { TimeRangePicker } from "@/components/time-range-picker";
import { exportAttendanceData, fetchAttendanceData } from "@/services/api";

export default function AttendanceMonitoring() {
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [searchQuery, setSearchQuery] = useState("");
  const [minDuration, setMinDuration] = useState("");
  const [maxDuration, setMaxDuration] = useState("");
  const [timeStart, setTimeStart] = useState("");
  const [timeEnd, setTimeEnd] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [attendanceData, setAttendanceData] = useState<any[]>([]);

  const handleSearch = async () => {
    if (!date) return;

    setIsLoading(true);

    try {
      const formattedDate = format(date, "yyyy-MM-dd");

      const data = await fetchAttendanceData({
        date: formattedDate,
        time_start: timeStart,
        time_end: timeEnd,
        name: searchQuery,
        min_duration_min: minDuration,
        max_duration_min: maxDuration,
      });

      setAttendanceData(data.data || data);
    } catch (error) {
      console.error("Error fetching attendance data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExport = async () => {
    if (!date || attendanceData.length === 0) return;

    try {
      setIsLoading(true);
      const formattedDate = format(date, "yyyy-MM-dd");

      const blob = await exportAttendanceData({
        date: formattedDate,
        time_start: timeStart,
        time_end: timeEnd,
        name: searchQuery,
        min_duration_min: minDuration,
        max_duration_min: maxDuration,
        format: "csv",
      });

      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `attendance_${formattedDate}.csv`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error exporting data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (date) {
      handleSearch();
    }
  }, [date]);

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">
        Мониторинг посещений аудитории
      </h1>

      <Card className="mb-8">
        <CardHeader>
          <CardTitle>Параметры поиска</CardTitle>
          <CardDescription>
            Выберите дату и установите фильтры для просмотра данных о посещениях
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <div className="space-y-2">
              <Label htmlFor="date">Дата (обязательно)</Label>
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    id="date"
                    variant="outline"
                    className={cn(
                      "w-full justify-start text-left font-normal",
                      !date && "text-muted-foreground"
                    )}
                  >
                    <CalendarIcon className="mr-2 h-4 w-4" />
                    {date ? format(date, "PPP") : "Выберите дату"}
                  </Button>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0">
                  <Calendar
                    mode="single"
                    selected={date}
                    onSelect={setDate}
                    initialFocus
                  />
                </PopoverContent>
              </Popover>
            </div>

            <div className="space-y-2">
              <Label>Временной интервал</Label>
              <TimeRangePicker
                startTime={timeStart}
                endTime={timeEnd}
                onStartTimeChange={setTimeStart}
                onEndTimeChange={setTimeEnd}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="search">Поиск по имени или ID</Label>
              <div className="flex">
                <Input
                  id="search"
                  placeholder="Введите имя или ID"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full"
                />
                <Button variant="ghost" className="px-3">
                  <Search className="h-4 w-4" />
                  <span className="sr-only">Поиск</span>
                </Button>
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="min-duration">Мин. длительность (мин)</Label>
              <Input
                id="min-duration"
                type="number"
                placeholder="Минимум"
                value={minDuration}
                onChange={(e) => setMinDuration(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="max-duration">Макс. длительность (мин)</Label>
              <Input
                id="max-duration"
                type="number"
                placeholder="Максимум"
                value={maxDuration}
                onChange={(e) => setMaxDuration(e.target.value)}
              />
            </div>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between">
          <Button
            variant="outline"
            onClick={() => {
              setSearchQuery("");
              setMinDuration("");
              setMaxDuration("");
              setTimeStart("");
              setTimeEnd("");
            }}
          >
            Сбросить
          </Button>
          <Button onClick={handleSearch} disabled={!date || isLoading}>
            {isLoading ? "Загрузка..." : "Применить фильтры"}
          </Button>
        </CardFooter>
      </Card>

      {attendanceData.length > 0 && (
        <>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Результаты</h2>
            <Button
              variant="outline"
              onClick={handleExport}
              className="flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              Экспорт в CSV
            </Button>
          </div>

          <AttendanceStats data={attendanceData} className="mb-6" />

          <AttendanceTable data={attendanceData} />
        </>
      )}

      {attendanceData.length === 0 && !isLoading && date && (
        <div className="text-center py-12 text-muted-foreground">
          <p>Нет данных для выбранных параметров</p>
        </div>
      )}
    </div>
  );
}
