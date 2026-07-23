import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { toast } from 'react-toastify';
import api from '../../../api/axios';
import { clinicApi } from '../api';
import { QK } from '../constants';

/* ==================== DASHBOARD ==================== */
export const useClinicDashboard = () =>
  useQuery({ queryKey: QK.dashboard, queryFn: () => clinicApi.getDashboard() });

/* ==================== PATIENTS ==================== */
export const usePatientProfiles = (params) =>
  useQuery({ queryKey: QK.patientProfiles(params), queryFn: () => clinicApi.getPatientProfiles(params) });
export const usePatientProfile = (id) =>
  useQuery({ queryKey: QK.patientProfile(id), queryFn: () => clinicApi.getPatientProfile(id), enabled: !!id });
export const useCreatePatientProfile = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createPatientProfile(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'patient-profiles'] }); toast.success('Pasien ditambahkan'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdatePatientProfile = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updatePatientProfile(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'patient-profiles'] }); toast.success('Pasien diperbarui'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDeletePatientProfile = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.deletePatientProfile(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'patient-profiles'] }); toast.success('Pasien dihapus'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== HC PROFESSIONALS ==================== */
export const useHCProfessionals = (params) =>
  useQuery({ queryKey: QK.hcProfessionals(params), queryFn: () => clinicApi.getHCProfessionals(params) });
export const useHCProfessional = (id) =>
  useQuery({ queryKey: QK.hcProfessional(id), queryFn: () => clinicApi.getHCProfessional(id), enabled: !!id });
export const useCreateHCProfessional = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createHCProfessional(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'hc-professionals'] }); toast.success('Tenaga medis ditambahkan'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateHCProfessional = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateHCProfessional(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'hc-professionals'] }); toast.success('Tenaga medis diperbarui'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDeleteHCProfessional = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.deleteHCProfessional(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'hc-professionals'] }); toast.success('Tenaga medis dihapus'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== ICD-10 CODES ==================== */
export const useICD10Codes = (params) =>
  useQuery({ queryKey: QK.icd10(params), queryFn: () => clinicApi.getICD10Codes(params) });
export const useICD10Code = (id) =>
  useQuery({ queryKey: QK.icd10Code(id), queryFn: () => clinicApi.getICD10Code(id), enabled: !!id });
export const useCreateICD10Code = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createICD10Code(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'icd10'] }); toast.success('Kode ICD-10 ditambahkan'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateICD10Code = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateICD10Code(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'icd10'] }); toast.success('Kode ICD-10 diperbarui'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDeleteICD10Code = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.deleteICD10Code(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'icd10'] }); toast.success('Kode ICD-10 dihapus'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== MEDICAL PROCEDURES ==================== */
export const useMedicalProcedures = (params) =>
  useQuery({ queryKey: QK.procedures(params), queryFn: () => clinicApi.getMedicalProcedures(params) });
export const useMedicalProcedure = (id) =>
  useQuery({ queryKey: QK.procedure(id), queryFn: () => clinicApi.getMedicalProcedure(id), enabled: !!id });
export const useCreateMedicalProcedure = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createMedicalProcedure(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'procedures'] }); toast.success('Prosedur ditambahkan'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateMedicalProcedure = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateMedicalProcedure(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'procedures'] }); toast.success('Prosedur diperbarui'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDeleteMedicalProcedure = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.deleteMedicalProcedure(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'procedures'] }); toast.success('Prosedur dihapus'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== QUEUES ==================== */
export const useQueues = (params) =>
  useQuery({ queryKey: QK.queues(params), queryFn: () => clinicApi.getQueues(params) });
export const useCurrentQueue = () =>
  useQuery({ queryKey: QK.queue('current'), queryFn: () => clinicApi.getCurrentQueue() });
export const useWaitingCount = () =>
  useQuery({ queryKey: QK.queue('waiting-count'), queryFn: () => clinicApi.getWaitingCount() });
export const useCreateQueue = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createQueue(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'queues'] }); toast.success('Antrian dibuat'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateQueueStatus = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, status }) => clinicApi.updateQueueStatus(id, status),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== VISITS ==================== */
export const useVisits = (params) =>
  useQuery({ queryKey: QK.visits(params), queryFn: () => clinicApi.getVisits(params) });
export const useVisit = (id) =>
  useQuery({ queryKey: QK.visit(id), queryFn: () => clinicApi.getVisit(id), enabled: !!id });
export const useVisitDetail = (id) =>
  useQuery({ queryKey: QK.visitDetail(id), queryFn: () => clinicApi.getVisitDetail(id), enabled: !!id });
export const useCreateVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createVisit(p),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Kunjungan terdaftar');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateVisit(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'visits'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useCheckinVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.checkinVisit(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      toast.success('Pasien check in');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useStartServingVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.startServingVisit(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Pemeriksaan dimulai');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useFinishVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.finishVisit(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Kunjungan selesai');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useCancelVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.cancelVisit(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'visits'] });
      qc.invalidateQueries({ queryKey: ['clinic', 'queues'] });
      qc.invalidateQueries({ queryKey: QK.dashboard });
      toast.success('Kunjungan dibatalkan');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== MEDICAL RECORDS ==================== */
export const useMedicalRecords = (params) =>
  useQuery({ queryKey: QK.medicalRecords(params), queryFn: () => clinicApi.getMedicalRecords(params) });
export const useMedicalRecord = (id) =>
  useQuery({ queryKey: QK.medicalRecord(id), queryFn: () => clinicApi.getMedicalRecord(id), enabled: !!id });
export const useMedicalRecordByVisit = (vid) =>
  useQuery({ queryKey: QK.medicalRecordByVisit(vid), queryFn: () => clinicApi.getMedicalRecordByVisit(vid), enabled: !!vid });
export const useCreateMedicalRecord = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createMedicalRecord(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'medical-records'] }); toast.success('Rekam medis dibuat'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateMedicalRecord = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateMedicalRecord(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'medical-records'] }); toast.success('Rekam medis diperbarui'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useFinalizeMedicalRecord = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.finalizeMedicalRecord(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'medical-records'] });
      toast.success('Rekam medis difinalkan');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== SOAP NOTES ==================== */
export const useSOAPNoteByVisit = (vid) =>
  useQuery({ queryKey: QK.soapNoteByVisit(vid), queryFn: () => clinicApi.getSOAPNoteByVisit(vid), enabled: !!vid });
export const useCreateSOAPNote = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createSOAPNote(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'soap-note-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateSOAPNoteByVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ visit_id, ...p }) => clinicApi.updateSOAPNoteByVisit(visit_id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'soap-note-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== VITAL SIGNS ==================== */
export const useVitalSignByVisit = (vid) =>
  useQuery({ queryKey: QK.vitalSignByVisit(vid), queryFn: () => clinicApi.getVitalSignByVisit(vid), enabled: !!vid });
export const useCreateVitalSign = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createVitalSign(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'vital-sign-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateVitalSignByVisit = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ visit_id, ...p }) => clinicApi.updateVitalSignByVisit(visit_id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'vital-sign-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== DIAGNOSES ==================== */
export const useDiagnosesByVisit = (vid) =>
  useQuery({ queryKey: QK.diagnosesByVisit(vid), queryFn: () => clinicApi.getDiagnosesByVisit(vid), enabled: !!vid });
export const useCreateDiagnosis = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createDiagnosis(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'diagnoses-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useUpdateDiagnosis = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, ...p }) => clinicApi.updateDiagnosis(id, p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'diagnoses-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDeleteDiagnosis = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.deleteDiagnosis(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'diagnoses-visit'] }); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== VISIT PROCEDURES ==================== */
export const useVisitProceduresByVisit = (vid) =>
  useQuery({ queryKey: QK.visitProceduresByVisit(vid), queryFn: () => clinicApi.getVisitProceduresByVisit(vid), enabled: !!vid });

/* ==================== PRESCRIPTIONS ==================== */
export const usePrescriptionByVisit = (vid) =>
  useQuery({ queryKey: QK.prescriptionByVisit(vid), queryFn: () => clinicApi.getPrescriptionByVisit(vid), enabled: !!vid });
export const useCreatePrescription = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p) => clinicApi.createPrescription(p),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['clinic', 'prescriptions'] }); toast.success('Resep dibuat'); },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};
export const useDispensePrescription = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id) => clinicApi.dispensePrescription(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['clinic', 'prescriptions'] });
      toast.success('Obat diberikan');
    },
    onError: (e) => toast.error(e?.response?.data?.detail || e.message),
  });
};

/* ==================== MEDICINES (Inventory items) ==================== */
export const useMedicines = (params) =>
  useQuery({ queryKey: ['clinic', 'medicines', params], queryFn: () => api.get('/inventory/items', { params }).then(r => r.data) });

/* ==================== MEDICAL CERTIFICATES ==================== */
export const useMedicalCertificates = (params) =>
  useQuery({ queryKey: QK.certificates(params), queryFn: () => api.get('/clinic/certificates/medical-certificates', { params }).then(r => r.data) });

/* ==================== ACTIVITY LOGS ==================== */
export const useActivityLogs = (params) =>
  useQuery({ queryKey: QK.activityLogs(params), queryFn: () => clinicApi.getActivityLogs(params) });
