import React, { useState, useEffect } from 'react';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import Badge from '../../../components/common/Badge';
import Modal from '../../../components/common/Modal';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import ConfirmDialog from '../../../components/common/ConfirmDialog';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import { showroomService } from '../../../api/services/showroomService';
import { LOCATION_TYPE_OPTIONS } from '../constants';
import { MapPin, Plus, Edit, Trash2, QrCode, Download, ExternalLink, Copy, Check } from 'lucide-react';

const LocationManagement = () => {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ code: '', name: '', type: 'internal', description: '', image_url: '' });
  const [confirmDelete, setConfirmDelete] = useState(null);
  const [qrModal, setQrModal] = useState(null);
  const [copied, setCopied] = useState(false);

  const fetchLocations = async () => {
    setLoading(true);
    try {
      const res = await showroomService.getAllLocations();
      if (res.success) setLocations(res.data);
    } catch { } finally { setLoading(false); }
  };

  useEffect(() => { fetchLocations(); }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editing) {
        await showroomService.updateLocation(editing.id, form);
      } else {
        await showroomService.createLocation(form);
      }
      setShowForm(false);
      setEditing(null);
      setForm({ code: '', name: '', type: 'internal', description: '', image_url: '' });
      fetchLocations();
    } catch { }
  };

  const handleEdit = (loc) => {
    setEditing(loc);
    setForm({ code: loc.code, name: loc.name, type: loc.type, description: loc.description || '', image_url: loc.image_url || '' });
    setShowForm(true);
  };

  const handleDelete = async () => {
    if (!confirmDelete) return;
    try {
      await showroomService.deleteLocation(confirmDelete.id);
      setConfirmDelete(null);
      fetchLocations();
    } catch { }
  };

  const getQRUrl = (code) => showroomService.getQRCodeUrl(code);

  const getScanUrl = (code) => `${window.location.origin}/scan/${code}`;

  const handleCopyLink = (code) => {
    navigator.clipboard.writeText(getScanUrl(code));
    setCopied(code);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Manajemen Lokasi"
        description="Kelola lokasi showroom beserta QR Code"
        actions={
          <Button onClick={() => { setShowForm(true); setEditing(null); setForm({ code: '', name: '', type: 'internal', description: '', image_url: '' }); }}>
            <Plus className="mr-1.5 h-4 w-4" />
            Tambah Lokasi
          </Button>
        }
      />

      {/* Form Modal */}
      <Modal isOpen={showForm} onClose={() => { setShowForm(false); setEditing(null); }} title={editing ? 'Edit Lokasi' : 'Tambah Lokasi'}>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <Input label="Kode Lokasi" placeholder="SHW-01" value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value.toUpperCase() })} required />
            <Select label="Tipe" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })} options={LOCATION_TYPE_OPTIONS} required />
          </div>
          <Input label="Nama Lokasi" placeholder="Showroom Utama" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          <Textarea label="Deskripsi" placeholder="Deskripsi lokasi (opsional)..." value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <Input label="URL Gambar" placeholder="https://..." value={form.image_url} onChange={(e) => setForm({ ...form, image_url: e.target.value })} />
          <div className="flex justify-end gap-2 pt-2">
            <Button type="button" variant="secondary" onClick={() => { setShowForm(false); setEditing(null); }}>Batal</Button>
            <Button type="submit">{editing ? 'Update' : 'Simpan'}</Button>
          </div>
        </form>
      </Modal>

      {/* QR Code Modal */}
      <Modal isOpen={!!qrModal} onClose={() => setQrModal(null)} title={`QR Code — ${qrModal?.code}`}>
        {qrModal && (
          <div className="flex flex-col items-center gap-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <img
                src={getQRUrl(qrModal.code)}
                alt={`QR ${qrModal.code}`}
                className="w-56 h-56"
              />
            </div>
            <p className="text-sm text-slate-600 text-center">{qrModal.name}</p>
            <p className="text-xs text-slate-400 font-mono">{getScanUrl(qrModal.code)}</p>

            <div className="flex gap-2 w-full">
              <Button
                variant="secondary"
                className="flex-1"
                onClick={() => handleCopyLink(qrModal.code)}
              >
                {copied === qrModal.code ? <Check className="mr-1.5 h-4 w-4 text-emerald-500" /> : <Copy className="mr-1.5 h-4 w-4" />}
                {copied === qrModal.code ? 'Tersalin!' : 'Salin Link'}
              </Button>
              <Button
                variant="secondary"
                className="flex-1"
                onClick={() => {
                  const a = document.createElement('a');
                  a.href = getQRUrl(qrModal.code);
                  a.download = `QR_${qrModal.code}.png`;
                  a.click();
                }}
              >
                <Download className="mr-1.5 h-4 w-4" />
                Download QR
              </Button>
              <Button
                className="flex-1"
                onClick={() => window.open(getScanUrl(qrModal.code), '_blank')}
              >
                <ExternalLink className="mr-1.5 h-4 w-4" />
                Buka Halaman
              </Button>
            </div>
          </div>
        )}
      </Modal>

      {/* Location List */}
      {loading ? (
        <LoadingSpinner />
      ) : locations.length === 0 ? (
        <EmptyState icon={MapPin} title="Belum ada lokasi" description="Klik 'Tambah Lokasi' untuk menambahkan lokasi baru." />
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
          {locations.map((loc) => (
            <div key={loc.id} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hover:border-indigo-200 hover:shadow-md transition-all">
              <div className="p-5">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2.5">
                    <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center">
                      <MapPin className="h-5 w-5 text-indigo-500" />
                    </div>
                    <div>
                      <p className="text-xs font-mono text-indigo-600">{loc.code}</p>
                      <h3 className="text-sm font-semibold text-slate-900">{loc.name}</h3>
                    </div>
                  </div>
                  <Badge variant={loc.is_active ? 'success' : 'default'}>
                    {loc.is_active ? 'Active' : 'Inactive'}
                  </Badge>
                </div>

                <div className="flex items-center gap-2 mb-2">
                  <span className="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full capitalize">{loc.type}</span>
                </div>

                {loc.description && (
                  <p className="text-xs text-slate-500 mb-3 line-clamp-2">{loc.description}</p>
                )}

                <div className="flex items-center gap-1.5 pt-3 border-t border-slate-100">
                  <Button variant="secondary" size="xs" onClick={() => setQrModal(loc)}>
                    <QrCode size={14} className="mr-1" />
                    QR Code
                  </Button>
                  <Button variant="edit" size="xs" onClick={() => handleEdit(loc)}>
                    <Edit size={14} />
                  </Button>
                  <Button variant="delete" size="xs" onClick={() => setConfirmDelete(loc)}>
                    <Trash2 size={14} />
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <ConfirmDialog
        isOpen={!!confirmDelete}
        onClose={() => setConfirmDelete(null)}
        onConfirm={handleDelete}
        title="Hapus Lokasi"
        description={`Hapus "${confirmDelete?.name}" (${confirmDelete?.code})? Lokasi yang masih memiliki stok tidak dapat dihapus.`}
        isDanger
      />
    </div>
  );
};

export default LocationManagement;
