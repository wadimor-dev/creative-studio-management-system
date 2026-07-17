import React from 'react';
import Modal from '../../../components/common/Modal';
import Button from '../../../components/common/Button';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Textarea from '../../../components/common/Textarea';
import { X, Plus, Trash2 } from 'lucide-react';

const TransferForm = ({ isOpen, onClose, onSubmit }) => {
  const [formData, setFormData] = React.useState({
    fromLocation: '',
    toLocation: '',
    items: [{ product: '', quantity: '' }],
    estimatedArrival: '',
    notes: '',
  });

  const [errors, setErrors] = React.useState({});

  const locations = [
    { value: '', label: 'Pilih Lokasi' },
    { value: 'showroom-utama', label: 'Showroom Utama' },
    { value: 'cabang-a', label: 'Cabang A' },
    { value: 'cabang-b', label: 'Cabang B' },
    { value: 'gudang', label: 'Gudang' },
  ];

  const products = [
    { value: '', label: 'Pilih Produk' },
    { value: 'sku-001', label: 'Kain Batik Motif X' },
    { value: 'sku-002', label: 'Kain Tenun Ikat' },
    { value: 'sku-003', label: 'Songket Palembang' },
    { value: 'sku-004', label: 'Ulos Batak' },
    { value: 'sku-005', label: 'Batik Tulis Solo' },
  ];

  const handleInputChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    setErrors(prev => ({ ...prev, [field]: '' }));
  };

  const handleItemChange = (index, field, value) => {
    const newItems = [...formData.items];
    newItems[index][field] = value;
    setFormData(prev => ({ ...prev, items: newItems }));
  };

  const addItem = () => {
    setFormData(prev => ({
      ...prev,
      items: [...prev.items, { product: '', quantity: '' }]
    }));
  };

  const removeItem = (index) => {
    if (formData.items.length > 1) {
      const newItems = formData.items.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, items: newItems }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.fromLocation) newErrors.fromLocation = 'Lokasi asal wajib diisi';
    if (!formData.toLocation) newErrors.toLocation = 'Lokasi tujuan wajib diisi';
    if (formData.fromLocation === formData.toLocation) {
      newErrors.toLocation = 'Lokasi tujuan tidak boleh sama dengan lokasi asal';
    }
    if (!formData.estimatedArrival) newErrors.estimatedArrival = 'Estimasi tiba wajib diisi';
    
    formData.items.forEach((item, index) => {
      if (!item.product) {
        newErrors[`item_${index}_product`] = 'Produk wajib dipilih';
      }
      if (!item.quantity || parseInt(item.quantity) <= 0) {
        newErrors[`item_${index}_quantity`] = 'Quantity harus lebih dari 0';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
      handleClose();
    }
  };

  const handleClose = () => {
    setFormData({
      fromLocation: '',
      toLocation: '',
      items: [{ product: '', quantity: '' }],
      estimatedArrival: '',
      notes: '',
    });
    setErrors({});
    onClose();
  };

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Transfer Stok Baru">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-1">
              Dari Lokasi *
            </label>
            <Select
              value={formData.fromLocation}
              onChange={(e) => handleInputChange('fromLocation', e.target.value)}
              options={locations}
              error={errors.fromLocation}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-1">
              Ke Lokasi *
            </label>
            <Select
              value={formData.toLocation}
              onChange={(e) => handleInputChange('toLocation', e.target.value)}
              options={locations}
              error={errors.toLocation}
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-1">
            Estimasi Tiba *
          </label>
          <Input
            type="date"
            value={formData.estimatedArrival}
            onChange={(e) => handleInputChange('estimatedArrival', e.target.value)}
            error={errors.estimatedArrival}
          />
        </div>

        <div>
          <div className="flex items-center justify-between mb-2">
            <label className="block text-sm font-medium text-neutral-700">
              Items *
            </label>
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={addItem}
              className="gap-1"
            >
              <Plus size={14} />
              Tambah Item
            </Button>
          </div>
          
          <div className="space-y-2">
            {formData.items.map((item, index) => (
              <div key={index} className="flex gap-2 items-start">
                <div className="flex-1">
                  <Select
                    value={item.product}
                    onChange={(e) => handleItemChange(index, 'product', e.target.value)}
                    options={products}
                    error={errors[`item_${index}_product`]}
                  />
                </div>
                <div className="w-32">
                  <Input
                    type="number"
                    placeholder="Qty"
                    value={item.quantity}
                    onChange={(e) => handleItemChange(index, 'quantity', e.target.value)}
                    error={errors[`item_${index}_quantity`]}
                  />
                </div>
                {formData.items.length > 1 && (
                  <Button
                    type="button"
                    variant="delete"
                    size="sm"
                    onClick={() => removeItem(index)}
                  >
                    <Trash2 size={14} />
                  </Button>
                )}
              </div>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-neutral-700 mb-1">
            Catatan
          </label>
          <Textarea
            rows={3}
            value={formData.notes}
            onChange={(e) => handleInputChange('notes', e.target.value)}
            placeholder="Tambahkan catatan untuk transfer ini..."
          />
        </div>

        <div className="flex justify-end gap-2 pt-4 border-t border-stone-200">
          <Button type="button" variant="outline" onClick={handleClose}>
            Batal
          </Button>
          <Button type="submit" variant="primary">
            Buat Transfer
          </Button>
        </div>
      </form>
    </Modal>
  );
};

export default TransferForm;
