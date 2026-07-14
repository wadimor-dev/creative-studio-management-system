import React from 'react';
import Button from '../../../components/common/Button';

const getStatusColor = (status) => {
  switch (status) {
    case 'READY': return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300 ring-1 ring-gray-200 dark:ring-gray-700';
    case 'WORKING': return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 ring-1 ring-green-200 dark:ring-green-800';
    case 'PAUSED': return 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400 ring-1 ring-orange-200 dark:ring-orange-800';
    case 'COMPLETED': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 ring-1 ring-blue-200 dark:ring-blue-800';
    case 'CANCELLED': return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400 ring-1 ring-red-200 dark:ring-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

const ActivityListItem = ({ activity, onStart }) => {
  return (
    <div className="flex items-center justify-between gap-4 py-4 px-5 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors border-b border-gray-100 dark:border-gray-700 last:border-0">
      <div>
        <h4 className="font-medium text-gray-900 dark:text-white">{activity.activity_name}</h4>
        <div className="mt-1 flex items-center gap-2">
          <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${getStatusColor(activity.status)}`}>
            {activity.status}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {activity.category?.name || 'Uncategorized'}
          </span>
        </div>
      </div>
      
      <div>
        {activity.status === 'READY' && (
          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={() => onStart(activity.id)}
            className="gap-1.5"
          >
            Start
          </Button>
        )}
      </div>
    </div>
  );
};

export default ActivityListItem;
