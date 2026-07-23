import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Visits from './pages/Visits';
import VisitDetail from './pages/VisitDetail';
import Queue from './pages/Queue';
import MedicalRecords from './pages/MedicalRecords';
import Medicines from './pages/Medicines';
import Patients from './pages/Patients';
import HealthcareProfessionals from './pages/HealthcareProfessionals';
import ICD10Codes from './pages/ICD10Codes';
import MedicalProcedures from './pages/MedicalProcedures';

const ClinicRoutes = () => (
  <Routes>
    <Route index element={<Navigate to='dashboard' replace />} />
    <Route path='dashboard' element={<Dashboard />} />
    <Route path='visits' element={<Visits />} />
    <Route path='visits/:id' element={<VisitDetail />} />
    <Route path='queue' element={<Queue />} />
    <Route path='medical-records' element={<MedicalRecords />} />
    <Route path='medicines' element={<Medicines />} />
    <Route path='patients' element={<Patients />} />
    <Route path='healthcare-professionals' element={<HealthcareProfessionals />} />
    <Route path='icd10' element={<ICD10Codes />} />
    <Route path='medical-procedures' element={<MedicalProcedures />} />
    <Route path='*' element={<Navigate to='dashboard' replace />} />
  </Routes>
);

export default ClinicRoutes;
