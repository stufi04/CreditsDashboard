import React from 'react'
import dayjs from 'dayjs'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import type { Message } from '../model/Message'

interface CreditsBarChartProps {
  data: Message[]
}

export function CreditsBarChart({ data }: CreditsBarChartProps) {

  const aggregatedCreditsByDate = React.useMemo(() => {
    if (!data.length) return []
    const map = new Map<string, number>()

    data.forEach(({ timestamp, credits_used }) => {
      const date = dayjs(timestamp).format('YYYY-MM-DD')
      map.set(date, (map.get(date) || 0) + credits_used)
    })

    const sortedDates = Array.from(map.keys()).sort()

    return sortedDates.map(date => ({
      date,
      credits: map.get(date) || 0,
    }))
  }, [data])

  return (
    <div style={{ width: '100%', height: 200, marginBottom: 20 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={aggregatedCreditsByDate}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip 
            formatter={(value: number) => value.toFixed(2)} 
           />
          <Bar dataKey="credits" fill="#1976d2" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}