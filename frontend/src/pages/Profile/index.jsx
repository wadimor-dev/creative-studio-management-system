import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Avatar from '../../components/common/Avatar';
import RoleBadge from '../../components/common/RoleBadge';
import { useAuth } from '../../contexts/AuthContext';
import { toastSuccess, toastError } from '../../utils/toast';

import ProfileForm from './components/ProfileForm';
import PasswordForm from './components/PasswordForm';
import { useProfile } from '../../hooks/useProfile';
import LoadingSpinner from '../../components/common/LoadingSpinner';

const ProfilePage = () => {
  const { user } = useAuth();
  const { updateProfile, changePassword, loading } = useProfile();
  const [activeTab, setActiveTab] = useState('Profile');

  const handleProfileSubmit = async (data) => {
    const success = await updateProfile(data);
    if (success) {
      toastSuccess("Profile information updated successfully.");
    }
  };

  const handlePasswordSubmit = async (data) => {
    const success = await changePassword(data);
    if (success) {
      toastSuccess("Password changed successfully.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto relative">
      <PageHeader 
        title="Account Settings" 
        description="Manage your profile information and security settings."
      />

      {loading && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-white/50 backdrop-blur-sm rounded-xl">
          <LoadingSpinner size="md" />
        </div>
      )}

      <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-8 border-b border-slate-200 flex flex-col sm:flex-row items-center sm:items-start gap-6">
          <Avatar name={user?.name || 'User'} size="xl" />
          <div className="text-center sm:text-left mt-2 sm:mt-0">
            <h2 className="text-2xl font-bold text-slate-900">{user?.name || 'Administrator'}</h2>
            <p className="text-slate-500 mt-1">{user?.email || 'admin@creativestudio.com'}</p>
            <div className="mt-3">
              <RoleBadge role={user?.role || 'ADMIN'} />
            </div>
          </div>
        </div>

        <div className="flex border-b border-slate-200 px-4">
          {['Profile', 'Security'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`
                px-6 py-4 text-sm font-medium transition-colors border-b-2 -mb-px
                ${activeTab === tab 
                  ? 'border-brand-500 text-brand-600' 
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'}
              `}
            >
              {tab}
            </button>
          ))}
        </div>

        <div className="p-8">
          {activeTab === 'Profile' && (
            <div>
              <h3 className="text-lg font-semibold text-slate-900 mb-6">Personal Information</h3>
              <ProfileForm user={user} onSubmit={handleProfileSubmit} />
            </div>
          )}

          {activeTab === 'Security' && (
            <div>
              <h3 className="text-lg font-semibold text-slate-900 mb-6">Change Password</h3>
              <PasswordForm onSubmit={handlePasswordSubmit} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
