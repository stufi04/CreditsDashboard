import { useRef } from 'react'

import { AgGridReact } from 'ag-grid-react'
import type { ColDef, GridApi, SortModelItem } from 'ag-grid-community'
import { ModuleRegistry, AllCommunityModule } from 'ag-grid-community'

import { useSearchParams } from 'react-router-dom'
import dayjs from 'dayjs'

import type { Message } from '../model/Message'

ModuleRegistry.registerModules([ AllCommunityModule ]);

type DashboardTableProps = {
    rowData: Message[]
  }

export function DashboardTable({ rowData }: DashboardTableProps) {
  const [searchParams, setSearchParams] = useSearchParams()

  const gridApi = useRef<GridApi | null>(null);

  // When grid is ready, apply sort from URL if exists
  const onGridReady = (params: any) => {
    gridApi.current = params.api

    const sortParams = searchParams.get('sort')
    if (sortParams) {
      const model: SortModelItem[] = sortParams.split(',').map(entry => {
        const [colId, sort] = entry.split(':')
        return { colId, sort: sort as 'asc' | 'desc' }
      })
      params.api.applyColumnState({ state: model, applyOrder: false });
    }
  }

  // On sort change, update URL with new sort
  const onSortChanged = () => {
    if (!gridApi.current) return
    const model = gridApi.current.getState().sort?.sortModel as SortModelItem[]
    console.log(model)
    if (model && model.length) {
      const sortParam = model.map(({ colId, sort }) => `${colId}:${sort}`).join(',')
      setSearchParams(prev => {
        const next = new URLSearchParams(prev)
        next.set('sort', sortParam)
        return next
      })
    } else {
      setSearchParams(prev => {
        const next = new URLSearchParams(prev)
        next.delete('sort')
        return next
      })
    }
  }

  const columns: ColDef[] = [
    { 
      field: 'message_id',
      headerName: 'Message ID',
      sortable: false,
      width: 120 
    },
    { 
      field: 'timestamp', 
      headerName: 'Timestamp', 
      sortable: false,
      valueFormatter: (params) => dayjs(params.value).format('DD-MM-YYYY HH:mm'),
      width: 200,
    },
    { 
      field: 'report_name', 
      headerName: 'Report Name', 
      sortable: true,
      valueGetter: params => params.data.report_name || '',
      width: 300,
    },
    { 
      field: 'credits_used', 
      headerName: 'Credits Used', 
      sortable: true,
      valueFormatter: params => params.value.toFixed(2),
      width: 200,
    },
  ]

  return (
    <div className="ag-theme-alpine" style={{ width: '100%', height: '100%' }}>
      <AgGridReact
        rowData={rowData}
        columnDefs={columns}
        onGridReady={onGridReady}
        onSortChanged={onSortChanged}
        getRowId={params => params.data.message_id}
        multiSortKey="ctrl"
        defaultColDef={{ sortable: true }}
      />
    </div>
  )
}