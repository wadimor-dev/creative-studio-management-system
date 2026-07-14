import React, { useState, useEffect } from 'react';
import Button from '../../../components/common/Button';

const formatDuration = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
};

const parseAsWIB = (value) => {
  if (!value) return null;

  if (value instanceof Date) {
    return value;
  }

  const input = String(value).trim();
  if (!input) return null;

  const hasTimezone = /([zZ]|[+-]\d{2}:?\d{2})$/.test(input);
  if (hasTimezone) {
    const parsed = new Date(input);
    if (!Number.isNaN(parsed.getTime())) return parsed;
  }

  const normalized = input.replace(' ', 'T');
  const match = normalized.match(/^(\d{4})-(\d{2})-(\d{2})[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.(\d{3}))?)?$/);

  if (match) {
    const [, year, month, day, hour, minute, second = '00'] = match;
    const utcTimestamp = Date.UTC(
      Number(year),
      Number(month) - 1,
      Number(day),
      Number(hour),
      Number(minute),
      Number(second),
    );
    return new Date(utcTimestamp - 7 * 60 * 60 * 1000);
  }

  const parsed = new Date(input);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
};

const formatWIBDateTime = (value) => {
  const date = parseAsWIB(value);
  if (!date) return '-';

  try {
    const formatter = new Intl.DateTimeFormat('id-ID', {
      timeZone: 'Asia/Jakarta',
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });

    return `${formatter.format(date)} WIB`;
  } catch (error) {
    return '-';
  }
};

const CurrentActivityCard = ({ activity, onAddProgress, onFinish, onPause, onResume, onCancel }) => {
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    let interval = null;
    
    if (activity) {
      if (activity.status === 'WORKING' && activity.current_session_started_at) {
        const sessionStart = parseAsWIB(activity.current_session_started_at);
        if (sessionStart) {
          const updateTimer = () => {
            const now = Date.now();
            const diffInSeconds = Math.floor((now - sessionStart.getTime()) / 1000);
            const total = (activity.worked_seconds || 0) + (diffInSeconds > 0 ? diffInSeconds : 0);
            setDuration(total);
          };

          updateTimer();
          interval = setInterval(updateTimer, 1000);
        } else {
          setDuration(activity.worked_seconds || 0);
        }
      } else {
        // For PAUSED or other states, just show accumulated seconds
        setDuration(activity.worked_seconds || 0);
      }
    } else {
      setDuration(0);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [activity]);

  if (!activity) return null;

  const isWorking = activity.status === 'WORKING';
  const isPaused = activity.status === 'PAUSED';
  const canCancel = isWorking || isPaused;

  return (
    <div className="mb-6 overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-gray-900/5 dark:bg-gray-800 dark:ring-gray-700">
      <div className="border-b border-gray-100 bg-gray-50/50 px-6 py-4 dark:border-gray-700 dark:bg-gray-800/50">
        <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">Current Activity</h3>
      </div>
      <div className="p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">
              {activity.activity_name}
            </h2>
            <div className="mt-2 flex items-center gap-3">
              <span className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${isWorking ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' : 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400'}`}>
                {activity.status}
              </span>
              <span className="text-sm text-gray-500 dark:text-gray-400">
                {activity.category?.name || 'Uncategorized'}
              </span>
            </div>
          </div>
          
          <div className="flex flex-col items-start md:items-end">
            <div className="text-3xl font-mono font-bold text-gray-900 dark:text-white tracking-tight">
              {formatDuration(duration)}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
              Started at: {formatWIBDateTime(activity.start_time)}
            </div>
          </div>
        </div>

        
        {activity.assets && activity.assets.length > 0 && (
          <div className="mt-4 rounded-xl border border-gray-100 bg-gray-50/50 p-4 dark:border-gray-700 dark:bg-gray-800/50">
            <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Asset Digunakan ({activity.assets.length} Item)
            </h4>
            <ul className="list-inside list-disc text-sm text-gray-600 dark:text-gray-400">
              {activity.assets.map((a, idx) => (
                <li key={idx}>Item #{a.item_id} (Qty: {a.quantity})</li>
              ))}
            </ul>
          </div>
        )}

        <div className="mt-6 flex flex-wrap gap-3 pt-6 border-t border-gray-100 dark:border-gray-700">
          <Button
            type="button"
            variant="secondary"
            size="md"
            onClick={() => onAddProgress(activity.id)}
            disabled={!isWorking}
            className="!px-4 !py-2.5"
          >
            Add Progress
          </Button>
          {isWorking ? (
            <Button
              type="button"
              variant="outline"
              size="md"
              onClick={() => onPause(activity.id)}
              className="!px-4 !py-2.5"
            >
              Pause
            </Button>
          ) : null}
          {isPaused ? (
            <Button
              type="button"
              variant="secondary"
              size="md"
              onClick={() => onResume(activity.id)}
              className="!px-4 !py-2.5"
            >
              Resume
            </Button>
          ) : null}
          {canCancel ? (
            <Button
              type="button"
              variant="danger"
              size="md"
              onClick={() => onCancel(activity.id)}
              className="!px-4 !py-2.5"
            >
              Cancel
            </Button>
          ) : null}
          <Button
            type="button"
            variant="primary"
            size="md"
            onClick={() => onFinish(activity.id)}
            disabled={!isWorking}
            className="!px-4 !py-2.5"
          >
            Finish Work
          </Button>
        </div>
      </div>
    </div>
  );
};

export default CurrentActivityCard;
