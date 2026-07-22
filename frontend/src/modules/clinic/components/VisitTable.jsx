import React from 'react';
import StatusBadge from './StatusBadge';
import { formatDateTime } from '../helpers';

const VisitTable = ({
  visits = [],
  onRowClick,
  emptyText = 'Belum ada kunjungan',
}) => {
  if (!visits.length)
    return <p className='text-slate-500 text-sm py-4'>{emptyText}</p>;

  return (
    <>
      {/* HP: kartu */}
      <ul className='space-y-2 md:hidden'>
        {visits.map((v) => (
          <li
            key={v.id}
            onClick={() => onRowClick?.(v)}
            className='border border-slate-200 rounded-lg p-3 active:bg-slate-50 cursor-pointer'
          >
            <div className='flex justify-between items-start gap-2'>
              <div className='min-w-0'>
                <div className='font-medium text-slate-800'>
                  {v.visit_no} · #{v.queue_no}
                </div>
                <div className='text-sm text-slate-700'>{v.employee_name}</div>
                <div className='text-sm text-slate-500 truncate'>
                  {v.complaint}
                </div>
              </div>
              <StatusBadge status={v.status} />
            </div>
            <div className='text-xs text-slate-400 mt-1'>
              {formatDateTime(v.created_at)}
            </div>
          </li>
        ))}
      </ul>

      {/* Tablet & desktop: tabel */}
      <div className='hidden md:block overflow-x-auto'>
        <table className='w-full text-sm min-w-[600px]'>
          <thead className='text-left text-slate-500 border-b border-slate-200'>
            <tr>
              <th className='py-2'>No</th>
              <th>Antrian</th>
              <th>Karyawan</th>
              <th>Keluhan</th>
              <th>Status</th>
              <th>Waktu</th>
            </tr>
          </thead>
          <tbody>
            {visits.map((v) => (
              <tr
                key={v.id}
                onClick={() => onRowClick?.(v)}
                className='border-b border-slate-100 hover:bg-slate-50 cursor-pointer'
              >
                <td className='py-2 text-slate-700'>{v.visit_no}</td>
                <td className='text-slate-700'>#{v.queue_no}</td>
                <td className='text-slate-700'>{v.employee_name}</td>
                <td className='max-w-[200px] truncate text-slate-600'>
                  {v.complaint}
                </td>
                <td>
                  <StatusBadge status={v.status} />
                </td>
                <td className='text-slate-500'>
                  {formatDateTime(v.created_at)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default VisitTable;
