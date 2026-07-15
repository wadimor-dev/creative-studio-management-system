import React, { useState } from 'react';
import PageHeader from '../../components/common/PageHeader';
import Button from '../../components/common/Button';
import Modal from '../../components/common/Modal';
import LoadingSpinner from '../../components/common/LoadingSpinner';
import { Plus, Edit2, Trash2, ChevronRight, ChevronDown, Folder, MapPin } from 'lucide-react';
import { toastSuccess, toastError } from '../../utils/toast';

import ProductsTabs from './components/ProductsTabs';
import { usePlacements } from '../../hooks/usePlacements';
import { placementService } from '../../api/services/placementService';

const PlacementNode = ({ node, level = 0, onEdit, onDelete, onAddChild }) => {
  const [expanded, setExpanded] = useState(true);
  const hasChildren = node.children && node.children.length > 0;

  return (
    <div className="w-full">
      <div 
        className={`flex items-center justify-between p-2 border-b border-slate-100 hover:bg-slate-50 transition-colors ${level === 0 ? 'bg-slate-50/50' : ''}`}
        style={{ paddingLeft: `${level * 24 + 16}px` }}
      >
        <div className="flex items-center gap-2">
          {hasChildren ? (
            <button onClick={() => setExpanded(!expanded)} className="p-1 text-slate-400 hover:text-slate-600">
              {expanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
            </button>
          ) : (
            <div className="w-6" /> // spacer
          )}
          
          {level === 0 ? <Folder size={16} className="text-brand-500" /> : <MapPin size={16} className="text-slate-400" />}
          
          <div className="flex flex-col">
            <span className="font-medium text-slate-700">{node.name}</span>
            {node.code && <span className="text-xs text-slate-400 font-mono">{node.code}</span>}
          </div>
          
          <span className="ml-2 text-xs px-2 py-0.5 bg-slate-100 text-slate-600 rounded-full">
            Level {node.level}
          </span>
          <span className="ml-2 text-xs px-2 py-0.5 bg-blue-50 text-blue-600 rounded-full border border-blue-100">
            {node.placement_type?.name || 'Unknown Type'}
          </span>
        </div>

        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity" style={{ opacity: 1 }}>
          <button 
            onClick={() => onAddChild(node)}
            className="p-1.5 text-slate-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
            title="Add Sub-Placement"
          >
            <Plus size={16} />
          </button>
          <button 
            onClick={() => onEdit(node)}
            className="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors"
            title="Edit"
          >
            <Edit2 size={16} />
          </button>
          <button 
            onClick={() => onDelete(node.id)}
            className="p-1.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
            title="Delete"
          >
            <Trash2 size={16} />
          </button>
        </div>
      </div>
      
      {expanded && hasChildren && (
        <div className="flex flex-col w-full">
          {node.children.map(child => (
            <PlacementNode 
              key={child.id} 
              node={child} 
              level={level + 1} 
              onEdit={onEdit} 
              onDelete={onDelete} 
              onAddChild={onAddChild} 
            />
          ))}
        </div>
      )}
    </div>
  );
};

const PlacementForm = ({ initialData, parentData, types, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    name: initialData?.name || '',
    code: initialData?.code || '',
    type_id: initialData?.type_id || (types.length > 0 ? types[0].id : ''),
    parent_id: initialData?.parent_id || parentData?.id || null,
    level: initialData?.level || (parentData ? parentData.level + 1 : 1),
    is_active: initialData?.is_active ?? true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {parentData && (
        <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 mb-4">
          <p className="text-xs text-slate-500 mb-1">Parent Placement</p>
          <p className="font-medium text-slate-700">{parentData.name}</p>
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Name *</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
          required
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Code (Barcode)</label>
        <input
          type="text"
          value={formData.code}
          onChange={(e) => setFormData({...formData, code: e.target.value})}
          className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 font-mono text-sm"
          placeholder="e.g. RAK-A01"
        />
        <p className="text-xs text-slate-500 mt-1">Leave empty to autogenerate or if not needed.</p>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Placement Type *</label>
          <select
            value={formData.type_id}
            onChange={(e) => setFormData({...formData, type_id: parseInt(e.target.value)})}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500"
            required
          >
            {types.map(t => (
              <option key={t.id} value={t.id}>{t.name}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Level</label>
          <input
            type="number"
            value={formData.level}
            onChange={(e) => setFormData({...formData, level: parseInt(e.target.value)})}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20 focus:border-brand-500 bg-slate-50"
            required
            readOnly
          />
        </div>
      </div>

      <div className="flex items-center gap-2 mt-2">
        <input
          type="checkbox"
          id="is_active"
          checked={formData.is_active}
          onChange={(e) => setFormData({...formData, is_active: e.target.checked})}
          className="rounded border-slate-300 text-brand-600 focus:ring-brand-500"
        />
        <label htmlFor="is_active" className="text-sm text-slate-700">Active</label>
      </div>

      <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-slate-200">
        <Button variant="outline" type="button" onClick={onCancel}>Cancel</Button>
        <Button variant="primary" type="submit">Save Placement</Button>
      </div>
    </form>
  );
};

const PlacementTypesModal = ({ isOpen, onClose, types, refetch }) => {
  const [newTypeName, setNewTypeName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleAddType = async (e) => {
    e.preventDefault();
    if (!newTypeName.trim()) return;
    
    setIsSubmitting(true);
    try {
      const res = await placementService.createType({ name: newTypeName });
      if (res.success) {
        toastSuccess('Type added successfully');
        setNewTypeName('');
        refetch(); // This will refresh the types in the parent component
      } else {
        toastError(res.message);
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Manage Placement Types">
      <div className="space-y-4">
        <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
          <h4 className="text-sm font-medium text-slate-700 mb-2">Existing Types</h4>
          {types.length === 0 ? (
            <p className="text-xs text-slate-500">No types created yet.</p>
          ) : (
            <div className="flex flex-wrap gap-2">
              {types.map(t => (
                <span key={t.id} className="px-2 py-1 bg-white border border-slate-200 rounded text-sm text-slate-600 shadow-sm">
                  {t.name}
                </span>
              ))}
            </div>
          )}
        </div>
        
        <form onSubmit={handleAddType} className="space-y-3 pt-2">
          <label className="block text-sm font-medium text-slate-700">Add New Type</label>
          <div className="flex gap-2">
            <input
              type="text"
              value={newTypeName}
              onChange={(e) => setNewTypeName(e.target.value)}
              placeholder="e.g. Warehouse, Showroom, Rak"
              className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              required
            />
            <Button type="submit" variant="primary" disabled={isSubmitting}>
              Add
            </Button>
          </div>
        </form>
        
        <div className="flex justify-end pt-4 mt-2 border-t border-slate-100">
          <Button variant="outline" onClick={onClose}>Close</Button>
        </div>
      </div>
    </Modal>
  );
};

const Placements = () => {
  const { placements, types, loading, refetch } = usePlacements(true); // true = fetch hierarchy
  const [modalState, setModalState] = useState({ isOpen: false, data: null, parentData: null });
  const [typesModalOpen, setTypesModalOpen] = useState(false);

  const openModal = (data = null, parentData = null) => {
    if (types.length === 0) {
      toastError("Please create at least one Placement Type first!");
      setTypesModalOpen(true);
      return;
    }
    setModalState({ isOpen: true, data, parentData });
  };
  const closeModal = () => setModalState({ isOpen: false, data: null, parentData: null });

  const handleSubmit = async (data) => {
    try {
      const res = modalState.data
        ? await placementService.update(modalState.data.id, data)
        : await placementService.create(data);

      if (res.success) {
        toastSuccess(`Placement ${modalState.data ? 'updated' : 'created'} successfully!`);
        closeModal();
        refetch();
      } else {
        toastError(res.message || "Failed to save placement");
      }
    } catch (err) {
      toastError(err.response?.data?.message || err.message || "An error occurred");
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete this placement?")) {
      try {
        const res = await placementService.delete(id);
        if (res.success) {
          toastSuccess("Placement deleted successfully");
          refetch();
        } else {
          toastError(res.message);
        }
      } catch (err) {
        toastError(err.response?.data?.message || err.message);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-full min-h-[400px]">
        <LoadingSpinner size="lg" text="Loading placements..." />
      </div>
    );
  }

  return (
    <div>
      <PageHeader 
        title="Products" 
        description="Manage product catalog, stock, and placements."
      />
      
      <ProductsTabs />

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex justify-between items-center bg-slate-50">
          <h3 className="font-semibold text-slate-800">Placement Hierarchy</h3>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={() => setTypesModalOpen(true)}>
              Manage Types
            </Button>
            <Button variant="primary" size="sm" className="gap-2" onClick={() => openModal()}>
              <Plus size={16} />
              Add Root Placement
            </Button>
          </div>
        </div>
        
        <div className="flex flex-col">
          {placements.length > 0 ? (
            placements.map(rootNode => (
              <PlacementNode 
                key={rootNode.id} 
                node={rootNode} 
                level={0}
                onEdit={(data) => openModal(data, null)}
                onDelete={handleDelete}
                onAddChild={(parent) => openModal(null, parent)}
              />
            ))
          ) : (
            <div className="p-8 text-center text-slate-500">
              No placements found. Create a root placement to get started.
            </div>
          )}
        </div>
      </div>

      <Modal 
        isOpen={modalState.isOpen} 
        onClose={closeModal} 
        title={modalState.data ? 'Edit Placement' : (modalState.parentData ? 'Add Sub-Placement' : 'New Root Placement')}
      >
        <PlacementForm 
          initialData={modalState.data}
          parentData={modalState.parentData}
          types={types}
          onSubmit={handleSubmit} 
          onCancel={closeModal} 
        />
      </Modal>

      <PlacementTypesModal 
        isOpen={typesModalOpen} 
        onClose={() => setTypesModalOpen(false)} 
        types={types} 
        refetch={refetch} 
      />

    </div>
  );
};

export default Placements;
