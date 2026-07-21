import React, { useState } from 'react';
import { isLowStock } from '../helpers';

const AdjustControl = ({ m, onAdjust }) => {
  const [amt, setAmt] = useState(10);
  const n = Math.max(1, Number(amt) || 1);
  return (
    <div className='flex items-center gap-1'>
      <button
        type='button'
        onClick={() => onAdjust(m, -Math.min(n, m.stock))}
        disabled={m.stock <= 0}
        className='w-7 h-7 rounded bg-red-100 text-red-700 font-bold leading-none disabled:opacity-40'
      >
        −
      </button>
      <input
        type='number'
        min={1}
        value={amt}
        onChange={(e) => setAmt(e.target.value)}
        className='w-14 border border-slate-300 rounded px-1 py-1 text-sm text-center focus:outline-none focus:ring-2 focus:ring-brand-500'
      />
      <button
        type='button'
        onClick={() => onAdjust(m, n)}
        className='w-7 h-7 rounded bg-green-100 text-green-700 font-bold leading-none'
      >
        +
      </button>
    </div>
  );
};

const MedicineStockTable = ({ medicines = [], onAdjust }) => {
  if (!medicines.length)
    return <p className='text-slate-500 text-sm py-4'>Belum ada obat</p>;

  return (
    <>
      {/* HP: kartu */}
      <ul className='space-y-2 md:hidden'>
        {medicines.map((m) => {
          const low = isLowStock(m);
          return (
            <li
              key={m.id}
              className={`border rounded-lg p-3 ${low ? 'border-red-200 bg-red-50' : 'border-slate-200'}`}
            >
              <div className='flex justify-between items-start'>
                <div className='min-w-0'>
                  <div className='font-medium text-slate-800 truncate'>
                    {m.name}
                  </div>
                  <div className='text-xs text-slate-500'>
                    {m.code} · min {m.min_stock}
                  </div>
                </div>
                <div className='text-right shrink-0'>
                  <div className='font-semibold text-slate-800'>
                    {m.stock} {m.unit}
                  </div>
                  {low ? (
                    <span className='text-red-600 text-xs font-medium'>
                      ⚠ Menipis
                    </span>
                  ) : (
                    <span className='text-green-600 text-xs'>Aman</span>
                  )}
                </div>
              </div>
              {onAdjust && (
                <div className='mt-2'>
                  <AdjustControl m={m} onAdjust={onAdjust} />
                </div>
              )}
            </li>
          );
        })}
      </ul>

      {/* Tablet & desktop: tabel */}
      <div className='hidden md:block overflow-x-auto'>
        <table className='w-full text-sm min-w-[620px]'>
          <thead className='text-left text-slate-500 border-b border-slate-200'>
            <tr>
              <th className='py-2'>Kode</th>
              <th>Nama</th>
              <th>Stok</th>
              <th>Min</th>
              <th>Status</th>
              {onAdjust && <th className='text-right'>Sesuaikan</th>}
            </tr>
          </thead>
          <tbody>
            {medicines.map((m) => {
              const low = isLowStock(m);
              return (
                <tr
                  key={m.id}
                  className={`border-b border-slate-100 ${low ? 'bg-red-50/50' : ''}`}
                >
                  <td className='py-2 text-slate-600'>{m.code}</td>
                  <td className='text-slate-800'>{m.name}</td>
                  <td className='text-slate-700 font-medium'>
                    {m.stock} {m.unit}
                  </td>
                  <td className='text-slate-600'>{m.min_stock}</td>
                  <td>
                    {low ? (
                      <span className='text-red-600 font-medium'>
                        ⚠ Menipis
                      </span>
                    ) : (
                      <span className='text-green-600'>Aman</span>
                    )}
                  </td>
                  {onAdjust && (
                    <td>
                      <div className='flex justify-end'>
                        <AdjustControl m={m} onAdjust={onAdjust} />
                      </div>
                    </td>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </>
  );
};

export default MedicineStockTable;
