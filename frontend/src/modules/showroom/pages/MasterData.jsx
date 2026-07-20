import React, { useState } from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import { useShowroomMasterData } from '../../../hooks/useShowroomV2';
import { Settings, Plus, Trash2, Edit, RefreshCw } from 'lucide-react';

const MASTER_TYPES = [
  { value: 'sample_type', label: 'Sample Type', desc: 'Tipe sample (Display, Photography, Premium, Archive)' },
  { value: 'maintenance_type', label: 'Maintenance Type', desc: 'Tipe maintenance (Cleaning, Repair, Laundry, Retired)' },
  { value: 'purpose', label: 'Purpose', desc: 'Tujuan penggunaan sample' },
  { value: 'borrow_reason', label: 'Borrow Reason', desc: 'Alasan peminjaman' },
  { value: 'release_reason', label: 'Release Reason', desc: 'Alasan rilis ke tamu' },
  { value: 'location_type', label: 'Location Type', desc: 'Tipe lokasi (Internal, External)' },
];

const MasterData = () => {
  const [selectedType, setSelectedType] = useState('sample_type');
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [form, setForm] = useState({ name: '', value: '', description: '', sort_order: 0 });
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [confirmSeed, setConfirmSeed] = useState(false);

  const { items, loading, refetch, create, update, remove, seed } = useShowroomMasterData(selectedType);

  const handleSeed = async () => {
    setConfirmSeed(false);
    await seed();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await update(editingItem.id, form);
      } else {
        await create({ ...form, type: selectedType });
      }
      setShowForm(false);
      setEditingItem(null);
      setForm({ name: '', value: '', description: '', sort_order: 0 });
    } catch (err) { /* handled by hook */ }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setForm({ name: item.name, value: item.value, description: item.description || '', sort_order: item.sort_order || 0 });
    setShowForm(true);
  };

  const handleDelete = async () => {
    if (confirmDelete) {
      await remove(confirmDelete.id);
      setConfirmDelete(null);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Master Data"
        description="Konfigurasi data referensi showroom"
        actions={
          <Button onClick={() => setConfirmSeed(true)} variant="secondary" size="sm">
            <RefreshCw className="mr-1.5 h-4 w-4" />
            Seed Defaults
          </Button>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <div className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-700 mb-3">Tipe Master Data</h3>
            <div className="space-y-1">
              {MASTER_TYPES.map((t) => (
                <button
                  key={t.value}
                  onClick={() => { setSelectedType(t.value); setShowForm(false); setEditingItem(null); }}
                  className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all duration-200 ${
                    selectedType === t.value
                      ? 'bg-brand-50 text-brand-700 font-medium border border-brand-200 shadow-sm'
                      : 'text-slate-600 hover:bg-slate-50 border border-transparent'
                  }`}
                >
                  <div>{t.label}</div>
                  <div className="text-xs text-slate-400 mt-0.5">{t.desc}</div>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div className="rounded-xl border border-slate-200 bg-white shadow-sm">
            <div className="flex items-center justify-between p-4 border-b border-slate-100">
              <h3 className="font-semibold text-slate-900">
                {MASTER_TYPES.find(t => t.value === selectedType)?.label}
                <span className="ml-2 text-sm font-normal text-slate-400">({items.length} items)</span>
              </h3>
              <Button
                onClick={() => { setShowForm(!showForm); setEditingItem(null); setForm({ name: '', value: '', description: '', sort_order: 0 }); }}
                size="sm"
              >
                <Plus className="mr-1 h-4 w-4" />
                Tambah
              </Button>
            </div>

            {showForm && (
              <form onSubmit={handleSubmit} className="p-4 bg-slate-50 border-b border-slate-200 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Name</label>
                    <input
                      type="text"
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Value</label>
                    <input
                      type="text"
                      value={form.value}
                      onChange={(e) => setForm({ ...form, value: e.target.value.toLowerCase().replace(/\s+/g, '_') })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
                      required
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Description</label>
                    <input
                      type="text"
                      value={form.description}
                      onChange={(e) => setForm({ ...form, description: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Sort Order</label>
                    <input
                      type="number"
                      value={form.sort_order}
                      onChange={(e) => setForm({ ...form, sort_order: parseInt(e.target.value) || 0 })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 transition-all"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    {editingItem ? 'Update' : 'Create'}
                  </Button>
                  <Button type="button" variant="secondary" size="sm" onClick={() => { setShowForm(false); setEditingItem(null); }}>
                    Cancel
                  </Button>
                </div>
              </form>
            )}

            <div className="p-4">
              {loading ? (
                <LoadingSpinner />
              ) : items.length === 0 ? (
                <EmptyState
                  icon={Settings}
                  title="Belum ada data"
                  description='Klik "Seed Defaults" untuk populate.'
                />
              ) : (
                <div className="space-y-2">
                  {items.map((item) => (
                    <div key={item.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-slate-200 transition-colors">
                      <div className="flex items-center gap-3">
                        <div className={`w-2 h-2 rounded-full ${item.is_active ? 'bg-emerald-500' : 'bg-slate-300'}`} />
                        <div>
                          <div className="text-sm font-medium text-slate-900">{item.name}</div>
                          <div className="text-xs text-slate-500">
                            <span className="font-mono bg-slate-200 px-1.5 py-0.5 rounded text-slate-600">{item.value}</span>
                            {item.description && <span className="ml-2">{item.description}</span>}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-1">
                        <span className="text-xs text-slate-400 mr-2">#{item.sort_order}</span>
                        <Button variant="edit" size="xs" onClick={() => handleEdit(item)}>
                          <Edit size={14} />
                        </Button>
                        <Button variant="delete" size="xs" onClick={() => setConfirmDelete(item)}>
                          <Trash2 size={14} />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <ConfirmDialog
        isOpen={!!confirmDelete}
        onClose={() => setConfirmDelete(null)}
        onConfirm={handleDelete}
        title="Hapus Item"
        description={`Hapus "${confirmDelete?.name}"?`}
        isDanger
      />

      <ConfirmDialog
        isOpen={confirmSeed}
        onClose={() => setConfirmSeed(false)}
        onConfirm={handleSeed}
        title="Seed Default Data"
        description="Seed default master data? Existing items will not be duplicated."
      />
    </div>
  );
};

export default MasterData;
