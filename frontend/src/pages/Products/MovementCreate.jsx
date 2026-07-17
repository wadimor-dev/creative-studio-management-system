// pages/Products/MovementCreate.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';

import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import { toastSuccess, toastError } from '../../utils/toast';

import MovementForm from './components/MovementForm';
import { productMovementService } from '../../api/services/productMovementService';

const MovementCreate = () => {
  const navigate = useNavigate();

  const handleFormSubmit = async (formData) => {
    try {
      const res = await productMovementService.create(formData);
      if (res.success) {
        toastSuccess('Movement recorded successfully!');
        navigate('/products/movements');
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Record Movement"
        description="Manually record a stock in, out, or transfer for a product."
        actions={
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => navigate('/products/movements')}
          >
            <ArrowLeft size={16} />
            Back to Movements
          </Button>
        }
      />

      <div className="rounded-xl border border-slate-200 bg-white p-6">
        <MovementForm
          onSubmit={handleFormSubmit}
          onCancel={() => navigate('/products/movements')}
        />
      </div>
    </div>
  );
};

export default MovementCreate;