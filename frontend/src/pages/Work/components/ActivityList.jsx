import React from 'react';
import ActivityListItem from './ActivityListItem';

const ActivityList = ({ activities, onStart }) => {
  if (!activities || activities.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-12 text-center dark:border-gray-700 dark:bg-gray-800">
        <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
        </svg>
        <h3 className="mt-2 text-sm font-semibold text-gray-900 dark:text-white">Belum ada aktivitas</h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Anda belum membuat aktivitas kerja hari ini.</p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-gray-900/5 dark:bg-gray-800 dark:ring-gray-700">
      <div className="border-b border-gray-100 bg-gray-50/50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Today's Activities</h3>
      </div>
      <div className="divide-y divide-gray-100 dark:divide-gray-700">
        {activities.map(activity => (
          <ActivityListItem key={activity.id} activity={activity} onStart={onStart} />
        ))}
      </div>
    </div>
  );
};

export default ActivityList;
