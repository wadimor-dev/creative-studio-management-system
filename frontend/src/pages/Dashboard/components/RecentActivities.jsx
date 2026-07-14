import React, { useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';

const RecentActivities = ({ data = [] }) => {
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 3;
  
  const totalPages = Math.ceil(data.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const paginatedData = data.slice(startIndex, endIndex);

  const handlePrev = () => {
    if (currentPage > 1) setCurrentPage(currentPage - 1);
  };

  const handleNext = () => {
    if (currentPage < totalPages) setCurrentPage(currentPage + 1);
  };

  return (
    <div className="h-full flex flex-col rounded-xl border border-gray-100 bg-white p-4 sm:p-6 dark:border-gray-800 dark:bg-gray-900 shadow-sm">
      <div className="mb-4 sm:mb-6 flex items-center justify-between">
        <div>
          <h3 className="text-base sm:text-lg font-semibold text-gray-900 dark:text-white">Recent Activities</h3>
          <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400">Latest completed or active tasks.</p>
        </div>
      </div>
      
      <div className="flex-1 overflow-x-auto">
        <table className="w-full text-left text-sm text-gray-600 dark:text-gray-400 min-w-[600px]">
          <thead className="border-b border-gray-100 bg-gray-50/50 text-xs font-medium uppercase text-gray-500 dark:border-gray-800 dark:bg-gray-800/50 dark:text-gray-400">
            <tr>
              <th className="px-4 py-3">User</th>
              <th className="px-4 py-3">Activity</th>
              <th className="px-4 py-3">Category</th>
              <th className="px-4 py-3">Started</th>
              <th className="px-4 py-3">Finished</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-800">
            {paginatedData.length === 0 ? (
              <tr>
                <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                  Belum ada aktivitas.
                </td>
              </tr>
            ) : (
              paginatedData.map((row) => (
                <tr key={row.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-gray-900 dark:text-white">{row.user}</td>
                  <td className="px-4 py-3">{row.activity}</td>
                  <td className="px-4 py-3">{row.category}</td>
                  <td className="px-4 py-3">
                    {row.started ? new Date(row.started).toLocaleString('id-ID', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '-'}
                  </td>
                  <td className="px-4 py-3">
                    {row.finished ? new Date(row.finished).toLocaleString('id-ID', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '-'}
                  </td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center rounded-full px-2 py-1 text-xs font-medium ${
                      row.status === 'COMPLETED' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' :
                      row.status === 'WORKING' ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400' :
                      'bg-gray-50 text-gray-700 dark:bg-gray-800 dark:text-gray-400'
                    }`}>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Controls */}
      {totalPages > 1 && (
        <div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-4 dark:border-gray-800">
          <span className="text-sm text-gray-500 dark:text-gray-400">
            Showing <span className="font-medium text-gray-900 dark:text-white">{startIndex + 1}</span> to <span className="font-medium text-gray-900 dark:text-white">{Math.min(endIndex, data.length)}</span> of <span className="font-medium text-gray-900 dark:text-white">{data.length}</span> results
          </span>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePrev}
              disabled={currentPage === 1}
              className="inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white p-1.5 text-gray-500 hover:bg-gray-50 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-brand-500/50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300"
              aria-label="Previous page"
            >
              <ChevronLeft size={18} />
            </button>
            <div className="text-sm font-medium text-gray-600 dark:text-gray-300">
              {currentPage} / {totalPages}
            </div>
            <button
              onClick={handleNext}
              disabled={currentPage === totalPages}
              className="inline-flex items-center justify-center rounded-lg border border-gray-200 bg-white p-1.5 text-gray-500 hover:bg-gray-50 hover:text-gray-700 focus:outline-none focus:ring-2 focus:ring-brand-500/50 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-gray-300"
              aria-label="Next page"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RecentActivities;
