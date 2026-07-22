import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './pages/DashboardV2';
import SampleManagement from './pages/SampleManagement';
import BorrowingPage from './pages/BorrowingPage';
import GuestManagement from './pages/GuestManagement';
import StockControl from './pages/StockControl';
import Reporting from './pages/Reporting';
import MasterData from './pages/MasterData';
import LocationManagement from './pages/LocationManagement';
import StorageManagement from './pages/StorageManagement';
import ScanStorage from './pages/ScanStorage';
import QRGenerator from './pages/QRGenerator';
import ShowroomManagement from './pages/ShowroomManagement';

const ShowroomRoutes = () => (
  <Routes>
    <Route index element={<Navigate to="dashboard" replace />} />
    <Route path="dashboard" element={<Dashboard />} />
    <Route path="samples" element={<SampleManagement />} />
    <Route path="borrowings" element={<BorrowingPage />} />
    <Route path="guests" element={<GuestManagement />} />
    <Route path="stock-control" element={<StockControl />} />
    <Route path="locations" element={<LocationManagement />} />
    <Route path="storage" element={<StorageManagement />} />
    <Route path="scan" element={<ScanStorage />} />
    <Route path="qr-generator" element={<QRGenerator />} />
    <Route path="reports" element={<Reporting />} />
    <Route path="master-data" element={<MasterData />} />
    <Route path="management" element={<ShowroomManagement />} />
  </Routes>
);

export default ShowroomRoutes;
