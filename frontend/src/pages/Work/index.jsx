import React, { useState } from 'react';
import { useCurrentActivity } from '../../hooks/useCurrentActivity';
import Button from '../../components/common/Button';
import { useTodayActivities } from '../../hooks/useTodayActivities';
import workActivityService from '../../services/workActivityService';
import workEvidenceService from '../../services/workEvidenceService';

import CurrentActivityCard from './components/CurrentActivityCard';
import ActivityList from './components/ActivityList';
import CreateActivityModal from './components/CreateActivityModal';
import EvidenceUploadModal from './components/EvidenceUploadModal';

const WorkWorkspace = () => {
  const { currentActivity, loading: currentLoading, refetch: refetchCurrent } = useCurrentActivity();
  const { activities, loading: listLoading, refetch: refetchList } = useTodayActivities();
  
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [evidenceModalConfig, setEvidenceModalConfig] = useState({
    isOpen: false,
    type: '',
    activityId: null,
    title: '',
    buttonLabel: ''
  });

  const handleCreateActivity = async (data) => {
    await workActivityService.createActivity(data);
    refetchList();
    refetchCurrent();
  };

  const handlePauseActivity = async (activityId) => {
    await workActivityService.pauseActivity(activityId);
    refetchCurrent();
    refetchList();
  };

  const handleResumeActivity = async (activityId) => {
    await workActivityService.resumeActivity(activityId);
    refetchCurrent();
    refetchList();
  };

  const handleCancelActivity = async (activityId) => {
    await workActivityService.cancelActivity(activityId);
    refetchCurrent();
    refetchList();
  };

  const openBeforeEvidence = async (activityId) => {
    try {
      const response = await workEvidenceService.getEvidences(activityId);
      const evidences = response?.data?.data ?? response?.data ?? response ?? [];
      const hasBeforeEvidence = Array.isArray(evidences) && evidences.some((e) => e.type === 'BEFORE');

      if (hasBeforeEvidence) {
        await workActivityService.startActivity(activityId, []);
        refetchCurrent();
        refetchList();
        return;
      }
    } catch (error) {
      console.error('Failed to check BEFORE evidence', error);
      // fallback to opening the evidence modal
    }

    setEvidenceModalConfig({
      isOpen: true,
      type: 'BEFORE',
      activityId,
      title: 'Ambil Foto Persiapan (Before)',
      buttonLabel: 'START WORK'
    });
  };

  const openProgressEvidence = (activityId) => {
    setEvidenceModalConfig({
      isOpen: true,
      type: 'PROGRESS',
      activityId,
      title: 'Upload Progress Kerja',
      buttonLabel: 'UPLOAD PROGRESS'
    });
  };

  const openAfterEvidence = (activityId) => {
    setEvidenceModalConfig({
      isOpen: true,
      type: 'AFTER',
      activityId,
      title: 'Ambil Foto Hasil (After)',
      buttonLabel: 'FINISH WORK'
    });
  };

  const handleEvidenceSubmit = async (activityId, type, file, description, assets = []) => {
    // 1. Upload evidence
    if (type === 'BEFORE') {
      try {
        await workEvidenceService.uploadEvidence(activityId, type, file, description);
      } catch (error) {
        const message = error?.response?.data?.detail || error?.message || '';
        if (!message.includes('Maximum 1 BEFORE evidence allowed')) {
          throw error;
        }
      }
    } else {
      await workEvidenceService.uploadEvidence(activityId, type, file, description);
    }

    // 2. Perform state transitions if necessary
    if (type === 'BEFORE') {
      await workActivityService.startActivity(activityId, assets);
    } else if (type === 'AFTER') {
      await workActivityService.finishActivity(activityId);
    }
    
    // 3. Refresh Data
    refetchCurrent();
    refetchList();
  };

  // Keep current activity visible in today's activities list too so status changes are reflected immediately.
  const listActivities = activities;

  if (currentLoading || listLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-200 border-t-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Header & Actions */}
      <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-gray-400">Work Workspace</h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Kelola aktivitas kerja Anda hari ini
          </p>
        </div>
        {(!currentActivity || currentActivity.status !== 'WORKING') && (
          <Button
            type="button"
            variant="primary"
            size="sm"
            onClick={() => setIsCreateModalOpen(true)}
            className="gap-2"
          >
            <svg className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
              <path d="M10.75 4.75a.75.75 0 00-1.5 0v4.5h-4.5a.75.75 0 000 1.5h4.5v4.5a.75.75 0 001.5 0v-4.5h4.5a.75.75 0 000-1.5h-4.5v-4.5z" />
            </svg>
            Buat Aktivitas
          </Button>
        )}
      </div>

      {/* Current Activity */}
      {currentActivity ? (
        <CurrentActivityCard 
          activity={currentActivity} 
          onAddProgress={openProgressEvidence}
          onFinish={openAfterEvidence}
          onPause={handlePauseActivity}
          onResume={handleResumeActivity}
          onCancel={handleCancelActivity}
        />
      ) : (
        <div className="mb-8 rounded-2xl border border-dashed border-gray-300 bg-white p-12 text-center dark:border-gray-700 dark:bg-gray-800">
          <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 className="mt-2 text-sm font-semibold text-gray-900 dark:text-white">Belum ada aktivitas</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">Mulai pekerjaan Anda dengan membuat aktivitas baru.</p>
          <div className="mt-6">
            <Button
              type="button"
              variant="primary"
              size="sm"
              onClick={() => setIsCreateModalOpen(true)}
              className="gap-2"
            >
              + Buat Aktivitas
            </Button>
          </div>
        </div>
      )}

      {/* Today's Activities List */}
      {(activities.length > 0 || !currentActivity) && (
        <ActivityList activities={listActivities} onStart={openBeforeEvidence} />
      )}

      {/* Modals */}
      <CreateActivityModal 
        isOpen={isCreateModalOpen} 
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateActivity}
      />
      
      <EvidenceUploadModal
        isOpen={evidenceModalConfig.isOpen}
        onClose={() => setEvidenceModalConfig(prev => ({ ...prev, isOpen: false }))}
        type={evidenceModalConfig.type}
        activityId={evidenceModalConfig.activityId}
        title={evidenceModalConfig.title}
        buttonLabel={evidenceModalConfig.buttonLabel}
        onSubmit={handleEvidenceSubmit}
      />
    </div>
  );
};

export default WorkWorkspace;
