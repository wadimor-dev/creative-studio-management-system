import React, { useState, useEffect, useCallback, useRef } from 'react';
import { showroomService } from '../../../api/services/showroomService';
import PageHeader from '../../../components/common/PageHeader';
import Button from '../../../components/common/Button';
import FilterTabs from '../../../components/common/FilterTabs';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import Modal from '../../../components/common/Modal';
import { QRCodeCanvas } from 'qrcode.react';
import { QrCode, Package, MapPin, Archive, Download, CheckCircle, XCircle, Search, Eye } from 'lucide-react';

const SOURCE_TABS = [
  { value: 'storage', label: 'Storage Management', icon: Archive },
  { value: 'location', label: 'Lokasi', icon: MapPin },
  { value: 'product', label: 'Produk', icon: Package },
];

const QRGenerator = () => {
  const [activeSource, setActiveSource] = useState('storage');
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState({});
  const [search, setSearch] = useState('');
  const [existingQREntities, setExistingQREntities] = useState([]);
  const [generatedQRs, setGeneratedQRs] = useState([]);
  const [generating, setGenerating] = useState(false);
  const qrCanvasRefs = useRef({});
  const [viewQR, setViewQR] = useState(null);

  const fetchItems = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      let res;
      if (activeSource === 'storage') {
        res = await showroomService.getStorages();
      } else if (activeSource === 'location') {
        res = await showroomService.getLocations();
      } else if (activeSource === 'product') {
        res = await showroomService.getProducts({ size: 100 });
      }
      if (res?.success !== false) {
        const data = res.data?.data || res.data || [];
        setItems(Array.isArray(data) ? data : []);
      } else {
        setItems([]);
      }
    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Gagal memuat data');
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [activeSource]);

  const fetchExistingQRs = useCallback(async () => {
    try {
      const res = await showroomService.getQREntities({ entity_type: activeSource });
      if (res?.success !== false) {
        setExistingQREntities(res.data?.data || res.data || []);
      }
    } catch (_) {}
  }, [activeSource]);

  useEffect(() => {
    fetchItems();
    fetchExistingQRs();
    setSelected({});
    setGeneratedQRs([]);
  }, [fetchItems, fetchExistingQRs]);

  const entityHasQR = (entityId) => {
    return existingQREntities.some(qr => qr.entity_id === entityId && qr.is_active !== false);
  };

  const getExistingQR = (entityId) => {
    return existingQREntities.find(qr => qr.entity_id === entityId && qr.is_active !== false);
  };

  const toggleSelect = (id) => {
    setSelected(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const selectAll = () => {
    const filtered = filteredItems;
    if (filtered.length === 0) return;
    const allSelected = filtered.every(item => selected[item.id]);
    const newSelected = { ...selected };
    filtered.forEach(item => { newSelected[item.id] = !allSelected; });
    setSelected(newSelected);
  };

  const generateQR = async () => {
    const selectedIds = Object.entries(selected).filter(([, v]) => v).map(([k]) => parseInt(k));
    if (selectedIds.length === 0) return;
    setGenerating(true);
    const results = [];
    for (const entityId of selectedIds) {
      const existing = getExistingQR(entityId);
      if (existing) {
        results.push({ entityId, entityType: activeSource, status: 'exists', token: existing.token, qr: existing });
        continue;
      }
      try {
        const res = await showroomService.createQREntity({
          entity_type: activeSource,
          entity_id: entityId,
          label: items.find(i => i.id === entityId)?.display_name || items.find(i => i.id === entityId)?.name || String(entityId),
        });
        if (res?.success !== false) {
          const qr = res.data?.data || res.data;
          results.push({ entityId, entityType: activeSource, status: 'created', token: qr.token, qr });
        } else {
          results.push({ entityId, entityType: activeSource, status: 'error', error: res.message || 'Gagal' });
        }
      } catch (err) {
        results.push({ entityId, entityType: activeSource, status: 'error', error: err.response?.data?.message || err.message });
      }
    }
    setGeneratedQRs(results);
    await fetchExistingQRs();
    setGenerating(false);
  };

  const getItemDisplayName = (item) => {
    return item.display_name || item.name || `ID: ${item.id}`;
  };

  const getItemCode = (item) => {
    return item.code || item.sku || `#${item.id}`;
  };

  const filteredItems = items.filter(item => {
    if (!search.trim()) return true;
    const q = search.toLowerCase();
    const name = (getItemDisplayName(item) || '').toLowerCase();
    const code = (getItemCode(item) || '').toLowerCase();
    return name.includes(q) || code.includes(q);
  });

  const selectedCount = Object.values(selected).filter(Boolean).length;

  return (
    <div className="space-y-6">
      <PageHeader title="QR Code Generator" description="Buat dan kelola QR Code untuk storage, lokasi, dan produk" />

      <FilterTabs tabs={SOURCE_TABS} active={activeSource} onChange={(v) => { setActiveSource(v); setGeneratedQRs([]); }} />

      <div className="flex items-center gap-3">
        <div className="relative flex-1 max-w-xs">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Cari..."
            className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <Button size="sm" variant="outline" onClick={selectAll}>
          {filteredItems.length > 0 && filteredItems.every(item => selected[item.id]) ? 'Unselect All' : 'Select All'}
        </Button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">{error}</div>
      )}

      {loading ? (
        <LoadingSpinner />
      ) : filteredItems.length === 0 ? (
        <div className="text-center py-12 text-slate-400">
          <Archive size={48} className="mx-auto mb-3 opacity-30" />
          <p className="font-medium">Tidak ada data</p>
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="max-h-[420px] overflow-y-auto">
            <table className="w-full text-sm">
              <thead className="bg-slate-50 sticky top-0">
                <tr>
                  <th className="w-10 px-4 py-3 text-left"></th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-700">Nama</th>
                  <th className="px-4 py-3 text-left font-semibold text-slate-700">Kode</th>
                  <th className="px-4 py-3 text-center font-semibold text-slate-700">QR Status</th>
                  <th className="px-4 py-3 text-center font-semibold text-slate-700">Aksi</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredItems.map(item => {
                  const hasQR = entityHasQR(item.id);
                  const existing = getExistingQR(item.id);
                  return (
                    <tr key={item.id} className={`hover:bg-slate-50 transition-colors ${selected[item.id] ? 'bg-indigo-50/50' : ''}`}>
                      <td className="px-4 py-2.5">
                        <input
                          type="checkbox"
                          checked={!!selected[item.id]}
                          onChange={() => toggleSelect(item.id)}
                          className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                        />
                      </td>
                      <td className="px-4 py-2.5 font-medium text-slate-800">{getItemDisplayName(item)}</td>
                      <td className="px-4 py-2.5 text-slate-500 font-mono text-xs">{getItemCode(item)}</td>
                      <td className="px-4 py-2.5 text-center">
                        {hasQR ? (
                          <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                            <CheckCircle size={12} /> Ada
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1 text-xs font-medium text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">
                            <XCircle size={12} /> Belum
                          </span>
                        )}
                      </td>
                      <td className="px-4 py-2.5 text-center">
                        {hasQR && existing ? (
                          <div className="flex items-center justify-center gap-1">
                            <button
                              onClick={() => setViewQR({ token: existing.token, name: getItemDisplayName(item), code: getItemCode(item) })}
                              className="p-1.5 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
                              title="Lihat QR"
                            >
                              <Eye size={16} />
                            </button>
                            <button
                              onClick={() => {
                                const canvas = qrCanvasRefs.current[existing.token];
                                if (canvas) {
                                  const url = canvas.toDataURL('image/png');
                                  const a = document.createElement('a');
                                  a.href = url;
                                  a.download = `QR_${getItemCode(item)}.png`;
                                  document.body.appendChild(a);
                                  a.click();
                                  document.body.removeChild(a);
                                }
                              }}
                              className="p-1.5 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                              title="Download QR"
                            >
                              <Download size={16} />
                            </button>
                          </div>
                        ) : (
                          <span className="text-xs text-slate-300">-</span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="flex items-center justify-between">
        <span className="text-sm text-slate-500">
          {selectedCount} dari {filteredItems.length} dipilih
        </span>
        <Button onClick={generateQR} disabled={selectedCount === 0 || generating} isLoading={generating} icon={<QrCode size={16} />}>
          {generating ? 'Memproses...' : `Generate QR (${selectedCount})`}
        </Button>
      </div>

      {generatedQRs.length > 0 && (
        <div>
          <h3 className="text-sm font-semibold text-slate-700 mb-3">Hasil Generate QR</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {generatedQRs.map((result, idx) => {
              const item = items.find(i => i.id === result.entityId);
              const name = getItemDisplayName(item || {});
              const code = getItemCode(item || {});
              return (
                <div key={idx} className="bg-white rounded-xl border border-slate-200 p-4 flex flex-col items-center text-center">
                  {result.status === 'created' || result.status === 'exists' ? (
                    <>
                      <div className="bg-white p-2 rounded-lg mb-2 border border-slate-100">
                        <QRCodeCanvas
                          ref={(el) => { qrCanvasRefs.current[result.token] = el; }}
                          value={result.token}
                          size={128}
                          bgColor="#ffffff"
                          fgColor="#1e293b"
                          level="H"
                          includeMargin={false}
                        />
                      </div>
                      <p className="text-sm font-semibold text-slate-800 leading-tight">{name}</p>
                      <p className="text-[10px] text-slate-400 font-mono mt-0.5 truncate max-w-full">{code}</p>
                      <p className="text-[10px] text-slate-400 font-mono truncate max-w-full">{result.token}</p>
                      {result.status === 'exists' && (
                        <span className="text-[10px] text-amber-600 mt-1">Sudah ada sebelumnya</span>
                      )}
                      <button
                        onClick={() => {
                          const canvas = qrCanvasRefs.current[result.token];
                          if (canvas) {
                            const url = canvas.toDataURL('image/png');
                            const a = document.createElement('a');
                            a.href = url;
                            a.download = `QR_${code}.png`;
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                          }
                        }}
                        className="mt-2 inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 font-medium"
                      >
                        <Download size={12} /> Download
                      </button>
                    </>
                  ) : (
                    <div className="py-6 text-red-500 text-sm">{result.error || 'Gagal'}</div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}

      <Modal isOpen={!!viewQR} onClose={() => setViewQR(null)} title="QR Code">
        {viewQR && (
          <div className="flex flex-col items-center py-4 space-y-4">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <QRCodeCanvas
                value={viewQR.token}
                size={256}
                bgColor="#ffffff"
                fgColor="#1e293b"
                level="H"
                includeMargin={false}
              />
            </div>
            <div className="text-center">
              <p className="font-semibold text-slate-800">{viewQR.name}</p>
              <p className="text-xs text-slate-500 font-mono mt-1">{viewQR.code}</p>
              <p className="text-xs text-slate-400 font-mono mt-0.5">{viewQR.token}</p>
            </div>
            <button
              onClick={() => {
                const canvas = document.querySelector(`canvas`);
                if (canvas) {
                  const url = canvas.toDataURL('image/png');
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = `QR_${viewQR.code}.png`;
                  document.body.appendChild(a);
                  a.click();
                  document.body.removeChild(a);
                }
              }}
              className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg text-sm font-medium hover:bg-indigo-700 transition-colors"
            >
              <Download size={16} /> Download QR
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default QRGenerator;
