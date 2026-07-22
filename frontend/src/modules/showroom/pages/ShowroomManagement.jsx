import React, { useState, useEffect, useCallback, useRef } from 'react';
import { showroomService } from '../../../api/services/showroomService';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import Modal from '../../../components/common/Modal';
import DataTable from '../../../components/common/DataTable';
import Badge from '../../../components/common/Badge';
import SearchableSelect from '../../../components/common/SearchableSelect';
import { Search, Plus, Download, FileText, Trash2, Layers, Archive, ArrowLeft } from 'lucide-react';

const SAMPLE_TYPES = [
  { value: '', label: 'Semua Tipe' },
  { value: 'Display', label: 'Display' },
  { value: 'Photography', label: 'Fotografi' },
  { value: 'Premium', label: 'Premium' },
  { value: 'Archive', label: 'Arsip' },
];

const MOVEMENT_DIRECTIONS = [
  { value: '', label: 'Semua Pergerakan' },
  { value: 'IN', label: 'Masuk (IN)' },
  { value: 'OUT', label: 'Keluar (OUT)' },
];

const REPORT_PERIODS = [
  { value: 'daily', label: 'Harian' },
  { value: 'weekly', label: 'Mingguan' },
  { value: 'monthly', label: 'Bulanan' },
];

const ShowroomManagement = () => {
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const perPage = 25;

  const [search, setSearch] = useState('');
  const [filterStorage, setFilterStorage] = useState('');
  const [filterSampleType, setFilterSampleType] = useState('');
  const [filterMovement, setFilterMovement] = useState('');

  const [storageLocations, setStorageLocations] = useState([]);
  const [allProducts, setAllProducts] = useState([]);
  const [allLocations, setAllLocations] = useState([]);
  const [movementTypes, setMovementTypes] = useState([]);

  const [addModal, setAddModal] = useState(false);
  const [addProduct, setAddProduct] = useState('');
  const [addStorage, setAddStorage] = useState('');
  const [addSampleType, setAddSampleType] = useState('Display');
  const [addQty, setAddQty] = useState(1);
  const [addMovementType, setAddMovementType] = useState('SHOWROOM_IN');
  const [addFromLocation, setAddFromLocation] = useState('');
  const [addToLocation, setAddToLocation] = useState('');
  const [addNotes, setAddNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const [editModal, setEditModal] = useState(false);
  const [editItem, setEditItem] = useState(null);
  const [editQty, setEditQty] = useState(1);

  const [deleteModal, setDeleteModal] = useState(false);
  const [deleteItem, setDeleteItem] = useState(null);

  const [reportModal, setReportModal] = useState(false);
  const [reportPeriod, setReportPeriod] = useState('daily');
  const [reportDate, setReportDate] = useState(new Date().toISOString().split('T')[0]);
  const [reportLoading, setReportLoading] = useState(false);
  const [reportData, setReportData] = useState(null);

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const params = { page, per_page: perPage };
      if (search.trim()) params.search = search.trim();
      if (filterStorage) params.storage_location_id = filterStorage;
      if (filterSampleType) params.sample_type = filterSampleType;
      const res = await showroomService.getManageProducts(params);
      if (res.success) {
        let filtered = res.data.items || [];
        if (filterMovement) {
          filtered = filtered.filter(i => i.movement && i.movement.direction === filterMovement);
        }
        setItems(filtered);
        setTotal(res.data.total || 0);
        setTotalPages(res.data.total_pages || 0);
      }
    } catch (_) {} finally {
      setLoading(false);
    }
  }, [page, search, filterStorage, filterSampleType, filterMovement]);

  const fetchStorageLocations = useCallback(async () => {
    try {
      const res = await showroomService.getStorageLocations({});
      if (res.success) setStorageLocations(res.data || []);
    } catch (_) {}
  }, []);

  const fetchAllProducts = useCallback(async () => {
    try {
      const res = await showroomService.getProducts();
      if (res.success) setAllProducts(res.data || []);
    } catch (_) {}
  }, []);

  const fetchLocations = useCallback(async () => {
    try {
      const res = await showroomService.getLocations();
      if (res.success) setAllLocations(res.data || []);
    } catch (_) {}
  }, []);

  const fetchMovementTypes = useCallback(async () => {
    try {
      const res = await showroomService.getMovementTypes();
      if (res.success) setMovementTypes(res.data || []);
    } catch (_) {}
  }, []);

  useEffect(() => { fetchData(); }, [fetchData]);
  useEffect(() => { fetchStorageLocations(); fetchAllProducts(); fetchLocations(); fetchMovementTypes(); }, []);

  useEffect(() => { setPage(1); }, [search, filterStorage, filterSampleType, filterMovement]);

  const handleSearch = (e) => {
    e.preventDefault();
    setPage(1);
    fetchData();
  };

  const storageOptions = storageLocations.map(s => ({ value: String(s.id), label: s.name, subLabel: s.code }));
  const productOptions = allProducts.map(p => ({
    value: String(p.id),
    label: p.display_name || p.name,
    subLabel: p.sku,
  }));
  const locationOptions = allLocations.map(l => ({ value: String(l.id), label: l.name, subLabel: l.code }));

  const openAddModal = () => {
    setAddProduct('');
    setAddStorage('');
    setAddSampleType('Display');
    setAddQty(1);
    setAddMovementType('SHOWROOM_IN');
    setAddFromLocation('');
    setAddToLocation('');
    setAddNotes('');
    setAddModal(true);
  };

  const handleAddProduct = async () => {
    if (!addProduct || !addStorage) return;
    setSubmitting(true);
    try {
      const mt = movementTypes.find(t => t.value === addMovementType);
      const direction = mt ? mt.direction : 'IN';
      const params = {
        product_id: addProduct,
        storage_location_id: addStorage,
        movement_type: addMovementType,
        sample_type: addSampleType,
        quantity: addQty,
      };
      if (direction === 'IN' && addFromLocation) params.from_location_id = Number(addFromLocation);
      if (direction === 'OUT' && addToLocation) params.to_location_id = Number(addToLocation);
      if (addNotes.trim()) params.notes = addNotes.trim();
      const res = await showroomService.addManageProduct(params);
      if (res.success) {
        setAddModal(false);
        fetchData();
      }
    } finally {
      setSubmitting(false);
    }
  };

  const openEditModal = (item) => {
    setEditItem(item);
    setEditQty(1);
    setEditModal(true);
  };

  const handleEditStock = async () => {
    if (!editItem || editQty <= 0) return;
    setSubmitting(true);
    try {
      await showroomService.addManageProduct({
        product_id: editItem.product_id,
        storage_location_id: editItem.storage_location?.id || undefined,
        movement_type: 'SHOWROOM_IN',
        sample_type: editItem.sample_type,
        quantity: editQty,
        notes: 'Adjustment by management',
      });
      setEditModal(false);
      setEditItem(null);
      fetchData();
    } finally {
      setSubmitting(false);
    }
  };

  const openDeleteModal = (item) => {
    setDeleteItem(item);
    setDeleteModal(true);
  };

  const handleDeleteStock = async () => {
    if (!deleteItem) return;
    setSubmitting(true);
    try {
      await showroomService.removeManageProduct(deleteItem.id, { quantity: deleteItem.quantity });
      setDeleteModal(false);
      setDeleteItem(null);
      fetchData();
    } finally {
      setSubmitting(false);
    }
  };

  const openReportModal = () => {
    setReportPeriod('daily');
    setReportDate(new Date().toISOString().split('T')[0]);
    setReportData(null);
    setReportModal(true);
  };

  const handleGenerateReport = async () => {
    setReportLoading(true);
    try {
      const params = { period: reportPeriod };
      if (reportDate) {
        const d = new Date(reportDate);
        if (reportPeriod === 'daily') {
          params.start_date = reportDate;
          params.end_date = reportDate;
        } else if (reportPeriod === 'weekly') {
          const start = new Date(d);
          start.setDate(d.getDate() - d.getDay());
          params.start_date = start.toISOString().split('T')[0];
          const end = new Date(start);
          end.setDate(start.getDate() + 6);
          params.end_date = end.toISOString().split('T')[0];
        } else {
          params.start_date = reportDate.split('-').slice(0, 2).join('-') + '-01';
          const lastDay = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
          params.end_date = reportDate.split('-').slice(0, 2).join('-') + '-' + String(lastDay).padStart(2, '0');
        }
      }
      const res = await showroomService.getManageReport(params);
      if (res.success) setReportData(res.data);
    } finally {
      setReportLoading(false);
    }
  };

  const exportCSV = () => {
    const headers = ['Nama Produk', 'SKU', 'Kategori', 'Motif', 'Sub Motif', 'Penyimpanan', 'Tipe Sample', 'Quantity', 'Pergerakan', 'Dari Lokasi', 'Ke Lokasi', 'Tgl Pergerakan'];
    const rows = items.map(i => {
      const mov = i.movement || {};
      return [
        i.product_name || '',
        i.sku || '',
        i.category?.name || '',
        i.motif?.name || '',
        i.sub_motif?.name || '',
        i.storage_location?.name || '',
        i.sample_type || '',
        i.quantity,
        mov.direction || '',
        mov.from_location?.name || '',
        mov.to_location?.name || '',
        mov.date ? new Date(mov.date).toLocaleDateString('id-ID') : '',
      ];
    });
    const csv = [headers.join(','), ...rows.map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `showroom_management_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const exportReportCSV = () => {
    if (!reportData) return;
    const headers = ['Pergerakan', 'Nama Produk', 'SKU', 'Quantity', 'Tipe Sample', 'Dari', 'Ke', 'Catatan', 'Tanggal'];
    const rows = (reportData.movements || []).map(m => [
      m.direction || m.movement_type || '',
      m.product_name || '',
      m.product_sku || '',
      m.quantity || 0,
      m.sample_type || '',
      m.from_location || '',
      m.to_location || '',
      m.notes || '',
      m.date ? new Date(m.date).toLocaleDateString('id-ID') : '',
    ]);
    const csv = [headers.join(','), ...rows.map(r => r.map(v => `"${String(v).replace(/"/g, '""')}"`).join(','))].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `showroom_report_${reportData?.period?.start || new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const columns = [
    {
      header: 'Produk',
      accessor: 'product_name',
      cell: (row) => (
        <div className="flex flex-col">
          <span className="font-semibold text-slate-800">{row.product_name}</span>
          <span className="text-xs font-mono text-slate-400">{row.sku}</span>
        </div>
      ),
    },
    {
      header: 'Kategori',
      cellClassName: 'max-w-[140px]',
      cell: (row) => (
        <div className="flex flex-col gap-0.5 text-xs">
          {row.category && <span className="flex items-center gap-1"><Layers size={10} /> {row.category.name}</span>}
          {row.motif && <span className="text-slate-500 ml-3.5">{row.motif.name}</span>}
          {row.sub_motif && <span className="text-slate-400 ml-3.5">{row.sub_motif.name}</span>}
          {row.variant && <span className="text-slate-400 ml-3.5 italic">{row.variant}</span>}
        </div>
      ),
    },
    {
      header: 'Penyimpanan',
      cell: (row) => (
        <div className="flex flex-col">
          {row.storage_location && <span className="flex items-center gap-1 text-xs"><Archive size={10} /> {row.storage_location.name}</span>}
          {!row.storage_location && <span className="text-xs text-slate-400">-</span>}
        </div>
      ),
    },
    {
      header: 'Tipe',
      cell: (row) => <span className="text-xs font-medium">{row.sample_type || '-'}</span>,
    },
    {
      header: 'Qty',
      cellClassName: 'text-center font-bold',
      cell: (row) => <span className="text-lg font-bold text-slate-800">{row.quantity}</span>,
    },
    {
      header: 'Pergerakan',
      cell: (row) => {
        const mov = row.movement;
        if (!mov) return <span className="text-xs text-slate-300">-</span>;
        const isIN = mov.direction === 'IN';
        const typeLabel = mov.type || '';
        const locName = isIN ? (mov.from_location?.name || '') : (mov.to_location?.name || '');
        return (
          <div className="flex flex-col gap-0.5">
            <div className="flex items-center gap-1">
              {isIN ? (
                <Badge variant="success" size="sm">
                  <div className="flex items-center gap-0.5">
                    <ArrowLeft size={10} /> IN
                  </div>
                </Badge>
              ) : (
                <Badge variant="danger" size="sm">
                  <div className="flex items-center gap-0.5">
                    <ArrowUpRight size={10} /> OUT
                  </div>
                </Badge>
              )}
            </div>
            {locName && (
              <span className="text-[10px] text-slate-500 truncate max-w-[120px]" title={`${typeLabel}: ${locName}`}>{locName}</span>
            )}
          </div>
        );
      },
    },
    {
      header: 'Aksi',
      cellClassName: 'text-right',
      cell: (row) => (
        <div className="flex items-center justify-end gap-1">
          <button onClick={() => openEditModal(row)} className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors" title="Tambah Stok">
            <Plus size={15} />
          </button>
          <button onClick={() => openDeleteModal(row)} className="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors" title="Hapus">
            <Trash2 size={15} />
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-4">
      <PageHeader
        title="Showroom Management"
        description="Kelola produk di showroom, pantau stok per penyimpanan dan pergerakan barang"
      />

      <div className="bg-white rounded-xl border border-slate-200 p-4 space-y-4">
        <form onSubmit={handleSearch} className="flex flex-wrap items-end gap-3">
          <div className="min-w-[200px] flex-1">
            <label className="text-xs font-semibold text-slate-600 block mb-1">Cari Produk</label>
            <div className="relative">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Nama atau SKU..."
                className="w-full pl-8 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              />
              <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-slate-400" />
            </div>
          </div>
          <div className="min-w-[160px]">
            <label className="text-xs font-semibold text-slate-600 block mb-1">Penyimpanan</label>
            <select value={filterStorage} onChange={(e) => setFilterStorage(e.target.value)} className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              <option value="">Semua Rak</option>
              {storageLocations.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </select>
          </div>
          <div className="min-w-[140px]">
            <label className="text-xs font-semibold text-slate-600 block mb-1">Tipe Sample</label>
            <select value={filterSampleType} onChange={(e) => setFilterSampleType(e.target.value)} className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              {SAMPLE_TYPES.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>
          <div className="min-w-[140px]">
            <label className="text-xs font-semibold text-slate-600 block mb-1">Pergerakan</label>
            <select value={filterMovement} onChange={(e) => setFilterMovement(e.target.value)} className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              {MOVEMENT_DIRECTIONS.map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>
          <Button variant="primary" size="sm" type="submit" className="mb-0">
            <Search size={14} /> Cari
          </Button>
        </form>
        <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
          <Button variant="primary" size="sm" onClick={openAddModal}>
            <Plus size={15} /> Tambah Produk
          </Button>
          <Button variant="outline" size="sm" onClick={exportCSV} disabled={items.length === 0}>
            <Download size={15} /> Export CSV
          </Button>
          <Button variant="outline" size="sm" onClick={openReportModal}>
            <FileText size={15} /> Laporan
          </Button>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <div className="px-4 py-3 border-b border-slate-100 flex items-center justify-between">
          <span className="text-sm font-semibold text-slate-700">Daftar Produk ({total})</span>
        </div>
        <DataTable
          columns={columns}
          data={items}
          isLoading={loading}
          emptyStateTitle="Belum ada produk"
          emptyStateDescription="Tambahkan produk ke showroom menggunakan tombol Tambah Produk"
          pagination={totalPages > 1 ? (
            <div className="flex items-center justify-center gap-2 py-2">
              <button onClick={() => setPage(p => Math.max(1, p - 1))} disabled={page <= 1} className="px-3 py-1 text-sm border border-slate-300 rounded-lg disabled:opacity-30 hover:bg-slate-50">Prev</button>
              <span className="text-sm text-slate-600">Halaman {page} dari {totalPages}</span>
              <button onClick={() => setPage(p => Math.min(totalPages, p + 1))} disabled={page >= totalPages} className="px-3 py-1 text-sm border border-slate-300 rounded-lg disabled:opacity-30 hover:bg-slate-50">Next</button>
            </div>
          ) : null}
        />
      </div>

      <Modal isOpen={addModal} onClose={() => setAddModal(false)} title="Tambah Produk / Pergerakan">
        <div className="space-y-4">
          <div>
            <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Produk</label>
            <SearchableSelect
              options={productOptions}
              value={addProduct}
              onChange={(v) => setAddProduct(v)}
              placeholder="Cari produk..."
            />
          </div>

          <div className="flex gap-3">
            <div className="flex-1">
              <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Penyimpanan</label>
              <SearchableSelect
                options={storageOptions}
                value={addStorage}
                onChange={(v) => setAddStorage(v)}
                placeholder="Pilih rak atau laci..."
              />
            </div>
            <div className="w-28">
              <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Qty</label>
              <input type="number" min="1" value={addQty} onChange={(e) => setAddQty(Math.max(1, parseInt(e.target.value) || 1))} className="w-full p-2 border border-slate-300 rounded-lg text-lg font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
            </div>
          </div>

          <div>
            <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Tipe Sample</label>
            <select value={addSampleType} onChange={(e) => setAddSampleType(e.target.value)} className="w-full p-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20">
              {SAMPLE_TYPES.filter(t => t.value).map(t => <option key={t.value} value={t.value}>{t.label}</option>)}
            </select>
          </div>

          <div className="group relative">
            <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Tipe Pergerakan</label>
            <select
              value={addMovementType}
              onChange={(e) => setAddMovementType(e.target.value)}
              className="w-full p-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
            >
              {movementTypes.map(mt => <option key={mt.value} value={mt.value}>{mt.label} ({mt.direction})</option>)}
            </select>
            {(() => {
              const active = movementTypes.find(mt => mt.value === addMovementType);
              return active?.notes ? (
                <div className="absolute top-full left-0 right-0 z-10 mt-1 px-3 py-2 bg-slate-800 text-white text-[11px] leading-tight rounded-lg shadow-lg opacity-0 group-hover:opacity-100 group-focus-within:opacity-100 transition-opacity duration-150 pointer-events-none">
                  {active.notes}
                </div>
              ) : null;
            })()}
          </div>

          {(() => {
            const mt = movementTypes.find(t => t.value === addMovementType);
            const dir = mt ? mt.direction : 'IN';
            return dir === 'IN' ? (
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Dari Lokasi</label>
                <SearchableSelect
                  options={locationOptions}
                  value={addFromLocation}
                  onChange={(v) => setAddFromLocation(v)}
                  placeholder="Pilih lokasi asal..."
                />
              </div>
            ) : (
              <div>
                <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Ke Lokasi</label>
                <SearchableSelect
                  options={locationOptions}
                  value={addToLocation}
                  onChange={(v) => setAddToLocation(v)}
                  placeholder="Pilih lokasi tujuan..."
                />
              </div>
            );
          })()}

          <div>
            <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Catatan</label>
            <input type="text" value={addNotes} onChange={(e) => setAddNotes(e.target.value)} placeholder="Opsional..." className="w-full p-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
          </div>

          {(() => {
            const mt = movementTypes.find(t => t.value === addMovementType);
            const dir = mt ? mt.direction : 'IN';
            return dir === 'OUT' && addStorage && addProduct ? (
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-700">
                Produk akan DIKELUARKAN dari stok showroom. Pastikan stok tersedia.
              </div>
            ) : null;
          })()}

          <div className="flex gap-2 pt-2 border-t border-slate-100">
            <Button variant="outline" className="flex-1" onClick={() => setAddModal(false)}>Batal</Button>
            <Button
              variant="primary"
              className="flex-1"
              onClick={handleAddProduct}
              isLoading={submitting}
              disabled={!addProduct || !addStorage}
            >
              {(() => {
                const mt = movementTypes.find(t => t.value === addMovementType);
                const dir = mt ? mt.direction : 'IN';
                return dir === 'IN' ? 'Masukkan Stok' : 'Keluarkan Stok';
              })()}
            </Button>
          </div>
        </div>
      </Modal>

      <Modal isOpen={editModal} onClose={() => setEditModal(false)} title="Tambah Stok Produk">
        {editItem && (
          <div className="space-y-4">
            <div className="bg-indigo-50 p-3 rounded-lg text-sm">
              <p className="font-semibold text-indigo-800">{editItem.product_name}</p>
              <p className="text-xs text-indigo-500 mt-0.5">{editItem.sku} | {editItem.storage_location?.name || '-'} | {editItem.sample_type} | Stok: <strong>{editItem.quantity}</strong></p>
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Tambah Jumlah</label>
              <input type="number" min="1" value={editQty} onChange={(e) => setEditQty(Math.max(1, parseInt(e.target.value) || 1))} className="w-full p-2 border border-slate-300 rounded-lg text-lg font-bold focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
            </div>
            <div className="flex gap-2 pt-2 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={() => setEditModal(false)}>Batal</Button>
              <Button variant="primary" className="flex-1" onClick={handleEditStock} isLoading={submitting}>Tambah Stok</Button>
            </div>
          </div>
        )}
      </Modal>

      <Modal isOpen={deleteModal} onClose={() => setDeleteModal(false)} title="Hapus Produk">
        {deleteItem && (
          <div className="space-y-4">
            <div className="bg-rose-50 p-3 rounded-lg text-sm">
              <p>Hapus <strong>{deleteItem.product_name}</strong> dari <strong>{deleteItem.storage_location?.name || 'penyimpanan'}</strong>?</p>
              <p className="text-xs text-rose-500 mt-1">Stok saat ini: <strong>{deleteItem.quantity}</strong> | Tipe: {deleteItem.sample_type}</p>
              <p className="text-xs text-rose-400 mt-1">Aksi ini akan mengeluarkan seluruh stok produk ini.</p>
            </div>
            <div className="flex gap-2 pt-2 border-t border-slate-100">
              <Button variant="outline" className="flex-1" onClick={() => setDeleteModal(false)}>Batal</Button>
              <Button variant="danger" className="flex-1" onClick={handleDeleteStock} isLoading={submitting}>Hapus</Button>
            </div>
          </div>
        )}
      </Modal>

      <Modal isOpen={reportModal} onClose={() => setReportModal(false)} title="Laporan Showroom" maxWidth="max-w-3xl">
        <div className="space-y-4">
          <div className="flex gap-3 items-end">
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Periode</label>
              <div className="flex gap-2">
                {REPORT_PERIODS.map(p => (
                  <button
                    key={p.value}
                    onClick={() => setReportPeriod(p.value)}
                    className={`px-3 py-1.5 text-sm rounded-lg border transition-colors ${reportPeriod === p.value ? 'bg-indigo-600 text-white border-indigo-600' : 'border-slate-300 text-slate-600 hover:bg-slate-50'}`}
                  >
                    {p.label}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 uppercase block mb-1">Tanggal Referensi</label>
              <input type="date" value={reportDate} onChange={(e) => setReportDate(e.target.value)} className="px-3 py-1.5 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
            </div>
            <Button variant="primary" size="sm" onClick={handleGenerateReport} isLoading={reportLoading}>
              <Search size={14} /> Generate
            </Button>
          </div>

          {reportData && (
            <div className="space-y-4">
              <div className="bg-slate-50 rounded-lg p-4 grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
                <div>
                  <span className="text-xs text-slate-500 block">Total Produk</span>
                  <span className="text-2xl font-bold text-slate-800">{reportData.summary?.total_items || 0}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Total Qty</span>
                  <span className="text-2xl font-bold text-slate-800">{reportData.summary?.total_quantity || 0}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Masuk ({reportData.summary?.in_count || 0}x)</span>
                  <span className="text-2xl font-bold text-emerald-600">+{reportData.summary?.in_qty || 0}</span>
                </div>
                <div>
                  <span className="text-xs text-slate-500 block">Keluar ({reportData.summary?.out_count || 0}x)</span>
                  <span className="text-2xl font-bold text-rose-600">-{reportData.summary?.out_qty || 0}</span>
                </div>
              </div>

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-semibold text-slate-700">
                    Riwayat Pergerakan ({reportData.period?.start} s/d {reportData.period?.end})
                  </span>
                  <Button variant="outline" size="xs" onClick={exportReportCSV}>
                    <Download size={12} /> Export CSV
                  </Button>
                </div>
                <div className="max-h-60 overflow-y-auto border border-slate-200 rounded-lg">
                  <table className="w-full text-sm">
                    <thead className="bg-slate-50 sticky top-0">
                      <tr>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600">Arah</th>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600">Produk</th>
                        <th className="px-3 py-2 text-center text-xs font-semibold text-slate-600">Qty</th>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600">Dari/Ke</th>
                        <th className="px-3 py-2 text-left text-xs font-semibold text-slate-600">Tanggal</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {(reportData.movements || []).length === 0 ? (
                        <tr><td colSpan={5} className="px-3 py-8 text-center text-slate-400">Tidak ada pergerakan</td></tr>
                      ) : (
                        reportData.movements.map((m, i) => (
                          <tr key={i} className="hover:bg-slate-50">
                            <td className="px-3 py-2">
                              {m.direction === 'IN' ? (
                                <Badge variant="success" size="sm"><ArrowLeft size={10} /> IN</Badge>
                              ) : (
                                <Badge variant="danger" size="sm"><ArrowUpRight size={10} /> OUT</Badge>
                              )}
                            </td>
                            <td className="px-3 py-2">
                              <span className="font-semibold text-slate-700">{m.product_name}</span>
                              <span className="text-xs text-slate-400 ml-1 font-mono">{m.product_sku}</span>
                            </td>
                            <td className="px-3 py-2 text-center font-bold">{m.quantity}</td>
                            <td className="px-3 py-2 text-xs text-slate-500">{m.notes || m.from_location || m.to_location || '-'}</td>
                            <td className="px-3 py-2 text-xs text-slate-400">{m.date ? new Date(m.date).toLocaleDateString('id-ID') : '-'}</td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </Modal>
    </div>
  );
};

export default ShowroomManagement;
