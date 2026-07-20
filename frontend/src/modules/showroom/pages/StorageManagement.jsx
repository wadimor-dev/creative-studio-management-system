import React, { useState, useEffect, useCallback } from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import Modal from '../../../components/common/Modal';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import { showroomService } from '../../../api/services/showroomService';
import { FolderTree, Plus, Edit, Trash2, ChevronRight, ChevronDown } from 'lucide-react';

const STORAGE_TYPES = [
  { value: 'shelf', label: 'Rak' },
  { value: 'rack', label: 'Rack' },
  { value: 'cabinet', label: 'Lemari' },
  { value: 'drawer', label: 'Laci' },
  { value: 'hanger', label: 'Gantungan' },
  { value: 'hook', label: 'Kait' },
  { value: 'floor', label: 'Lantai' },
  { value: 'wall', label: 'Dinding' },
  { value: 'other', label: 'Lainnya' },
];

const CAPACITY_UNITS = [
  { value: 'PCS', label: 'PCS' },
  { value: 'BOX', label: 'BOX' },
  { value: 'HANGER', label: 'HANGER' },
  { value: 'ROLL', label: 'ROLL' },
];

const TreeNode = ({ node, level = 0, onEdit, onDelete, onAddChild, expanded, toggleExpand }) => {
  const hasChildren = node.children && node.children.length > 0;
  const capacityPct = node.capacity_qty > 0 ? Math.round((node.used_capacity / node.capacity_qty) * 100) : null;
  const capacityColor = capacityPct === null ? 'text-slate-400' : capacityPct > 90 ? 'text-red-500' : capacityPct > 70 ? 'text-amber-500' : 'text-emerald-500';

  return (
    <div>
      <div
        className="flex items-center gap-2 py-2 px-3 rounded-lg hover:bg-slate-50 group"
        style={{ paddingLeft: `${level * 24 + 12}px` }}
      >
        {hasChildren ? (
          <button onClick={() => toggleExpand(node.id)} className="text-slate-400 hover:text-slate-600">
            {expanded[node.id] ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>
        ) : (
          <span className="w-4" />
        )}

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-medium text-sm text-slate-800">{node.name}</span>
            <span className="text-xs text-slate-400 font-mono">{node.code}</span>
            {node.storage_type && (
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-500 uppercase">
                {node.storage_type}
              </span>
            )}
          </div>
          <div className="flex items-center gap-3 mt-0.5">
            {capacityPct !== null && (
              <span className={`text-xs font-medium ${capacityColor}`}>
                {node.used_capacity}/{node.capacity_qty} {node.capacity_unit || 'PCS'} ({capacityPct}%)
              </span>
            )}
            {node.path && <span className="text-[10px] text-slate-400 font-mono">{node.path}</span>}
          </div>
        </div>

        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button onClick={() => onAddChild(node)} className="p-1.5 rounded-md hover:bg-slate-200 text-slate-400 hover:text-indigo-600" title="Add Child">
            <Plus size={14} />
          </button>
          <button onClick={() => onEdit(node)} className="p-1.5 rounded-md hover:bg-slate-200 text-slate-400 hover:text-indigo-600" title="Edit">
            <Edit size={14} />
          </button>
          <button onClick={() => onDelete(node)} className="p-1.5 rounded-md hover:bg-slate-200 text-slate-400 hover:text-red-500" title="Delete">
            <Trash2 size={14} />
          </button>
        </div>
      </div>

      {hasChildren && expanded[node.id] && node.children.map(child => (
        <TreeNode
          key={child.id}
          node={child}
          level={level + 1}
          onEdit={onEdit}
          onDelete={onDelete}
          onAddChild={onAddChild}
          expanded={expanded}
          toggleExpand={toggleExpand}
        />
      ))}
    </div>
  );
};

const StorageManagement = () => {
  const [tree, setTree] = useState([]);
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [parentId, setParentId] = useState(null);
  const [form, setForm] = useState({
    name: '', code: '', location_id: '', storage_type: 'shelf',
    capacity_qty: '', capacity_unit: 'PCS', capacity_note: '', description: '',
  });
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [expanded, setExpanded] = useState({});

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const [treeRes, locsRes] = await Promise.all([
        showroomService.getStorageTree(),
        showroomService.getAllLocations(),
      ]);
      if (treeRes.success) setTree(treeRes.data);
      if (locsRes.success) setLocations(locsRes.data);
    } catch {} finally { setLoading(false); }
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);

  const toggleExpand = (id) => setExpanded(prev => ({ ...prev, [id]: !prev[id] }));

  const handleAddRoot = () => {
    setEditing(null);
    setParentId(null);
    setForm({ name: '', code: '', location_id: locations[0]?.id || '', storage_type: 'shelf', capacity_qty: '', capacity_unit: 'PCS', capacity_note: '', description: '' });
    setShowForm(true);
  };

  const handleAddChild = (parent) => {
    setEditing(null);
    setParentId(parent.id);
    setForm({ name: '', code: '', location_id: parent.location_id, storage_type: 'shelf', capacity_qty: '', capacity_unit: 'PCS', capacity_note: '', description: '' });
    setShowForm(true);
  };

  const handleEdit = (node) => {
    setEditing(node);
    setParentId(node.parent_id);
    setForm({
      name: node.name, code: node.code, location_id: node.location_id,
      storage_type: node.storage_type, capacity_qty: node.capacity_qty || '',
      capacity_unit: node.capacity_unit || 'PCS', capacity_note: node.capacity_note || '',
      description: node.description || '',
    });
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = { ...form, parent_id: parentId };
      if (payload.capacity_qty) payload.capacity_qty = parseInt(payload.capacity_qty);
      else delete payload.capacity_qty;
      if (!payload.location_id) payload.location_id = locations[0]?.id;
      if (editing) {
        await showroomService.updateStorageLocation(editing.id, payload);
      } else {
        await showroomService.createStorageLocation(payload);
      }
      setShowForm(false);
      setEditing(null);
      fetchData();
    } catch {}
  };

  const handleDelete = async () => {
    if (!confirmDelete) return;
    try {
      await showroomService.deleteStorageLocation(confirmDelete.id);
      setConfirmDelete(null);
      fetchData();
    } catch {}
  };

  const locationMap = Object.fromEntries(locations.map(l => [l.id, l]));

  if (loading) return <LoadingSpinner />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Manajemen Storage"
        description="Kelola lokasi penyimpanan fisik (rak, laci, gantungan)"
        action={<Button onClick={handleAddRoot} icon={<Plus size={16} />}>Tambah Root</Button>}
      />

      {tree.length === 0 ? (
        <EmptyState
          icon={FolderTree}
          title="Belum ada storage location"
          description="Buat storage location pertama untuk mengelola lokasi penyimpanan fisik"
          action={<Button onClick={handleAddRoot} icon={<Plus size={16} />}>Buat Storage</Button>}
        />
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-4 py-3 border-b border-slate-100 flex items-center gap-2">
            <FolderTree size={16} className="text-indigo-500" />
            <span className="text-sm font-semibold text-slate-700">Storage Tree</span>
          </div>
          <div className="divide-y divide-slate-50">
            {tree.map(node => (
              <TreeNode
                key={node.id}
                node={node}
                onEdit={handleEdit}
                onDelete={setConfirmDelete}
                onAddChild={handleAddChild}
                expanded={expanded}
                toggleExpand={toggleExpand}
              />
            ))}
          </div>
        </div>
      )}

      {showForm && (
        <Modal isOpen={showForm} onClose={() => setShowForm(false)} title={editing ? 'Edit Storage' : 'Tambah Storage'}>
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input label="Nama" placeholder="Nama storage location" value={form.name} onChange={e => setForm({ ...form, name: e.target.value })} required />
            <Input label="Kode" placeholder="e.g. A-01-02" value={form.code} onChange={e => setForm({ ...form, code: e.target.value })} required />
            <Select
              label="Lokasi Utama"
              value={form.location_id}
              onChange={e => setForm({ ...form, location_id: e.target.value })}
              options={locations.map(l => ({ value: l.id, label: `${l.name} (${l.code})` }))}
              required
            />
            <Select
              label="Tipe Storage"
              value={form.storage_type}
              onChange={e => setForm({ ...form, storage_type: e.target.value })}
              options={STORAGE_TYPES}
            />
            <div className="grid grid-cols-2 gap-3">
              <Input label="Kapasitas" type="number" placeholder="Jumlah kapasitas" value={form.capacity_qty} onChange={e => setForm({ ...form, capacity_qty: e.target.value })} />
              <Select label="Unit" value={form.capacity_unit} onChange={e => setForm({ ...form, capacity_unit: e.target.value })} options={CAPACITY_UNITS} />
            </div>
            <Input label="Catatan Kapasitas" placeholder="Catatan kapasitas (opsional)" value={form.capacity_note} onChange={e => setForm({ ...form, capacity_note: e.target.value })} />
            <Textarea label="Deskripsi" placeholder="Deskripsi storage (opsional)" value={form.description} onChange={e => setForm({ ...form, description: e.target.value })} />
            {parentId && <p className="text-xs text-slate-500">Parent: {locationMap[form.location_id]?.name || 'N/A'}</p>}
            <div className="flex justify-end gap-2 pt-2">
              <Button type="button" variant="ghost" onClick={() => setShowForm(false)}>Batal</Button>
              <Button type="submit">{editing ? 'Update' : 'Simpan'}</Button>
            </div>
          </form>
        </Modal>
      )}

      <ConfirmDialog
        isOpen={!!confirmDelete}
        onClose={() => setConfirmDelete(null)}
        onConfirm={handleDelete}
        title="Hapus Storage?"
        description={`Yakin ingin menghapus "${confirmDelete?.name}"? Storage yang sudah dihapus tidak dapat dikembalikan.`}
      />
    </div>
  );
};

export default StorageManagement;
