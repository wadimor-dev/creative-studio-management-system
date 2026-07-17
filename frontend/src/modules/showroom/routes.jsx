import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import Stock from './pages/Stock';
import Transfers from './pages/Transfers';
import StockIn from './pages/StockIn';
import StockOut from './pages/StockOut';
// import Products from './pages/Products';
// import Customers from './pages/Customers';
// import Orders from './pages/Orders';
// import Delivery from './pages/Delivery';

const ShowroomRoutes = () => (
  <Routes>
    <Route index element={<Navigate to="dashboard" replace />} />
    <Route path="dashboard" element={<Dashboard />} />
    <Route path="stock" element={<Stock />} />
    <Route path="transfers" element={<Transfers />} />
    <Route path="stock-in" element={<StockIn />} />
    <Route path="stock-out" element={<StockOut />} />
    {/* <Route path="products" element={<Products />} />
    <Route path="customers" element={<Customers />} />
    <Route path="orders" element={<Orders />} />
    <Route path="delivery" element={<Delivery />} /> */}
  </Routes>
);

export default ShowroomRoutes;