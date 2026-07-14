import React from 'react';
import { Users, Package, CheckCircle, Clock } from 'lucide-react';

const StudioStatus = ({ data }) => {
  return (
    <div className="rounded-xl bg-gradient-to-r from-gray-900 to-gray-800 p-6 shadow-lg text-white">
      <h2 className="text-lg font-semibold mb-4 text-gray-100">Studio Hari Ini</h2>
      <div className="flex flex-wrap gap-6 sm:gap-10">
        
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400">
            <Users size={20} />
          </div>
          <div>
            <div className="text-2xl font-bold">{data.working || 0}</div>
            <div className="text-sm text-gray-400">Orang Sedang Bekerja</div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-amber-500/20 text-amber-400">
            <Package size={20} />
          </div>
          <div>
            <div className="text-2xl font-bold">{data.assets_out || 0}</div>
            <div className="text-sm text-gray-400">Asset Dipakai</div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-500/20 text-blue-400">
            <CheckCircle size={20} />
          </div>
          <div>
            <div className="text-2xl font-bold">{data.completed || 0}</div>
            <div className="text-sm text-gray-400">Aktivitas Selesai</div>
          </div>
        </div>

      </div>
    </div>
  );
};

export default StudioStatus;
