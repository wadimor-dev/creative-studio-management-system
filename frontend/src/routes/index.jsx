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
import ProductStockOverview from '../pages/Products/StockOverview';

import Reports from '../pages/Reports';
import Users from '../pages/Users';
import Profile from '../pages/Profile';
import WorkWorkspace from '../pages/Work';
import { useAuth } from '../contexts/AuthContext';



const HomeRedirect = () => {
  const { user } = useAuth();
  if (user?.role?.name === 'STAFF') {
    return <Navigate to="/work" replace />;
  }
  return <Navigate to="/dashboard" replace />;
};

const AppRoutes = () => {
  const { user } = useAuth();
  
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
          <Route path="/work" element={<WorkWorkspace />} />
          
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

          {/* Products Routes */}
        <Route path="products">
          <Route index element={<ProductsDashboard />} />
          <Route path="stock" element={<ProductStockOverview />} />
          <Route path="catalog" element={<ProductCatalog />} />
          <Route path="movements" element={<ProductMovements />} />
          <Route path="master-data" element={<ProductMasterData />} />
        </Route>

        <Route path="/reports" element={<Reports />} />
          <Route element={<ProtectedRoute permission="USERS" />}>
            <Route path="/users" element={<Users />} />
          </Route>
          <Route path="/profile" element={<Profile />} />
          <Route path="/settings" element={<Navigate to="/profile" replace />} />
        </Route>
      </Route>
      
      {/* 404 Catch All */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
};

export default AppRoutes;
