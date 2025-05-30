"use client"
import { Input } from "@/components/ui/input"

interface TimeRangePickerProps {
  startTime: string
  endTime: string
  onStartTimeChange: (time: string) => void
  onEndTimeChange: (time: string) => void
}

export function TimeRangePicker({ startTime, endTime, onStartTimeChange, onEndTimeChange }: TimeRangePickerProps) {
  return (
    <div className="grid grid-cols-2 gap-2">
      <div>
        <Input type="time" value={startTime} onChange={(e) => onStartTimeChange(e.target.value)} placeholder="С" />
      </div>
      <div>
        <Input type="time" value={endTime} onChange={(e) => onEndTimeChange(e.target.value)} placeholder="По" />
      </div>
    </div>
  )
}
