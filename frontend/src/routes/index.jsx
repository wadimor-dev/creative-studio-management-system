import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import AuthLayout from '../layouts/AuthLayout';
import MainLayout from '../layouts/MainLayout';
import ProtectedRoute from '../components/layout/ProtectedRoute';

import Login from '../pages/Login';
import Dashboard from '../pages/Dashboard';
import InventoryDashboard from '../pages/Inventory';
import ItemsList from '../pages/Inventory/Items';
import Categories from '../pages/Inventory/Categories';
import Locations from '../pages/Inventory/Locations';
import InventoryHistory from '../pages/Inventory/History';

import ProductsDashboard from '../pages/Products';
import ProductMasterData from '../pages/Products/MasterData';
import ProductCatalog from '../pages/Products/Catalog';
import ProductMovements from '../pages/Products/Movements';
import MovementCreate from '../pages/Products/MovementCreate';

import ProductStockOverview from '../pages/Products/StockOverview';
import Placements from '../pages/Products/Placements';
import BarcodeCenter from '../pages/Products/BarcodeCenter';

import ScannerLayout from '../layouts/ScannerLayout';
import ScannerApp from '../pages/Scanner/ScannerApp';

import Reports from '../pages/Reports';
import Users from '../pages/Users';
import Profile from '../pages/Profile';
import WorkWorkspace from '../pages/Work';
import ActivityLog from '../pages/Logs/ActivityLog';
import AuditLog from '../pages/Logs/AuditLog';
import BackupManager from '../pages/System/BackupManager';

// import ShowroomDashboard from '../modules/showroom/pages/Dashboard';
import ShowroomLayout from '../layouts/ShowroomLayout';
import ShowroomRoutes from '../modules/showroom/routes';
import ScanLocation from '../pages/ScanLocation';

import { useAuth } from '../contexts/AuthContext';



const HomeRedirect = () => {
  const { user } = useAuth();
  if (user?.role?.name === 'ADMIN') {
    return <Navigate to="/dashboard" replace />;
  }
  return <Navigate to="/work" replace />;
};

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      {/* Protected Routes (Main App Shell) */}
      <Route element={<ProtectedRoute />}>
        <Route element={<MainLayout />}>

          <Route path="/" element={<HomeRedirect />} />

          <Route element={<ProtectedRoute permission="DASHBOARD" />}>
            <Route path="/dashboard" element={<Dashboard />} />
          </Route>

          <Route element={<ProtectedRoute permission="WORK" />}>
            <Route path="/work" element={<WorkWorkspace />} />
          </Route>
          
          {/* Inventory Routes */}
          <Route element={<ProtectedRoute permission="INVENTORY" />}>
            <Route path="inventory">
              <Route index element={<InventoryDashboard />} />
              <Route path="items" element={<ItemsList />} />
              <Route path="history" element={<InventoryHistory />} />
              <Route path="categories" element={<Categories />} />
              <Route path="locations" element={<Locations />} />
            </Route>
          </Route>

          {/* Scanner Routes for V1 (Deleted/Moved to V2 Scanner Layout) */}

          {/* Products Routes */}
          <Route element={<ProtectedRoute permission="PRODUCTS" />}>
            <Route path="products">
              <Route index element={<ProductsDashboard />} />
              <Route path="stock" element={<ProductStockOverview />} />
              <Route path="catalog" element={<ProductCatalog />} />
              <Route path="movements" element={<ProductMovements />} />
              <Route path="movements/create" element={<MovementCreate />} />
              <Route path="master-data" element={<ProductMasterData />} />
              <Route path="placements" element={<Placements />} />
              <Route path="barcode-center" element={<BarcodeCenter />} />
            </Route>
          </Route>



          <Route element={<ProtectedRoute permission="USERS" />}>
            <Route path="/reports" element={<Reports />} />
          </Route>

          <Route element={<ProtectedRoute permission="USERS" />}>
            <Route path="/users" element={<Users />} />
          </Route>

          <Route element={<ProtectedRoute permission="USERS" />}>
            <Route path="/logs/activity" element={<ActivityLog />} />
            <Route path="/logs/audit" element={<AuditLog />} />
            <Route path="/system/backups" element={<BackupManager />} />
          </Route>
          
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Navigate to="/profile" replace />} />
        </Route>

        <Route element={<ScannerLayout />}>
          <Route element={<ProtectedRoute permission="PRODUCTS" />}>
            <Route path="/scanner" element={<ScannerApp />} />
            
          </Route>
        </Route>
      </Route>
      
      {/* 404 Catch All */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />

      {/* Public Scan Page (no auth) */}
      <Route path="/scan/:code" element={<ScanLocation />} />

      {/* SHOWROOM */}
      <Route element={<ShowroomLayout />}>
        <Route element={<ProtectedRoute permission="SHOWROOM" />}>
          <Route path="/showroom/*" element={<ShowroomRoutes />} />
        </Route>
      </Route>
      
    </Routes>
  );
};

export default AppRoutes;
