import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import ConfirmDialog from '../../components/common/ConfirmDialog';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import UserStats from './components/UserStats';
import UserFilter from './components/UserFilter';
import UserTable from './components/UserTable';
import UserForm from './components/UserForm';

import { useUsers } from '../../hooks/useUsers';
import { userService } from '../../api/services/userService';

const UsersPage = () => {
  const { users, loading, refetch } = useUsers();

  const [formModal, setFormModal] = useState({ isOpen: false, data: null });
  const [deleteModal, setDeleteModal] = useState({ isOpen: false, data: null });

  const openAddModal = () => setFormModal({ isOpen: true, data: null });
  const openEditModal = (user) => setFormModal({ isOpen: true, data: user });
  const closeFormModal = () => setFormModal({ isOpen: false, data: null });

  const openDeleteModal = (user) => setDeleteModal({ isOpen: true, data: user });
  const closeDeleteModal = () => setDeleteModal({ isOpen: false, data: null });

  const handleFormSubmit = async (data) => {
    try {
      // Extract username from email
      const generatedUsername = data.email.split('@')[0];
      
      const payload = {
        username: generatedUsername,
        full_name: data.name,
        email: data.email,
        password: data.password || undefined,
        role_ids: data.role_ids,
        is_active: data.status === '1'
      };

      let res;
      if (formModal.data?.id) {
        res = await userService.updateUser(formModal.data.id, payload);
      } else {
        res = await userService.createUser(payload);
      }

      if (res.success) {
        toastSuccess(formModal.data ? "User updated successfully!" : "User created successfully!");
        closeFormModal();
        refetch();
      } else {
        toastError(res.message || "Failed to save user");
      }
    } catch (err) {
      if (!err.response) {
        toastError("Failed to connect to server");
      }
    }
  };

  const handleDeleteConfirm = async () => {
    try {
      if (deleteModal.data?.id) {
        const res = await userService.deleteUser(deleteModal.data.id);
        if (res.success) {
          toastSuccess("User deleted successfully!");
          closeDeleteModal();
          refetch();
        } else {
          toastError(res.message || "Failed to delete user");
        }
      }
    } catch (err) {
      toastError("Failed to connect to server");
    }
  };

  if (loading && !users) {
    return (
      <div className="flex justify-center items-center h-full min-h-[400px]">
        <LoadingSpinner size="lg" text="Loading users..." />
      </div>
    );
  }

  // The backend returns an array of users in res.data
  const usersList = Array.isArray(users) ? users : (users?.items || []);
  
  // Calculate stats on the fly since backend paginated response doesn't include them
  const safeStats = users?.stats || { 
    total: usersList.length, 
    active: usersList.filter(u => u.is_active).length, 
    inactive: usersList.filter(u => !u.is_active).length 
  };
  const safeUsersList = usersList;

  return (
    <div>
      <PageHeader 
        title="User Management" 
        description="Manage system access, roles, and user accounts."
        action={
          <Button variant="primary" className="gap-2" onClick={openAddModal}>
            <Plus size={16} />
            Add User
          </Button>
        }
      />

      <div className="space-y-6">
        <UserStats stats={safeStats} />
        
        <div className="bg-white p-4 sm:p-6 rounded-xl border border-slate-200 shadow-sm">
          <UserFilter />
          {loading ? (
            <div className="flex justify-center p-8"><LoadingSpinner /></div>
          ) : (
            <UserTable 
              data={safeUsersList} 
              onEdit={openEditModal} 
              onDelete={openDeleteModal} 
            />
          )}
        </div>
      </div>

      <Modal 
        isOpen={formModal.isOpen} 
        onClose={closeFormModal} 
        title={formModal.data ? 'Edit User' : 'Add New User'}
      >
        <UserForm 
          initialData={formModal.data}
          onSubmit={handleFormSubmit}
          onCancel={closeFormModal}
        />
      </Modal>

      <ConfirmDialog 
        isOpen={deleteModal.isOpen}
        onClose={closeDeleteModal}
        onConfirm={handleDeleteConfirm}
        title="Delete User"
        description={`Are you sure you want to delete user "${deleteModal.data?.name}"? This action cannot be undone and will revoke their system access.`}
        isDanger={true}
        confirmText="Delete User"
      />
    </div>
  );
};

export default UsersPage;
