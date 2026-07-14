import React from 'react';
import { AlertTriangle } from 'lucide-react';
import Modal from './Modal';
import Button from './Button';

const ConfirmDialog = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  description = 'Are you sure you want to perform this action? This cannot be undone.',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  isDanger = false,
  isLoading = false,
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      maxWidth="max-w-md"
      footer={
        <div className="flex w-full gap-3 sm:justify-end">
          <Button 
            variant="secondary" 
            onClick={onClose} 
            disabled={isLoading}
            className="w-full sm:w-auto"
          >
            {cancelText}
          </Button>
          <Button 
            variant={isDanger ? 'danger' : 'primary'} 
            onClick={onConfirm} 
            isLoading={isLoading}
            className="w-full sm:w-auto"
          >
            {confirmText}
          </Button>
        </div>
      }
    >
      <div className="sm:flex sm:items-start">
        <div className={`mx-auto flex h-12 w-12 flex-shrink-0 items-center justify-center rounded-full sm:mx-0 sm:h-10 sm:w-10 ${isDanger ? 'bg-rose-100' : 'bg-blue-100'}`}>
          <AlertTriangle className={`h-6 w-6 ${isDanger ? 'text-rose-600' : 'text-blue-600'}`} aria-hidden="true" />
        </div>
        <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left">
          <p className="text-sm text-slate-500">
            {description}
          </p>
        </div>
      </div>
    </Modal>
  );
};

export default ConfirmDialog;
