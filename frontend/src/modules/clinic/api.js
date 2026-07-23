import api from '../../api/axios';
import { ENDPOINTS } from '../../api/endpoints';

const { CLINIC } = ENDPOINTS;

export const clinicApi = {
  /* ==================== PATIENTS ==================== */
  getPatientProfiles(params) { return api.get(CLINIC.MASTER_DATA.PATIENT_PROFILES, { params }).then(r => r.data); },
  getPatientProfile(id) { return api.get(CLINIC.MASTER_DATA.PATIENT_PROFILE(id)).then(r => r.data); },
  getPatientProfileByEmployee(eid) { return api.get(CLINIC.MASTER_DATA.PATIENT_PROFILE_BY_EMPLOYEE(eid)).then(r => r.data); },
  getPatientProfileByMr(mr) { return api.get(CLINIC.MASTER_DATA.PATIENT_PROFILE_BY_MR(mr)).then(r => r.data); },
  createPatientProfile(payload) { return api.post(CLINIC.MASTER_DATA.PATIENT_PROFILES, payload).then(r => r.data); },
  updatePatientProfile(id, payload) { return api.put(CLINIC.MASTER_DATA.PATIENT_PROFILE(id), payload).then(r => r.data); },
  deletePatientProfile(id) { return api.delete(CLINIC.MASTER_DATA.PATIENT_PROFILE(id)).then(r => r.data); },

  /* ==================== HC PROFESSIONALS ==================== */
  getHCProfessionals(params) { return api.get(CLINIC.MASTER_DATA.HEALTHCARE_PROFESSIONALS, { params }).then(r => r.data); },
  getHCProfessional(id) { return api.get(CLINIC.MASTER_DATA.HEALTHCARE_PROFESSIONAL(id)).then(r => r.data); },
  createHCProfessional(payload) { return api.post(CLINIC.MASTER_DATA.HEALTHCARE_PROFESSIONALS, payload).then(r => r.data); },
  updateHCProfessional(id, payload) { return api.put(CLINIC.MASTER_DATA.HEALTHCARE_PROFESSIONAL(id), payload).then(r => r.data); },
  deleteHCProfessional(id) { return api.delete(CLINIC.MASTER_DATA.HEALTHCARE_PROFESSIONAL(id)).then(r => r.data); },

  /* ==================== ICD-10 CODES ==================== */
  getICD10Codes(params) { return api.get(CLINIC.MASTER_DATA.ICD10_CODES, { params }).then(r => r.data); },
  getICD10Code(id) { return api.get(CLINIC.MASTER_DATA.ICD10_CODE(id)).then(r => r.data); },
  createICD10Code(payload) { return api.post(CLINIC.MASTER_DATA.ICD10_CODES, payload).then(r => r.data); },
  updateICD10Code(id, payload) { return api.put(CLINIC.MASTER_DATA.ICD10_CODE(id), payload).then(r => r.data); },
  deleteICD10Code(id) { return api.delete(CLINIC.MASTER_DATA.ICD10_CODE(id)).then(r => r.data); },

  /* ==================== MEDICAL PROCEDURES ==================== */
  getMedicalProcedures(params) { return api.get(CLINIC.MASTER_DATA.MEDICAL_PROCEDURES, { params }).then(r => r.data); },
  getMedicalProcedure(id) { return api.get(CLINIC.MASTER_DATA.MEDICAL_PROCEDURE(id)).then(r => r.data); },
  createMedicalProcedure(payload) { return api.post(CLINIC.MASTER_DATA.MEDICAL_PROCEDURES, payload).then(r => r.data); },
  updateMedicalProcedure(id, payload) { return api.put(CLINIC.MASTER_DATA.MEDICAL_PROCEDURE(id), payload).then(r => r.data); },
  deleteMedicalProcedure(id) { return api.delete(CLINIC.MASTER_DATA.MEDICAL_PROCEDURE(id)).then(r => r.data); },

  /* ==================== QUEUES ==================== */
  getQueues(params) { return api.get(CLINIC.REGISTRATION.QUEUES, { params }).then(r => r.data); },
  getCurrentQueue() { return api.get(CLINIC.REGISTRATION.QUEUE_CURRENT).then(r => r.data); },
  getWaitingCount() { return api.get(CLINIC.REGISTRATION.QUEUE_WAITING_COUNT).then(r => r.data); },
  getQueue(id) { return api.get(CLINIC.REGISTRATION.QUEUE(id)).then(r => r.data); },
  createQueue(payload) { return api.post(CLINIC.REGISTRATION.QUEUES, payload).then(r => r.data); },
  updateQueueStatus(id, status) { return api.put(CLINIC.REGISTRATION.QUEUE_STATUS(id), { status }).then(r => r.data); },

  /* ==================== VISITS ==================== */
  getVisits(params) { return api.get(CLINIC.REGISTRATION.VISITS, { params }).then(r => r.data); },
  getVisit(id) { return api.get(CLINIC.REGISTRATION.VISIT(id)).then(r => r.data); },
  getVisitDetail(id) { return api.get(CLINIC.REGISTRATION.VISIT_DETAIL(id)).then(r => r.data); },
  createVisit(payload) { return api.post(CLINIC.REGISTRATION.VISITS, payload).then(r => r.data); },
  updateVisit(id, payload) { return api.put(CLINIC.REGISTRATION.VISIT(id), payload).then(r => r.data); },
  checkinVisit(id) { return api.put(CLINIC.REGISTRATION.VISIT_CHECKIN(id)).then(r => r.data); },
  startServingVisit(id) { return api.put(CLINIC.REGISTRATION.VISIT_START_SERVING(id)).then(r => r.data); },
  finishVisit(id) { return api.put(CLINIC.REGISTRATION.VISIT_FINISH(id)).then(r => r.data); },
  cancelVisit(id) { return api.put(CLINIC.REGISTRATION.VISIT_CANCEL(id)).then(r => r.data); },

  /* ==================== MEDICAL RECORDS ==================== */
  getMedicalRecords(params) { return api.get(CLINIC.MEDICAL.MEDICAL_RECORDS, { params }).then(r => r.data); },
  getMedicalRecord(id) { return api.get(CLINIC.MEDICAL.MEDICAL_RECORD(id)).then(r => r.data); },
  getMedicalRecordByVisit(vid) { return api.get(CLINIC.MEDICAL.MEDICAL_RECORD_BY_VISIT(vid)).then(r => r.data); },
  createMedicalRecord(payload) { return api.post(CLINIC.MEDICAL.MEDICAL_RECORDS, payload).then(r => r.data); },
  updateMedicalRecord(id, payload) { return api.put(CLINIC.MEDICAL.MEDICAL_RECORD(id), payload).then(r => r.data); },
  finalizeMedicalRecord(id) { return api.put(CLINIC.MEDICAL.MEDICAL_RECORD_FINALIZE(id)).then(r => r.data); },

  /* ==================== SOAP NOTES ==================== */
  getSOAPNote(id) { return api.get(CLINIC.MEDICAL.SOAP_NOTE(id)).then(r => r.data); },
  getSOAPNoteByVisit(vid) { return api.get(CLINIC.MEDICAL.SOAP_NOTE_BY_VISIT(vid)).then(r => r.data); },
  createSOAPNote(payload) { return api.post(CLINIC.MEDICAL.SOAP_NOTES, payload).then(r => r.data); },
  updateSOAPNote(id, payload) { return api.put(CLINIC.MEDICAL.SOAP_NOTE(id), payload).then(r => r.data); },
  updateSOAPNoteByVisit(vid, payload) { return api.put(CLINIC.MEDICAL.SOAP_NOTE_BY_VISIT(vid), payload).then(r => r.data); },

  /* ==================== VITAL SIGNS ==================== */
  getVitalSign(id) { return api.get(CLINIC.MEDICAL.VITAL_SIGN(id)).then(r => r.data); },
  getVitalSignByVisit(vid) { return api.get(CLINIC.MEDICAL.VITAL_SIGN_BY_VISIT(vid)).then(r => r.data); },
  createVitalSign(payload) { return api.post(CLINIC.MEDICAL.VITAL_SIGNS, payload).then(r => r.data); },
  updateVitalSign(id, payload) { return api.put(CLINIC.MEDICAL.VITAL_SIGN(id), payload).then(r => r.data); },
  updateVitalSignByVisit(vid, payload) { return api.put(CLINIC.MEDICAL.VITAL_SIGN_BY_VISIT(vid), payload).then(r => r.data); },

  /* ==================== DIAGNOSES ==================== */
  getDiagnosesByVisit(vid) { return api.get(CLINIC.MEDICAL.DIAGNOSES_BY_VISIT(vid)).then(r => r.data); },
  createDiagnosis(payload) { return api.post(CLINIC.MEDICAL.DIAGNOSES, payload).then(r => r.data); },
  updateDiagnosis(id, payload) { return api.put(CLINIC.MEDICAL.DIAGNOSIS(id), payload).then(r => r.data); },
  deleteDiagnosis(id) { return api.delete(CLINIC.MEDICAL.DIAGNOSIS(id)).then(r => r.data); },

  /* ==================== VISIT PROCEDURES ==================== */
  getVisitProceduresByVisit(vid) { return api.get(CLINIC.MEDICAL.VISIT_PROCEDURES_BY_VISIT(vid)).then(r => r.data); },
  createVisitProcedure(payload) { return api.post(CLINIC.MEDICAL.VISIT_PROCEDURES, payload).then(r => r.data); },
  updateVisitProcedure(id, payload) { return api.put(CLINIC.MEDICAL.VISIT_PROCEDURE(id), payload).then(r => r.data); },
  deleteVisitProcedure(id) { return api.delete(CLINIC.MEDICAL.VISIT_PROCEDURE(id)).then(r => r.data); },

  /* ==================== MEDICAL ATTACHMENTS ==================== */
  getAttachmentsByVisit(vid) { return api.get(CLINIC.MEDICAL.ATTACHMENTS_BY_VISIT(vid)).then(r => r.data); },
  createAttachment(payload) { return api.post(CLINIC.MEDICAL.ATTACHMENTS, payload).then(r => r.data); },
  updateAttachment(id, payload) { return api.put(CLINIC.MEDICAL.ATTACHMENT(id), payload).then(r => r.data); },
  deleteAttachment(id) { return api.delete(CLINIC.MEDICAL.ATTACHMENT(id)).then(r => r.data); },

  /* ==================== PRESCRIPTIONS ==================== */
  getPrescription(id) { return api.get(CLINIC.PHARMACY.PRESCRIPTION(id)).then(r => r.data); },
  getPrescriptionByVisit(vid) { return api.get(CLINIC.PHARMACY.PRESCRIPTION_BY_VISIT(vid)).then(r => r.data); },
  createPrescription(payload) { return api.post(CLINIC.PHARMACY.PRESCRIPTIONS, payload).then(r => r.data); },
  updatePrescription(id, payload) { return api.put(CLINIC.PHARMACY.PRESCRIPTION(id), payload).then(r => r.data); },
  dispensePrescription(id) { return api.put(CLINIC.PHARMACY.PRESCRIPTION_DISPENSE(id)).then(r => r.data); },
  cancelPrescription(id) { return api.put(CLINIC.PHARMACY.PRESCRIPTION_CANCEL(id)).then(r => r.data); },

  /* ==================== PRESCRIPTION ITEMS ==================== */
  getPrescriptionItemsByRx(rid) { return api.get(CLINIC.PHARMACY.PRESCRIPTION_ITEMS_BY_RX(rid)).then(r => r.data); },
  createPrescriptionItem(payload) { return api.post(CLINIC.PHARMACY.PRESCRIPTION_ITEMS, payload).then(r => r.data); },
  updatePrescriptionItem(id, payload) { return api.put(CLINIC.PHARMACY.PRESCRIPTION_ITEM(id), payload).then(r => r.data); },
  deletePrescriptionItem(id) { return api.delete(CLINIC.PHARMACY.PRESCRIPTION_ITEM(id)).then(r => r.data); },

  /* ==================== MEDICINE DISPENSES ==================== */
  getMedicineDispense(id) { return api.get(CLINIC.PHARMACY.MEDICINE_DISPENSE(id)).then(r => r.data); },
  createMedicineDispense(payload) { return api.post(CLINIC.PHARMACY.MEDICINE_DISPENSES, payload).then(r => r.data); },

  /* ==================== MEDICAL CERTIFICATES ==================== */
  getMedicalCertificate(id) { return api.get(CLINIC.CERTIFICATES.MEDICAL_CERTIFICATE(id)).then(r => r.data); },
  getMedicalCertificateByVisit(vid) { return api.get(CLINIC.CERTIFICATES.MEDICAL_CERTIFICATE_BY_VISIT(vid)).then(r => r.data); },
  createMedicalCertificate(payload) { return api.post(CLINIC.CERTIFICATES.MEDICAL_CERTIFICATES, payload).then(r => r.data); },
  updateMedicalCertificate(id, payload) { return api.put(CLINIC.CERTIFICATES.MEDICAL_CERTIFICATE(id), payload).then(r => r.data); },
  deleteMedicalCertificate(id) { return api.delete(CLINIC.CERTIFICATES.MEDICAL_CERTIFICATE(id)).then(r => r.data); },

  /* ==================== ACTIVITY LOGS ==================== */
  getActivityLogs(params) { return api.get(CLINIC.AUDIT.ACTIVITY_LOGS, { params }).then(r => r.data); },
  createActivityLog(payload) { return api.post(CLINIC.AUDIT.ACTIVITY_LOGS, payload).then(r => r.data); },

  /* ==================== DASHBOARD ==================== */
  async getDashboard() {
    const [visitsR, queuesR, patientsR] = await Promise.all([
      this.getVisits({ limit: 50 }),
      this.getQueues({ limit: 50 }),
      this.getPatientProfiles({ limit: 5 }),
    ]);
    const visits = Array.isArray(visitsR) ? visitsR : visitsR?.data || visitsR?.items || [];
    const queues = Array.isArray(queuesR) ? queuesR : queuesR?.data || queuesR?.items || [];
    const patients = Array.isArray(patientsR) ? patientsR : patientsR?.data || patientsR?.items || [];
    const today = new Date().toDateString();
    const todayVisits = visits.filter(v => v.visit_date && new Date(v.visit_date).toDateString() === today);
    const todayQueues = queues.filter(q => q.queue_date && new Date(q.queue_date).toDateString() === today);
    const byStatus = {};
    todayVisits.forEach(v => { byStatus[v.visit_status] = (byStatus[v.visit_status] || 0) + 1; });
    return {
      totals: {
        patientsActive: patients.length,
        visitsToday: todayVisits.length,
        waitingCount: todayQueues.filter(q => q.status === 'WAITING').length,
        servingCount: todayQueues.filter(q => q.status === 'SERVING').length,
      },
      visitsByStatus: byStatus,
      todayQueue: todayQueues.filter(q => q.status === 'WAITING' || q.status === 'CALLING').sort((a, b) => a.queue_number?.localeCompare?.(b.queue_number) || 0),
      todayVisits: todayVisits.slice(0, 10),
    };
  },
};
