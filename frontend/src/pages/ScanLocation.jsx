import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { MapPin, Package, ArrowLeft, Box, Hash } from 'lucide-react';

const ScanLocation = () => {
  const { code } = useParams();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`${import.meta.env.VITE_API_URL || 'https://api-csms.idekode.web.id/api/v1'}/showroom-v2/public/scan/${code}`)
      .then((res) => {
        if (!res.ok) throw new Error('Lokasi tidak ditemukan');
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, [code]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-10 w-10 border-4 border-indigo-500 border-t-transparent mx-auto mb-4" />
          <p className="text-sm text-slate-500">Memuat data lokasi...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50 flex items-center justify-center">
        <div className="text-center max-w-sm mx-auto px-4">
          <div className="w-16 h-16 bg-red-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <MapPin className="h-8 w-8 text-red-500" />
          </div>
          <h1 className="text-lg font-bold text-slate-900 mb-2">Lokasi Tidak Ditemukan</h1>
          <p className="text-sm text-slate-500 mb-4">{error}</p>
          <p className="text-xs text-slate-400">Kode: {code}</p>
        </div>
      </div>
    );
  }

  const { location, products, total_products, total_quantity } = data;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50">
      <div className="max-w-lg mx-auto px-4 py-6">
        {/* Header */}
        <div className="mb-6">
          <Link to="/dashboard" className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-700 mb-4">
            <ArrowLeft className="h-4 w-4" />
            Kembali
          </Link>

          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
            <div className="bg-gradient-to-r from-indigo-600 to-indigo-700 px-6 py-5">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                  <MapPin className="h-6 w-6 text-white" />
                </div>
                <div>
                  <p className="text-xs text-indigo-200 font-medium uppercase tracking-wide">{location.code}</p>
                  <h1 className="text-xl font-bold text-white">{location.name}</h1>
                </div>
              </div>
              {location.description && (
                <p className="text-sm text-indigo-100 mt-3">{location.description}</p>
              )}
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 divide-x divide-slate-100">
              <div className="px-5 py-4 text-center">
                <p className="text-2xl font-bold text-slate-900">{total_products}</p>
                <p className="text-xs text-slate-500 mt-0.5">Jenis Produk</p>
              </div>
              <div className="px-5 py-4 text-center">
                <p className="text-2xl font-bold text-slate-900">{total_quantity}</p>
                <p className="text-xs text-slate-500 mt-0.5">Total Qty</p>
              </div>
            </div>
          </div>
        </div>

        {/* Product List */}
        <div className="mb-6">
          <h2 className="text-sm font-semibold text-slate-700 mb-3 flex items-center gap-2">
            <Package className="h-4 w-4" />
            Daftar Produk di Lokasi Ini
          </h2>

          {products.length === 0 ? (
            <div className="bg-white rounded-xl border border-slate-200 p-8 text-center">
              <Box className="h-10 w-10 text-slate-300 mx-auto mb-3" />
              <p className="text-sm text-slate-500">Belum ada produk di lokasi ini</p>
            </div>
          ) : (
            <div className="space-y-2">
              {products.map((p, idx) => (
                <div key={idx} className="bg-white rounded-xl border border-slate-200 p-4 flex items-center gap-3 hover:border-indigo-200 transition-colors">
                  <div className="w-10 h-10 bg-indigo-50 rounded-lg flex items-center justify-center shrink-0">
                    <Package className="h-5 w-5 text-indigo-500" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-slate-900 truncate">{p.product_name}</p>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs font-mono text-slate-500">{p.sku}</span>
                      {p.sample_type && (
                        <span className="text-[10px] font-medium bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                          {p.sample_type}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <p className="text-lg font-bold text-slate-900">{p.quantity}</p>
                    <p className="text-[10px] text-slate-400 uppercase">qty</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Footer */}
        <p className="text-center text-xs text-slate-400">
          CSMS Showroom &middot; {location.code}
        </p>
      </div>
    </div>
  );
};

export default ScanLocation;
