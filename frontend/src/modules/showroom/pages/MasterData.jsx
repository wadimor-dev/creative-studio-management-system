import React, { useState, useEffect, useCallback } from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import { useShowroomMasterData } from '../../../hooks/useShowroomV2';
import { showroomService } from '../../../api/services/showroomService';
import { Settings, Plus, Trash2, Edit, RefreshCw } from 'lucide-react';

const MASTER_TYPES = [
  { value: 'sample_type', label: 'Sample Type', desc: 'Tipe sample (Display, Photography, Premium, Archive)' },
  { value: 'maintenance_type', label: 'Maintenance Type', desc: 'Tipe maintenance (Cleaning, Repair, Laundry, Retired)' },
  { value: 'purpose', label: 'Purpose', desc: 'Tujuan penggunaan sample' },
  { value: 'borrow_reason', label: 'Borrow Reason', desc: 'Alasan peminjaman' },
  { value: 'release_reason', label: 'Release Reason', desc: 'Alasan rilis ke tamu' },
  { value: 'location_type', label: 'Location Type', desc: 'Tipe lokasi (Internal, External)' },
  { value: 'movement_type', label: 'Movement Type', desc: 'Tipe pergerakan (Handover, Borrow, Return, dll)' },
  { value: 'location', label: 'Location', desc: 'Lokasi showroom (Ruang Meeting, Display Area, dll)' },
];

const DIRECTION_OPTIONS = [
  { value: 'IN', label: 'Masuk (IN)' },
  { value: 'OUT', label: 'Keluar (OUT)' },
];

const LOCATION_TYPE_OPTIONS = [
  { value: 'internal', label: 'Internal' },
  { value: 'external', label: 'External' },
];

const MasterData = () => {
  const [selectedType, setSelectedType] = useState('sample_type');
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [form, setForm] = useState({ name: '', value: '', description: '', sort_order: 0 });
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [confirmSeed, setConfirmSeed] = useState(false);

  const { items, loading, refetch, create, update, remove, seed } = useShowroomMasterData(selectedType);

  const [mtItems, setMtItems] = useState([]);
  const [mtLoading, setMtLoading] = useState(false);
  const [mtForm, setMtForm] = useState({ code: '', name: '', direction: 'IN', is_active: true, notes: '' });

  const [locItems, setLocItems] = useState([]);
  const [locLoading, setLocLoading] = useState(false);
  const [locForm, setLocForm] = useState({ code: '', name: '', type: 'internal', description: '', is_active: true });

  const fetchMovementTypes = useCallback(async () => {
    setMtLoading(true);
    try {
      const res = await showroomService.listMovementTypes({ active_only: false });
      if (res.success) setMtItems(res.data || []);
    } catch (_) {} finally {
      setMtLoading(false);
    }
  }, []);

  const fetchLocations = useCallback(async () => {
    setLocLoading(true);
    try {
      const res = await showroomService.getAllLocations();
      if (res.success) setLocItems(res.data || []);
    } catch (_) {} finally {
      setLocLoading(false);
    }
  }, []);

  useEffect(() => {
    if (selectedType === 'movement_type') fetchMovementTypes();
    if (selectedType === 'location') fetchLocations();
  }, [selectedType, fetchMovementTypes, fetchLocations]);

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
    } catch (err) {}
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setForm({ name: item.name, value: item.value, description: item.description || '', sort_order: item.sort_order || 0 });
    setShowForm(true);
  };

  const handleDelete = async () => {
    if (confirmDelete) {
      if (selectedType === 'movement_type') {
        await showroomService.deleteMovementType(confirmDelete.id);
        fetchMovementTypes();
      } else if (selectedType === 'location') {
        await showroomService.deleteLocation(confirmDelete.id);
        fetchLocations();
      } else {
        await remove(confirmDelete.id);
      }
      setConfirmDelete(null);
    }
  };

  const handleMtSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await showroomService.updateMovementType(editingItem.id, mtForm);
      } else {
        await showroomService.createMovementType(mtForm);
      }
      setShowForm(false);
      setEditingItem(null);
      setMtForm({ code: '', name: '', direction: 'IN', is_active: true, notes: '' });
      fetchMovementTypes();
    } catch (err) {}
  };

  const handleMtEdit = (item) => {
    setEditingItem(item);
    setMtForm({ code: item.code, name: item.name, direction: item.direction, is_active: item.is_active, notes: item.notes || '' });
    setShowForm(true);
  };

  const handleLocSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingItem) {
        await showroomService.updateLocation(editingItem.id, locForm);
      } else {
        await showroomService.createLocation(locForm);
      }
      setShowForm(false);
      setEditingItem(null);
      setLocForm({ code: '', name: '', type: 'internal', description: '', is_active: true });
      fetchLocations();
    } catch (err) {}
  };

  const handleLocEdit = (item) => {
    setEditingItem(item);
    setLocForm({ code: item.code, name: item.name, type: item.type, description: item.description || '', is_active: item.is_active });
    setShowForm(true);
  };

  const resetForm = () => {
    setEditingItem(null);
    if (selectedType === 'movement_type') {
      setMtForm({ code: '', name: '', direction: 'IN', is_active: true, notes: '' });
    } else if (selectedType === 'location') {
      setLocForm({ code: '', name: '', type: 'internal', description: '', is_active: true });
    } else {
      setForm({ name: '', value: '', description: '', sort_order: 0 });
    }
  };

  const hasSeed = selectedType !== 'movement_type' && selectedType !== 'location';

  return (
    <div className="space-y-6">
      <PageHeader
        title="Master Data"
        description="Konfigurasi data referensi showroom"
        actions={
          hasSeed && (
            <Button onClick={() => setConfirmSeed(true)} variant="secondary" size="sm">
              <RefreshCw className="mr-1.5 h-4 w-4" />
              Seed Defaults
            </Button>
          )
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
                  onClick={() => { setSelectedType(t.value); resetForm(); }}
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
                <span className="ml-2 text-sm font-normal text-slate-400">(
                  {selectedType === 'movement_type' ? mtItems.length : selectedType === 'location' ? locItems.length : items.length} items)
                </span>
              </h3>
              <Button
                onClick={() => { setShowForm(!showForm); setEditingItem(null); resetForm(); }}
                size="sm"
              >
                <Plus className="mr-1 h-4 w-4" />
                Tambah
              </Button>
            </div>

            {showForm && selectedType === 'movement_type' && (
              <form onSubmit={handleMtSubmit} className="p-4 bg-slate-50 border-b border-slate-200 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Code</label>
                    <input
                      type="text"
                      value={mtForm.code}
                      onChange={(e) => setMtForm({ ...mtForm, code: e.target.value.toUpperCase().replace(/\s+/g, '_') })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 font-mono"
                      placeholder="SHOWROOM_IN"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Name</label>
                    <input
                      type="text"
                      value={mtForm.name}
                      onChange={(e) => setMtForm({ ...mtForm, name: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                      placeholder="Showroom In"
                      required
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Direction</label>
                    <select
                      value={mtForm.direction}
                      onChange={(e) => setMtForm({ ...mtForm, direction: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      {DIRECTION_OPTIONS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Active</label>
                    <div className="flex items-center h-full pt-1">
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={mtForm.is_active}
                          onChange={(e) => setMtForm({ ...mtForm, is_active: e.target.checked })}
                          className="sr-only peer"
                        />
                        <div className="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-brand-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand-600"></div>
                        <span className="ms-2 text-sm text-slate-600">{mtForm.is_active ? 'Active' : 'Inactive'}</span>
                      </label>
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Keterangan</label>
                  <textarea
                    value={mtForm.notes}
                    onChange={(e) => setMtForm({ ...mtForm, notes: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    rows={2}
                    placeholder="Barang masuk ke showroom dari lokasi lain..."
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    {editingItem ? 'Update' : 'Create'}
                  </Button>
                  <Button type="button" variant="secondary" size="sm" onClick={resetForm}>
                    Cancel
                  </Button>
                </div>
              </form>
            )}

            {showForm && selectedType === 'location' && (
              <form onSubmit={handleLocSubmit} className="p-4 bg-slate-50 border-b border-slate-200 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Code</label>
                    <input
                      type="text"
                      value={locForm.code}
                      onChange={(e) => setLocForm({ ...locForm, code: e.target.value.toUpperCase().replace(/\s+/g, '_') })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 font-mono"
                      placeholder="RUANG_MEETING"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Name</label>
                    <input
                      type="text"
                      value={locForm.name}
                      onChange={(e) => setLocForm({ ...locForm, name: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                      placeholder="Ruang Meeting"
                      required
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Type</label>
                    <select
                      value={locForm.type}
                      onChange={(e) => setLocForm({ ...locForm, type: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    >
                      {LOCATION_TYPE_OPTIONS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Active</label>
                    <div className="flex items-center h-full pt-1">
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={locForm.is_active}
                          onChange={(e) => setLocForm({ ...locForm, is_active: e.target.checked })}
                          className="sr-only peer"
                        />
                        <div className="w-9 h-5 bg-slate-200 peer-focus:outline-none peer-focus:ring-2 peer-focus:ring-brand-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand-600"></div>
                        <span className="ms-2 text-sm text-slate-600">{locForm.is_active ? 'Active' : 'Inactive'}</span>
                      </label>
                    </div>
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1">Description</label>
                  <input
                    type="text"
                    value={locForm.description}
                    onChange={(e) => setLocForm({ ...locForm, description: e.target.value })}
                    className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    placeholder="Opsional..."
                  />
                </div>
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    {editingItem ? 'Update' : 'Create'}
                  </Button>
                  <Button type="button" variant="secondary" size="sm" onClick={resetForm}>
                    Cancel
                  </Button>
                </div>
              </form>
            )}

            {showForm && selectedType !== 'movement_type' && selectedType !== 'location' && (
              <form onSubmit={handleSubmit} className="p-4 bg-slate-50 border-b border-slate-200 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Name</label>
                    <input
                      type="text"
                      value={form.name}
                      onChange={(e) => setForm({ ...form, name: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Value</label>
                    <input
                      type="text"
                      value={form.value}
                      onChange={(e) => setForm({ ...form, value: e.target.value.toLowerCase().replace(/\s+/g, '_') })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
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
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Sort Order</label>
                    <input
                      type="number"
                      value={form.sort_order}
                      onChange={(e) => setForm({ ...form, sort_order: parseInt(e.target.value) || 0 })}
                      className="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button type="submit" size="sm">
                    {editingItem ? 'Update' : 'Create'}
                  </Button>
                  <Button type="button" variant="secondary" size="sm" onClick={resetForm}>
                    Cancel
                  </Button>
                </div>
              </form>
            )}

            <div className="p-4">
              {selectedType === 'movement_type' ? (
                mtLoading ? (
                  <LoadingSpinner />
                ) : mtItems.length === 0 ? (
                  <EmptyState icon={Settings} title="Belum ada data" description="Klik 'Tambah' untuk membuat tipe pergerakan baru." />
                ) : (
                  <div className="space-y-2">
                    {mtItems.map((item) => (
                      <div key={item.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-slate-200 transition-colors">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${item.is_active ? 'bg-emerald-500' : 'bg-slate-300'}`} />
                          <div>
                            <div className="text-sm font-medium text-slate-900">{item.name}</div>
                            <div className="text-xs text-slate-500 flex items-center gap-2">
                              <span className="font-mono bg-slate-200 px-1.5 py-0.5 rounded text-slate-600">{item.code}</span>
                              <span className={`px-1.5 py-0.5 rounded text-xs font-medium ${item.direction === 'IN' ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-100 text-rose-700'}`}>
                                {item.direction}
                              </span>
                            </div>
                            {item.notes && <div className="text-[11px] text-slate-400 mt-0.5 leading-tight">{item.notes}</div>}
                          </div>
                        </div>
                        <div className="flex items-center gap-1">
                          <Button variant="edit" size="xs" onClick={() => handleMtEdit(item)}><Edit size={14} /></Button>
                          <Button variant="delete" size="xs" onClick={() => setConfirmDelete(item)}><Trash2 size={14} /></Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )
              ) : selectedType === 'location' ? (
                locLoading ? (
                  <LoadingSpinner />
                ) : locItems.length === 0 ? (
                  <EmptyState icon={Settings} title="Belum ada data" description="Klik 'Tambah' untuk membuat lokasi baru." />
                ) : (
                  <div className="space-y-2">
                    {locItems.map((item) => (
                      <div key={item.id} className="flex items-center justify-between p-3 bg-slate-50 rounded-lg border border-slate-100 hover:border-slate-200 transition-colors">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${item.is_active ? 'bg-emerald-500' : 'bg-slate-300'}`} />
                          <div>
                            <div className="text-sm font-medium text-slate-900">{item.name}</div>
                            <div className="text-xs text-slate-500 flex items-center gap-2">
                              <span className="font-mono bg-slate-200 px-1.5 py-0.5 rounded text-slate-600">{item.code}</span>
                              <span className="px-1.5 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-700 capitalize">{item.type}</span>
                              {item.description && <span className="text-slate-400">— {item.description}</span>}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-1">
                          <Button variant="edit" size="xs" onClick={() => handleLocEdit(item)}><Edit size={14} /></Button>
                          <Button variant="delete" size="xs" onClick={() => setConfirmDelete(item)}><Trash2 size={14} /></Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )
              ) : (
                loading ? (
                  <LoadingSpinner />
                ) : items.length === 0 ? (
                  <EmptyState icon={Settings} title="Belum ada data" description='Klik "Seed Defaults" untuk populate.' />
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
                          <Button variant="edit" size="xs" onClick={() => handleEdit(item)}><Edit size={14} /></Button>
                          <Button variant="delete" size="xs" onClick={() => setConfirmDelete(item)}><Trash2 size={14} /></Button>
                        </div>
                      </div>
                    ))}
                  </div>
                )
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
        description={`Hapus "${confirmDelete?.name || confirmDelete?.code || confirmDelete?.value}"?`}
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
