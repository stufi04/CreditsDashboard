import { useState, useEffect } from 'react'
import { CreditsBarChart } from './CreditsBarChart'
import { DashboardTable } from './DashboardTable'

import type { Message } from '../model/Message' 

export function CreditsDashboard() {
  const [data, setData] = useState<Message[]>([])

  useEffect(() => {
    fetch('http://127.0.0.1:5000/usage')
      .then(res => res.json())
      .then(setData)
      .catch(console.error)
  }, [])

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        justifyContent: 'flex-start',
        width: '100%',         
        maxWidth: 900,          
        margin: '0 auto',     
        gap: 20,
      }}
    >
      <h3>Credits Usage Dashboard</h3>
      <div style={{ width: '100%' }}>
        <CreditsBarChart data={data} />
      </div>
      <div style={{ width: '100%', height: 600 }}>
        <DashboardTable rowData={data} />
      </div>
    </div>
  )
}