import React from 'react';
import DataTable from '../../../components/common/DataTable';
import Avatar from '../../../components/common/Avatar';
import RoleBadge from '../../../components/common/RoleBadge';
import Badge from '../../../components/common/Badge';
import Button from '../../../components/common/Button';
import { Edit2, Trash2 } from 'lucide-react';

const UserTable = ({ data, onEdit, onDelete }) => {
  const columns = [
    {
      header: 'User',
      cell: (row) => (
        <div className="flex items-center gap-3">
          <Avatar src={row.avatar} name={row.full_name || row.username} size="md" />
          <div className="font-medium text-slate-900">{row.full_name || row.username}</div>
        </div>
      )
    },
    {
      header: 'Email',
      accessor: 'email',
      cellClassName: 'text-slate-500'
    },
    {
      header: 'Role',
      cell: (row) => <RoleBadge role={row.role?.name || row.role} />
    },
    {
      header: 'Status',
      cell: (row) => (
        <Badge variant={row.is_active || row.status === 'ACTIVE' ? 'success' : 'default'}>
          {row.is_active ? 'ACTIVE' : (row.status || 'INACTIVE')}
        </Badge>
      )
    },
    {
      header: 'Action',
      cellClassName: 'text-right',
      cell: (row) => (
        <div className="flex justify-end gap-2">
          <Button variant="edit" onClick={() => onEdit(row)}>
            <Edit2 size={14} />
          </Button>
          <Button variant="delete" onClick={() => onDelete(row)}>
            <Trash2 size={14} />
          </Button>
        </div>
      )
    }
  ];

  return <DataTable columns={columns} data={data} />;
};

export default UserTable;
