import React, { useRef, useState } from 'react';
import * as XLSX from 'xlsx';
import { FileText, X, AlertTriangle } from 'lucide-react';
import { useImportEmployees } from '../hooks';

const norm = (s) =>
  String(s ?? '')
    .trim()
    .toLowerCase();

// Deteksi kolom secara fleksibel berdasarkan nama header
const matchers = {
  full_name: (h) => h.includes('nama') || h.includes('name'),
  employee_no: (h) =>
    h === 'nik' ||
    h === 'nip' ||
    h === 'no' ||
    h.includes('induk') ||
    h.includes('employee'),
  department: (h) =>
    h.includes('depart') ||
    h.includes('jabat') ||
    h.includes('divisi') ||
    h.includes('posisi') ||
    h.includes('bagian') ||
    h.includes('position'),
};

const mapRow = (row) => {
  const out = {
    full_name: '',
    employee_no: '',
    department: '',
    is_active: true,
  };
  for (const [key, val] of Object.entries(row)) {
    const h = norm(key);
    const v = String(val ?? '').trim();
    if (!v) continue;
    if (!out.full_name && matchers.full_name(h)) out.full_name = v;
    else if (!out.employee_no && matchers.employee_no(h)) out.employee_no = v;
    else if (!out.department && matchers.department(h)) out.department = v;
  }
  return out;
};

const EmployeeImportExcel = () => {
  const importEmployees = useImportEmployees();
  const fileRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [rows, setRows] = useState([]);
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');

  const valid = rows.filter((r) => r.full_name && r.employee_no);
  const invalidCount = rows.length - valid.length;

  const reset = () => {
    setRows([]);
    setFileName('');
    setError('');
    if (fileRef.current) fileRef.current.value = '';
  };

  const handleFile = async (file) => {
    if (!file) return;
    setError('');
    setFileName(file.name);
    try {
      const buf = await file.arrayBuffer();
      const wb = XLSX.read(buf, { type: 'array' });
      const ws = wb.Sheets[wb.SheetNames[0]];
      // raw:false → jaga NIK panjang tetap sebagai teks, tidak jadi angka
      const json = XLSX.utils.sheet_to_json(ws, { defval: '', raw: false });
      if (!json.length) {
        setError('Sheet kosong atau tidak terbaca.');
        setRows([]);
        return;
      }
      setRows(json.map(mapRow));
    } catch {
      setError('Gagal membaca file. Pastikan format .xlsx / .xls valid.');
      setRows([]);
    }
  };

  const doImport = () => {
    if (!valid.length) return;
    importEmployees.mutate(valid, {
      onSuccess: () => {
        reset();
        setOpen(false);
      },
    });
  };

  const downloadTemplate = () => {
    const ws = XLSX.utils.aoa_to_sheet([
      ['Nama', 'NIK', 'Jabatan'],
      ['Budi Santoso', '3201010101010001', 'Op Tenun Youjia'],
      ['Siti Aminah', '3201010101010002', 'Admin Purchasing'],
    ]);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Karyawan');
    XLSX.writeFile(wb, 'template_karyawan.xlsx');
  };

  return (
    <>
      <button
        type='button'
        onClick={() => setOpen(true)}
        className='inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-slate-300 text-slate-600 text-xs font-medium hover:bg-slate-50'
      >
        <FileText className='w-3.5 h-3.5' /> Import Excel
      </button>

      {open && (
        <div
          className='fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-slate-900/50 sm:p-4'
          onClick={() => setOpen(false)}
        >
          <div
            className='bg-white w-full sm:max-w-2xl rounded-t-2xl sm:rounded-xl shadow-xl max-h-[90vh] flex flex-col'
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className='flex items-center justify-between px-5 py-4 border-b border-slate-100'>
              <div>
                <h3 className='font-semibold text-slate-800'>
                  Import Karyawan dari Excel
                </h3>
                <p className='text-xs text-slate-500'>
                  Kolom: Nama, NIK, Departemen/Jabatan
                </p>
              </div>
              <button
                onClick={() => setOpen(false)}
                className='text-slate-400 hover:text-slate-600'
              >
                <X className='w-5 h-5' />
              </button>
            </div>

            {/* Body */}
            <div className='p-5 overflow-y-auto space-y-4'>
              <div className='flex flex-col sm:flex-row gap-2'>
                <input
                  ref={fileRef}
                  type='file'
                  accept='.xlsx,.xls'
                  className='hidden'
                  onChange={(e) => handleFile(e.target.files?.[0])}
                />
                <button
                  onClick={() => fileRef.current?.click()}
                  className='flex-1 border-2 border-dashed border-slate-300 rounded-lg px-4 py-6 text-center text-sm text-slate-500 hover:border-brand-400 hover:text-brand-600'
                >
                  {fileName ? (
                    <span className='font-medium text-slate-700'>
                      {fileName}
                    </span>
                  ) : (
                    'Klik untuk pilih file .xlsx / .xls'
                  )}
                </button>
                <button
                  onClick={downloadTemplate}
                  className='sm:self-start text-xs text-brand-600 hover:underline whitespace-nowrap px-2 py-1'
                >
                  Unduh template
                </button>
              </div>

              {error && (
                <div className='flex items-center gap-2 text-red-700 bg-red-50 border border-red-200 rounded-lg px-3 py-2 text-sm'>
                  <AlertTriangle className='w-4 h-4 shrink-0' /> {error}
                </div>
              )}

              {rows.length > 0 && (
                <>
                  <div className='flex items-center gap-3 text-sm'>
                    <span className='text-green-700 font-medium'>
                      {valid.length} valid
                    </span>
                    {invalidCount > 0 && (
                      <span className='text-amber-700'>
                        {invalidCount} dilewati (Nama/NIK kosong)
                      </span>
                    )}
                  </div>
                  <div className='border border-slate-200 rounded-lg overflow-hidden'>
                    <div className='max-h-64 overflow-y-auto'>
                      <table className='w-full text-sm'>
                        <thead className='bg-slate-50 text-slate-500 sticky top-0'>
                          <tr>
                            <th className='text-left px-3 py-2'>Nama</th>
                            <th className='text-left px-3 py-2'>NIK</th>
                            <th className='text-left px-3 py-2'>Departemen</th>
                            <th className='px-3 py-2'></th>
                          </tr>
                        </thead>
                        <tbody>
                          {rows.map((r, i) => {
                            const ok = r.full_name && r.employee_no;
                            return (
                              <tr
                                key={i}
                                className={`border-t border-slate-100 ${ok ? '' : 'bg-amber-50/60'}`}
                              >
                                <td className='px-3 py-1.5 text-slate-800'>
                                  {r.full_name || (
                                    <span className='text-slate-300'>—</span>
                                  )}
                                </td>
                                <td className='px-3 py-1.5 text-slate-600'>
                                  {r.employee_no || (
                                    <span className='text-slate-300'>—</span>
                                  )}
                                </td>
                                <td className='px-3 py-1.5 text-slate-600'>
                                  {r.department || (
                                    <span className='text-slate-300'>—</span>
                                  )}
                                </td>
                                <td className='px-3 py-1.5 text-right'>
                                  {ok ? (
                                    <span className='text-green-600 text-xs'>
                                      ✓
                                    </span>
                                  ) : (
                                    <span className='text-amber-600 text-xs'>
                                      lewati
                                    </span>
                                  )}
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Footer */}
            <div className='flex items-center justify-end gap-2 px-5 py-4 border-t border-slate-100'>
              <button
                onClick={() => {
                  reset();
                  setOpen(false);
                }}
                className='px-4 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100'
              >
                Batal
              </button>
              <button
                onClick={doImport}
                disabled={!valid.length || importEmployees.isPending}
                className='px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'
              >
                {importEmployees.isPending
                  ? 'Mengimpor…'
                  : `Import ${valid.length} Karyawan`}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default EmployeeImportExcel;
