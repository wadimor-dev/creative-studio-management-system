import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, FileText, ArrowRight, User, Activity } from 'lucide-react';
import { useVisits, useSOAPNoteByVisit, useUpdateSOAPNoteByVisit, useVitalSignByVisit, useUpdateVitalSignByVisit, useDiagnosesByVisit, useICD10Codes, useCreateDiagnosis, useDeleteDiagnosis } from '../hooks';
import { CLINIC_ROUTES, VISIT_STATUS } from '../constants';
import { formatTime } from '../helpers';

const SOAP_FIELDS = [
  { key: 'subjective', label: 'Subjective', hint: 'Keluhan pasien' },
  { key: 'objective', label: 'Objective', hint: 'Hasil pemeriksaan' },
  { key: 'assessment', label: 'Assessment', hint: 'Diagnosis' },
  { key: 'plan', label: 'Plan', hint: 'Tindakan / anjuran' },
];

const VITAL_FIELDS = [
  { key: 'systolic', label: 'TD Sistolik', unit: 'mmHg', type: 'number' },
  { key: 'diastolic', label: 'TD Diastolik', unit: 'mmHg', type: 'number' },
  { key: 'pulse', label: 'Nadi', unit: 'x/mnt', type: 'number' },
  { key: 'respiration', label: 'RR', unit: 'x/mnt', type: 'number' },
  { key: 'temperature', label: 'Suhu', unit: '°C', type: 'number', step: '0.1' },
  { key: 'spo2', label: 'SpO2', unit: '%', type: 'number', step: '0.1' },
  { key: 'weight', label: 'BB', unit: 'kg', type: 'number', step: '0.1' },
  { key: 'height', label: 'TB', unit: 'cm', type: 'number', step: '0.1' },
];

const MedicalRecords = () => {
  const navigate = useNavigate();
  const { data: visitsData, isLoading } = useVisits({ limit: 100 });
  const { data: icd10Data } = useICD10Codes({ limit: 200 });
  const [selectedVisitId, setSelectedVisitId] = useState(null);
  const [soapForm, setSoapForm] = useState({});
  const [vitalForm, setVitalForm] = useState({});
  const [icd10Id, setIcd10Id] = useState('');
  const [diagType, setDiagType] = useState('PRIMARY');
  const [diagNote, setDiagNote] = useState('');

  const updateSOAP = useUpdateSOAPNoteByVisit();
  const updateVital = useUpdateVitalSignByVisit();
  const createDiag = useCreateDiagnosis();
  const deleteDiag = useDeleteDiagnosis();

  const visits = Array.isArray(visitsData) ? visitsData : visitsData?.data || visitsData?.items || [];
  const icd10Codes = Array.isArray(icd10Data) ? icd10Data : icd10Data?.data || icd10Data?.items || [];
  const servingVisits = visits.filter(v => v.visit_status === VISIT_STATUS.SERVING);

  const selectedVisit = servingVisits.find(v => v.id === selectedVisitId);
  const { data: soapData } = useSOAPNoteByVisit(selectedVisitId);
  const { data: vitalData } = useVitalSignByVisit(selectedVisitId);
  const { data: diagData, refetch: refetchDiag } = useDiagnosesByVisit(selectedVisitId);

  const soapNote = soapData?.data || soapData;
  const vitalSign = vitalData?.data || vitalData;
  const diagnoses = Array.isArray(diagData) ? diagData : diagData?.data || diagData || [];

  useEffect(() => {
    if (soapNote) {
      setSoapForm({
        subjective: soapNote.subjective || '',
        objective: soapNote.objective || '',
        assessment: soapNote.assessment || '',
        plan: soapNote.plan || '',
      });
    } else {
      setSoapForm({ subjective: selectedVisit?.complaint || '', objective: '', assessment: '', plan: '' });
    }
    if (vitalSign) {
      setVitalForm({
        systolic: vitalSign.systolic || '', diastolic: vitalSign.diastolic || '',
        pulse: vitalSign.pulse || '', respiration: vitalSign.respiration || '',
        temperature: vitalSign.temperature || '', spo2: vitalSign.spo2 || '',
        height: vitalSign.height || '', weight: vitalSign.weight || '',
      });
    } else {
      setVitalForm({});
    }
  }, [soapNote, vitalSign, selectedVisit]);

  const saveSOAP = () => {
    if (!selectedVisitId) return;
    updateSOAP.mutate({ visit_id: selectedVisitId, ...soapForm });
  };

  const saveVitals = () => {
    if (!selectedVisitId) return;
    const cleaned = {};
    Object.entries(vitalForm).forEach(([k, v]) => { if (v !== '') cleaned[k] = Number(v); });
    updateVital.mutate({ visit_id: selectedVisitId, ...cleaned });
  };

  const addDiagnosis = () => {
    if (!selectedVisitId || !icd10Id) return;
    createDiag.mutate(
      { visit_id: selectedVisitId, icd10_id: icd10Id, diagnosis_type: diagType, diagnosis_note: diagNote || undefined },
      { onSuccess: () => { setIcd10Id(''); setDiagNote(''); refetchDiag(); } }
    );
  };

  const handleRemoveDiag = (id) => {
    deleteDiag.mutate(id, { onSuccess: () => refetchDiag() });
  };

  const fieldCls = 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500';

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-7xl'>
      <div>
        <h1 className='text-xl font-semibold text-slate-800'>Rekam Medis</h1>
        <p className='text-slate-500 text-sm'>Isi catatan SOAP, tanda vital, diagnosis untuk pasien yang diperiksa.</p>
      </div>

      <div className='grid md:grid-cols-4 gap-4 md:gap-6'>
        <div className='md:col-span-1'>
          <div className='bg-white border border-slate-200 rounded-xl p-4 md:p-5 shadow-sm'>
            <h2 className='font-semibold text-slate-800 mb-3'>Diperiksa</h2>
            {isLoading ? (
              <div className='space-y-2'>{Array.from({ length: 3 }).map((_, i) => <div key={i} className='h-16 rounded-lg bg-slate-100 animate-pulse' />)}</div>
            ) : servingVisits.length === 0 ? (
              <div className='text-center py-8 text-slate-400'>
                <Activity className='w-9 h-9 mx-auto mb-2 opacity-40' />
                <p className='text-sm'>Belum ada pasien diperiksa.</p>
                <button onClick={() => navigate(CLINIC_ROUTES.queue)} className='mt-2 inline-flex items-center gap-1 text-brand-600 text-sm hover:underline'>
                  Panggil dari Antrian <ArrowRight className='w-3.5 h-3.5' />
                </button>
              </div>
            ) : (
              <ul className='space-y-2'>
                {servingVisits.map((v) => (
                  <li key={v.id}>
                    <button onClick={() => setSelectedVisitId(v.id)}
                      className={`w-full text-left border rounded-lg p-3 transition ${selectedVisitId === v.id ? 'border-brand-500 bg-brand-50 ring-1 ring-brand-500' : 'border-slate-200 hover:bg-slate-50'}`}>
                      <div className='flex items-center gap-2'>
                        <span className='w-8 h-8 rounded-lg bg-white border border-slate-200 text-brand-700 font-bold grid place-items-center text-sm shrink-0'>#{v.queue_number || '—'}</span>
                        <div className='min-w-0'>
                          <div className='font-medium text-slate-800 truncate'>{v.patient_name || 'Pasien'}</div>
                          {v.complaint && <div className='text-xs text-slate-500 truncate'>{v.complaint}</div>}
                        </div>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>

        <div className='md:col-span-3 space-y-4'>
          {!selectedVisit ? (
            <div className='bg-white border border-dashed border-slate-300 rounded-xl p-10 text-center text-slate-400'>
              <FileText className='w-10 h-10 mx-auto mb-2 opacity-40' />
              <p className='text-sm'>Pilih pasien di samping untuk mulai mengisi rekam medis.</p>
            </div>
          ) : (
            <>
              <div className='bg-gradient-to-r from-slate-800 to-slate-900 text-white rounded-xl p-4 md:p-5'>
                <div className='flex items-center gap-3'>
                  <span className='w-11 h-11 rounded-xl bg-white/15 grid place-items-center font-bold'>#{selectedVisit.queue_number || '—'}</span>
                  <div className='min-w-0'>
                    <div className='font-semibold truncate flex items-center gap-2'><User className='w-4 h-4' /> {selectedVisit.patient_name || 'Pasien'}</div>
                    <div className='text-slate-300 text-sm'>{selectedVisit.visit_number} · masuk {formatTime(selectedVisit.visit_date)}</div>
                  </div>
                </div>
                {selectedVisit.complaint && (
                  <div className='mt-3 text-sm bg-white/10 rounded-lg px-3 py-2'><span className='text-slate-300'>Keluhan: </span>{selectedVisit.complaint}</div>
                )}
              </div>

              <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
                <h2 className='font-semibold text-slate-800 mb-3'>Tanda Vital</h2>
                <div className='grid grid-cols-2 sm:grid-cols-4 gap-3'>
                  {VITAL_FIELDS.map(f => (
                    <div key={f.key}>
                      <label className='block text-xs text-slate-500 mb-0.5'>{f.label} ({f.unit})</label>
                      <input type={f.type} step={f.step} value={vitalForm[f.key] ?? ''} onChange={(e) => setVitalForm(p => ({ ...p, [f.key]: e.target.value }))} className={fieldCls} />
                    </div>
                  ))}
                </div>
                <button onClick={saveVitals} disabled={updateVital.isPending} className='mt-3 px-4 py-2 rounded-lg bg-slate-800 text-white text-sm font-medium hover:bg-slate-900 disabled:opacity-50'>
                  {updateVital.isPending ? 'Menyimpan…' : 'Simpan Tanda Vital'}
                </button>
              </div>

              <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
                <h2 className='font-semibold text-slate-800 mb-3'>SOAP</h2>
                <div className='grid sm:grid-cols-2 gap-3'>
                  {SOAP_FIELDS.map(({ key, label, hint }) => (
                    <div key={key}>
                      <label className='block text-sm mb-1 text-slate-700 font-medium'>{label} <span className='text-slate-400 font-normal'>· {hint}</span></label>
                      <textarea value={soapForm[key] || ''} onChange={(e) => setSoapForm(p => ({ ...p, [key]: e.target.value }))} rows={3} className={fieldCls} />
                    </div>
                  ))}
                </div>
                <button onClick={saveSOAP} disabled={updateSOAP.isPending} className='mt-3 px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'>
                  {updateSOAP.isPending ? 'Menyimpan…' : 'Simpan SOAP'}
                </button>
              </div>

              <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
                <h2 className='font-semibold text-slate-800 mb-3'>Diagnosis</h2>
                <div className='flex flex-wrap gap-2 items-end mb-4'>
                  <div className='flex-1 min-w-[200px]'>
                    <label className='block text-xs text-slate-500 mb-0.5'>Kode ICD-10</label>
                    <select value={icd10Id} onChange={(e) => setIcd10Id(e.target.value)} className={fieldCls}>
                      <option value=''>— pilih —</option>
                      {icd10Codes.map(c => <option key={c.id} value={c.id}>{c.code} — {c.name}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className='block text-xs text-slate-500 mb-0.5'>Tipe</label>
                    <select value={diagType} onChange={(e) => setDiagType(e.target.value)} className={fieldCls}>
                      <option value='PRIMARY'>Utama</option>
                      <option value='SECONDARY'>Sekunder</option>
                      <option value='DIFFERENTIAL'>Diferensial</option>
                      <option value='FINAL'>Final</option>
                    </select>
                  </div>
                  <div className='flex-1 min-w-[200px]'>
                    <label className='block text-xs text-slate-500 mb-0.5'>Catatan</label>
                    <input value={diagNote} onChange={(e) => setDiagNote(e.target.value)} className={fieldCls} placeholder='Opsional' />
                  </div>
                  <button onClick={addDiagnosis} disabled={!icd10Id || createDiag.isPending}
                    className='px-4 py-2 rounded-lg bg-brand-600 text-white text-sm font-medium hover:bg-brand-700 disabled:opacity-50'>
                    + Tambah
                  </button>
                </div>
                {diagnoses.length > 0 ? (
                  <ul className='space-y-2'>
                    {diagnoses.map((d) => (
                      <li key={d.id} className='flex items-center gap-2 text-sm bg-slate-50 rounded-lg px-3 py-2'>
                        <span className='px-2 py-0.5 rounded bg-blue-100 text-blue-700 text-xs font-medium'>
                          {d.diagnosis_type === 'PRIMARY' ? 'Utama' : d.diagnosis_type === 'SECONDARY' ? 'Sekunder' : d.diagnosis_type}
                        </span>
                        <span className='font-medium'>{d.icd10_code}</span>
                        <span className='text-slate-600 flex-1'>{d.icd10_name}</span>
                        <button onClick={() => handleRemoveDiag(d.id)} className='text-red-500 hover:text-red-700 text-xs'>Hapus</button>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className='text-sm text-slate-400'>Belum ada diagnosis.</p>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicalRecords;
