import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle } from 'lucide-react';
import { useVisitDetail, useFinishVisit } from '../hooks';
import { VISIT_STATUS } from '../constants';
import { formatDateTime, visitStatusLabel, visitStatusBadge } from '../helpers';
import { StatusBadge } from '../components';

const VisitDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, isLoading } = useVisitDetail(id);
  const finishVisit = useFinishVisit();

  if (isLoading) return <div className='p-6 space-y-4 animate-pulse'><div className='h-8 w-48 bg-slate-200 rounded' /><div className='h-32 bg-slate-100 rounded' /></div>;
  if (!data) return <div className='p-6 text-slate-500'>Kunjungan tidak ditemukan.</div>;

  const v = data?.data || data;
  const mr = v.medical_record;
  const soap = v.soap_note;
  const vs = v.vital_sign;
  const diagnoses = v.diagnoses || [];
  const procedures = v.procedures || [];
  const rx = v.prescription;
  const certs = v.certificates || [];
  const attachments = v.attachments || [];

  return (
    <div className='p-4 md:p-6 space-y-5 max-w-4xl'>
      <button onClick={() => navigate(-1)} className='inline-flex items-center gap-1 text-sm text-slate-500 hover:text-slate-700'>
        <ArrowLeft className='w-4 h-4' /> Kembali
      </button>

      <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
        <div className='flex items-center gap-3 mb-4'>
          <div className='w-12 h-12 rounded-xl bg-brand-50 text-brand-700 font-bold grid place-items-center'>
            #{v.queue_number || '—'}
          </div>
          <div>
            <h1 className='text-xl font-semibold text-slate-800'>{v.patient_name || 'Pasien'}</h1>
            <div className='text-sm text-slate-500'>{v.visit_number} · {formatDateTime(v.visit_date)}</div>
          </div>
          <div className='ml-auto flex items-center gap-2'>
            <StatusBadge label={visitStatusLabel(v.visit_status)} className={visitStatusBadge(v.visit_status)} />
            {v.visit_status === VISIT_STATUS.SERVING && (
              <button onClick={() => finishVisit.mutate(v.id)}
                disabled={finishVisit.isPending}
                className='inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-green-600 text-white text-sm font-medium hover:bg-green-700 disabled:opacity-50'>
                <CheckCircle className='w-4 h-4' />
                {finishVisit.isPending ? '…' : 'Selesai'}
              </button>
            )}
          </div>
        </div>
        {v.complaint && (
          <div className='bg-slate-50 rounded-lg p-3 text-sm'>
            <span className='font-medium text-slate-700'>Keluhan: </span>{v.complaint}
          </div>
        )}
      </div>

      {mr && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>Rekam Medis</h2>
          <div className='grid sm:grid-cols-2 gap-3 text-sm'>
            <div><span className='text-slate-500'>No. Rekam Medis:</span> <span className='font-medium'>{mr.record_number}</span></div>
            <div><span className='text-slate-500'>Status:</span> {mr.status === 'FINALIZED' ? 'Final' : 'Aktif'}</div>
            {mr.chief_complaint && <div className='sm:col-span-2'><span className='text-slate-500'>Keluhan Utama:</span> {mr.chief_complaint}</div>}
            {mr.present_illness && <div className='sm:col-span-2'><span className='text-slate-500'>Riwayat Penyakit:</span> {mr.present_illness}</div>}
          </div>
        </div>
      )}

      {vs && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>Tanda Vital</h2>
          <div className='grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm'>
            {vs.systolic && <div><span className='text-slate-500'>TD:</span> <span className='font-medium'>{vs.systolic}/{vs.diastolic} mmHg</span></div>}
            {vs.pulse && <div><span className='text-slate-500'>Nadi:</span> <span className='font-medium'>{vs.pulse} x/mnt</span></div>}
            {vs.temperature && <div><span className='text-slate-500'>Suhu:</span> <span className='font-medium'>{vs.temperature} °C</span></div>}
            {vs.spo2 && <div><span className='text-slate-500'>SpO2:</span> <span className='font-medium'>{vs.spo2}%</span></div>}
            {vs.respiration && <div><span className='text-slate-500'>RR:</span> <span className='font-medium'>{vs.respiration} x/mnt</span></div>}
            {vs.weight && <div><span className='text-slate-500'>BB:</span> <span className='font-medium'>{vs.weight} kg</span></div>}
            {vs.height && <div><span className='text-slate-500'>TB:</span> <span className='font-medium'>{vs.height} cm</span></div>}
          </div>
        </div>
      )}

      {soap && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>SOAP</h2>
          <div className='space-y-3 text-sm'>
            {soap.subjective && <div><span className='font-medium text-slate-700'>S - Subjective:</span><p className='text-slate-600 mt-0.5'>{soap.subjective}</p></div>}
            {soap.objective && <div><span className='font-medium text-slate-700'>O - Objective:</span><p className='text-slate-600 mt-0.5'>{soap.objective}</p></div>}
            {soap.assessment && <div><span className='font-medium text-slate-700'>A - Assessment:</span><p className='text-slate-600 mt-0.5'>{soap.assessment}</p></div>}
            {soap.plan && <div><span className='font-medium text-slate-700'>P - Plan:</span><p className='text-slate-600 mt-0.5'>{soap.plan}</p></div>}
          </div>
        </div>
      )}

      {diagnoses.length > 0 && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>Diagnosis</h2>
          <ul className='space-y-2'>
            {diagnoses.map((d) => (
              <li key={d.id} className='flex items-center gap-2 text-sm'>
                <span className='px-2 py-0.5 rounded bg-blue-100 text-blue-700 text-xs font-medium'>
                  {d.diagnosis_type === 'PRIMARY' ? 'Utama' : d.diagnosis_type === 'SECONDARY' ? 'Sekunder' : d.diagnosis_type}
                </span>
                <span className='font-medium'>{d.icd10_code}</span>
                <span className='text-slate-600'>{d.icd10_name}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {rx && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>Resep</h2>
          {rx.items?.length > 0 ? (
            <ul className='space-y-2'>
              {rx.items.map((item) => (
                <li key={item.id} className='flex items-center gap-2 text-sm'>
                  <span className='font-medium'>{item.medicine_name}</span>
                  <span className='text-slate-500'>{item.quantity} · {item.dosage || ''} {item.frequency || ''}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className='text-sm text-slate-400'>Tidak ada item resep.</p>
          )}
        </div>
      )}

      {procedures.length > 0 && (
        <div className='bg-white border border-slate-200 rounded-xl p-5 shadow-sm'>
          <h2 className='font-semibold text-slate-800 mb-3'>Tindakan</h2>
          <ul className='space-y-1'>
            {procedures.map((p) => (
              <li key={p.id} className='text-sm'><span className='font-medium'>{p.procedure_name}</span></li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default VisitDetail;
