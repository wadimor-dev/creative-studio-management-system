import React from 'react';
import LoadingSpinner from './LoadingSpinner';
import EmptyState from './EmptyState';
const DataTable = ({
  columns,
  data,
  isLoading = false,
  emptyStateTitle = 'No data found',
  emptyStateDescription = 'There are no records to display at this time.',
  emptyStateAction,
  pagination,
}) => {
  return (
    <div className="flex flex-col min-w-0 w-full">
      <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
        <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div className="overflow-hidden shadow sm:rounded-lg">
            <table className="min-w-full divide-y divide-slate-300">
              <thead className="bg-slate-50">
                <tr>
                  {columns.map((column, i) => (
                    <th
                      key={i}
                      scope="col"
                      className={`px-3 py-3.5 text-left text-sm font-semibold text-slate-900 ${column.className || ''}`}
                    >
                      {column.header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {isLoading ? (
                  <tr>
                    <td colSpan={columns.length} className="px-3 py-12 text-center">
                      <LoadingSpinner />
                    </td>
                  </tr>
                ) : data.length === 0 ? (
                  <tr>
                    <td colSpan={columns.length} className="px-3 py-12">
                      <EmptyState 
                        title={emptyStateTitle}
                        description={emptyStateDescription}
                        action={emptyStateAction}
                      />
                    </td>
                  </tr>
                ) : (
                  data.map((row, rowIndex) => (
                    <tr key={rowIndex} className="transition-colors duration-200 hover:bg-slate-50">
                      {columns.map((column, colIndex) => (
                        <td
                          key={colIndex}
                          className={`whitespace-nowrap px-3 py-4 text-sm text-slate-500 ${column.cellClassName || ''}`}
                        >
                          {column.cell ? column.cell(row) : row[column.accessor]}
                        </td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          
          {pagination && !isLoading && data.length > 0 && (
            <div className="mt-4">
              {pagination}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
export default DataTable;