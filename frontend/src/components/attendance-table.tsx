"use client"

import { useState } from "react"
import { ArrowDown, ArrowUp, ArrowUpDown } from "lucide-react"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

type AttendanceRecord = {
  id: string
  userName: string
  entryTime: string
  exitTime: string
  durationMinutes: number
}

type SortField = "userName" | "entryTime" | "exitTime" | "durationMinutes"
type SortDirection = "asc" | "desc"

interface AttendanceTableProps {
  data: AttendanceRecord[]
}

export function AttendanceTable({ data }: AttendanceTableProps) {
  const [sortField, setSortField] = useState<SortField>("entryTime")
  const [sortDirection, setSortDirection] = useState<SortDirection>("desc")

  const handleSort = (field: SortField) => {
    if (field === sortField) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc")
    } else {
      setSortField(field)
      setSortDirection("asc")
    }
  }

  const getSortIcon = (field: SortField) => {
    if (field !== sortField) return <ArrowUpDown className="ml-2 h-4 w-4" />
    return sortDirection === "asc" ? <ArrowUp className="ml-2 h-4 w-4" /> : <ArrowDown className="ml-2 h-4 w-4" />
  }

  const sortedData = [...data].sort((a, b) => {
    if (sortField === "userName") {
      return sortDirection === "asc" ? a.userName.localeCompare(b.userName) : b.userName.localeCompare(a.userName)
    } else if (sortField === "durationMinutes") {
      return sortDirection === "asc" ? a.durationMinutes - b.durationMinutes : b.durationMinutes - a.durationMinutes
    } else {
      // For dates
      const dateA = new Date(a[sortField]).getTime()
      const dateB = new Date(b[sortField]).getTime()
      return sortDirection === "asc" ? dateA - dateB : dateB - dateA
    }
  })

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="cursor-pointer" onClick={() => handleSort("userName")}>
              <div className="flex items-center">
                Имя пользователя
                {getSortIcon("userName")}
              </div>
            </TableHead>
            <TableHead className="cursor-pointer" onClick={() => handleSort("entryTime")}>
              <div className="flex items-center">
                Время входа
                {getSortIcon("entryTime")}
              </div>
            </TableHead>
            <TableHead className="cursor-pointer" onClick={() => handleSort("exitTime")}>
              <div className="flex items-center">
                Время выхода
                {getSortIcon("exitTime")}
              </div>
            </TableHead>
            <TableHead className="cursor-pointer text-right" onClick={() => handleSort("durationMinutes")}>
              <div className="flex items-center justify-end">
                Длительность (мин)
                {getSortIcon("durationMinutes")}
              </div>
            </TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {sortedData.map((record, index) => (
            <TableRow key={record.id || index} className={index % 2 === 0 ? "bg-muted/50" : ""}>
              <TableCell className="font-medium">{record.userName}</TableCell>
              <TableCell>{record.entryTime}</TableCell>
              <TableCell>{record.exitTime}</TableCell>
              <TableCell className="text-right">{record.durationMinutes}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
