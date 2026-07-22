import React from 'react';
import StatusBadge from './StatusBadge';
import { nextStatuses, visitStatusLabel } from '../helpers';

const QueueCard = ({ visit, onAdvance }) => {
  const nexts = nextStatuses(visit.status);
  return (
    <div className='border border-slate-200 rounded-lg p-3 flex flex-col sm:flex-row sm:items-center gap-3'>
      <div className='flex items-center gap-3 flex-1 min-w-0'>
        <div className='text-2xl font-bold w-12 text-center text-brand-600 shrink-0'>
          #{visit.queue_no}
        </div>
        <div className='min-w-0'>
          <div className='font-medium text-slate-800 truncate'>
            {visit.employee_name}
          </div>
          <div className='text-slate-500 text-sm truncate'>
            {visit.complaint}
          </div>
        </div>
      </div>
      <div className='flex items-center justify-between sm:justify-end gap-2 flex-wrap'>
        <StatusBadge status={visit.status} />
        <div className='flex gap-1 flex-wrap'>
          {nexts.map((s) => (
            <button
              key={s}
              onClick={() => onAdvance?.(visit, s)}
              className='px-2 py-1 text-xs rounded bg-slate-100 text-slate-700 hover:bg-slate-200 whitespace-nowrap'
            >
              → {visitStatusLabel(s)}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default QueueCard;
