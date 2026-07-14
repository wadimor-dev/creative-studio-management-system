import React, { useState, useEffect } from 'react';

const Timer = ({ startTime }) => {
  const [elapsed, setElapsed] = useState('');

  useEffect(() => {
    if (!startTime) return;
    const interval = setInterval(() => {
      const now = new Date();
      const start = new Date(startTime);
      const diff = Math.floor((now - start) / 1000);
      const h = Math.floor(diff / 3600).toString().padStart(2, '0');
      const m = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
      const s = (diff % 60).toString().padStart(2, '0');
      if (h > 0) setElapsed(`${h}:${m}:${s}`);
      else setElapsed(`${m}:${s}`);
    }, 1000);
    return () => clearInterval(interval);
  }, [startTime]);

  return <span>{elapsed || '00:00'}</span>;
};

const CurrentStudioActivity = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="rounded-xl border border-gray-100 bg-white p-8 text-center dark:border-gray-800 dark:bg-gray-900 shadow-sm">
        <p className="text-sm text-gray-500 dark:text-gray-400">Tidak ada yang sedang bekerja saat ini.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {data.map((act) => (
        <div key={act.id} className="flex flex-col rounded-xl border border-gray-100 bg-white p-4 dark:border-gray-800 dark:bg-gray-900 shadow-sm hover:shadow-md transition-shadow">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span className="font-semibold text-gray-900 dark:text-white">{act.user}</span>
            </div>
            <span className="text-xs font-medium px-2 py-1 bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400 rounded-md">
              WORKING
            </span>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-300 font-medium">{act.activity}</div>
          <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{act.category}</div>
          <div className="mt-4 pt-3 border-t border-gray-50 dark:border-gray-800 flex items-center gap-2 text-sm text-gray-700 dark:text-gray-200 font-mono bg-gray-50 dark:bg-gray-800/50 p-2 rounded-lg justify-center">
            <Timer startTime={act.start_time} />
          </div>
        </div>
      ))}
    </div>
  );
};

export default CurrentStudioActivity;
