import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Visits from './pages/Visits';
import Queue from './pages/Queue';
import MedicalRecords from './pages/MedicalRecords';
import Medicines from './pages/Medicines';

const ClinicRoutes = () => (
  <Routes>
    <Route index element={<Navigate to='dashboard' replace />} />
    <Route path='dashboard' element={<Dashboard />} />
    <Route path='visits' element={<Visits />} />
    <Route path='queue' element={<Queue />} />
    <Route path='medical-records' element={<MedicalRecords />} />
    <Route path='medicines' element={<Medicines />} />
    <Route path='*' element={<Navigate to='dashboard' replace />} />
  </Routes>
);

export default ClinicRoutes;
