import React from 'react';
import { Navigate } from 'react-router-dom';

const ProductsDashboard = () => {
  return <Navigate to="/products/stock" replace />;
};

export default ProductsDashboard;
