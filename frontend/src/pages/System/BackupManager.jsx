import React from 'react';
import { useQuery, useMutation } from '@tanstack/react-query';
import { systemService } from '../../api/services/systemService';
import PageHeader from '../../components/common/PageHeader';
import { DatabaseBackup, Download, Plus, HardDrive } from 'lucide-react';
import DataTable from '../../components/common/DataTable';
import { useAuth } from '../../contexts/AuthContext';
import apiClient from '../../api/axios';

const formatBytes = (bytes, decimals = 2) => {
    if (!+bytes) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
};

export default function BackupManager() {
  const { user } = useAuth();
  
  const { data: backupData, isLoading, error, refetch } = useQuery({
    queryKey: ['system-backups'],
    queryFn: () => systemService.getBackups(),
    refetchInterval: 10000,
  });

  const triggerMutation = useMutation({
    mutationFn: () => systemService.triggerBackup(),
    onSuccess: () => {
      alert("Backup triggered successfully. It will run in the background.");
      setTimeout(refetch, 3000);
    },
    onError: (err) => {
      alert("Failed to trigger backup: " + err.message);
    }
  });

  const handleDownload = async (filename) => {
    try {
      // First get the token manually to append
      const token = localStorage.getItem('token');
      // Constructing API URL for download
      const response = await apiClient.get(`/system/backups/download/${filename}`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (e) {
      alert("Failed to download file");
    }
  };

  const columns = React.useMemo(
    () => [
      {
        Header: 'Filename',
        accessor: 'filename',
        Cell: ({ value }) => (
          <div className="flex items-center gap-2">
            <HardDrive className="w-4 h-4 text-slate-400" />
            <span className="font-medium text-slate-700">{value}</span>
          </div>
        )
      },
      {
        Header: 'Size',
        accessor: 'size_bytes',
        Cell: ({ value }) => formatBytes(value),
      },
      {
        Header: 'Created At',
        accessor: 'created_at',
        Cell: ({ value }) => new Date(value).toLocaleString(),
      },
      {
        Header: 'Actions',
        id: 'actions',
        Cell: ({ row }) => (
          <button 
            onClick={() => handleDownload(row.original.filename)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-brand-600 hover:text-brand-700 hover:bg-brand-50 rounded-lg transition-colors"
          >
            <Download className="w-4 h-4" />
            Download
          </button>
        )
      }
    ],
    []
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="System Backups"
        description="Manage and download database and file backups"
        action={
          <button
            onClick={() => triggerMutation.mutate()}
            disabled={triggerMutation.isPending}
            className="flex items-center gap-2 px-4 py-2 bg-brand-600 text-white rounded-xl hover:bg-brand-700 transition-colors disabled:opacity-50 font-medium shadow-sm shadow-brand-200"
          >
            <Plus size={18} />
            {triggerMutation.isPending ? "Starting..." : "Create Backup Now"}
          </button>
        }
      />

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        {isLoading ? (
          <div className="flex justify-center p-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600"></div>
          </div>
        ) : error ? (
          <div className="p-12 text-center text-red-500 bg-red-50">
            Failed to load backups. Ensure you have the correct permissions.
          </div>
        ) : (
          <DataTable 
            columns={columns} 
            data={backupData?.data || []} 
            searchable={true}
            searchPlaceholder="Search files..."
          />
        )}
      </div>
    </div>
  );
}
