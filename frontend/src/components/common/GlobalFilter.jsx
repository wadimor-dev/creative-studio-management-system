import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import Input from './Input';
import Select from './Select';
import Button from './Button';
import { FilterX, Search, Filter } from 'lucide-react';

import { productMasterService } from '../../api/services/productMasterService';
import { userService } from '../../api/services/userService';
import { categoryService } from '../../api/services/categoryService';
import { useAuth } from '../../contexts/AuthContext';
import { hasPermission } from '../../utils/permissions';

/**
 * GlobalFilter Component
 * 
 * @param {Array} availableFilters - List of filter keys to display. Options: 
 *   ['type', 'category', 'inventory_category', 'motif', 'sub_motif', 'color', 'location', 'user', 'date']
 * @param {Function} onApply - Callback when filters are applied, receives filter object
 */
const GlobalFilter = ({ availableFilters = [], onApply }) => {
  const { register, handleSubmit, reset } = useForm();
  
  const [options, setOptions] = useState({
    types: [],
    categories: [],
    motifs: [],
    sub_motifs: [],
    colors: [],
    locations: [],
    users: [],
    inventory_categories: []
  });

  const { user } = useAuth();

  const [isExpanded, setIsExpanded] = useState(false);

  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const promises = [];
        
        // Product Master Data
        if (availableFilters.includes('type')) promises.push(productMasterService.getAllDropdown('types').then(res => ({ key: 'types', data: res.data })));
        // Categories can be product master or general categories. Product master has 'categories'
        if (availableFilters.includes('category')) promises.push(productMasterService.getAllDropdown('categories').then(res => ({ key: 'categories', data: res.data })));
        if (availableFilters.includes('inventory_category')) promises.push(categoryService.getAll().then(res => ({ key: 'inventory_categories', data: res.data })));
        if (availableFilters.includes('motif')) promises.push(productMasterService.getAllDropdown('motifs').then(res => ({ key: 'motifs', data: res.data })));
        if (availableFilters.includes('sub_motif')) promises.push(productMasterService.getAllDropdown('sub-motifs').then(res => ({ key: 'sub_motifs', data: res.data })));
        if (availableFilters.includes('color')) promises.push(productMasterService.getAllDropdown('colors').then(res => ({ key: 'colors', data: res.data })));
        
        // Locations & Users
        if (availableFilters.includes('location')) promises.push(productMasterService.getAllDropdown('locations').then(res => ({ key: 'locations', data: res.data })));

        if (
            availableFilters.includes('user') &&
            hasPermission(user, 'USERS')
        ) promises.push(userService.getUsers().then(res => ({ key: 'users', data: res.data })));

        const results = await Promise.all(promises);
        
        const newOptions = { ...options };
        results.forEach(res => {
          newOptions[res.key] = res.data;
        });
        
        setOptions(newOptions);
      } catch (err) {
        console.error("Failed to load filter options", err);
      }
    };

    fetchOptions();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [availableFilters.join(',')]);

  const handleReset = () => {
    reset();
    onApply({});
  };

  const onSubmit = (data) => {
    // Clean up empty strings
    const cleaned = Object.entries(data).reduce((acc, [key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        acc[key] = value;
      }
      return acc;
    }, {});
    
    onApply(cleaned);
  };

  // Determine grid columns based on number of active filters
  // We put at most 3 or 4 filters per row
  const activeFiltersCount = availableFilters.length;
  
  if (activeFiltersCount === 0) return null;

  return (
    <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm mb-6">
      <div className="flex items-center justify-between mb-4 cursor-pointer" onClick={() => setIsExpanded(!isExpanded)}>
        <div className="flex items-center gap-2 text-slate-800 font-medium">
          <Filter size={18} className="text-brand-500" />
          <h3>Advanced Filters</h3>
        </div>
        <div className="text-xs text-brand-600 font-medium hover:text-brand-700">
          {isExpanded ? 'Hide Filters' : 'Show Filters'}
        </div>
      </div>

      {isExpanded && (
        <form onSubmit={handleSubmit(onSubmit)}>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 items-end">
            
            {availableFilters.includes('date') && (
              <>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1.5">Start Date</label>
                  <Input type="date" className="text-sm" {...register('start_date')} />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 mb-1.5">End Date</label>
                  <Input type="date" className="text-sm" {...register('end_date')} />
                </div>
              </>
            )}

            {availableFilters.includes('type') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Product Type</label>
                <Select className="text-sm" {...register('type_id')}>
                  <option value="">All Types</option>
                  {options.types?.map(t => <option key={t.id} value={t.id}>{t.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('category') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Category</label>
                <Select className="text-sm" {...register('category_id')}>
                  <option value="">All Categories</option>
                  {options.categories?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('inventory_category') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Category</label>
                <Select className="text-sm" {...register('category_id')}>
                  <option value="">All Categories</option>
                  {options.inventory_categories?.map(opt => <option key={opt.id} value={opt.id}>{opt.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('motif') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Motif</label>
                <Select className="text-sm" {...register('motif_id')}>
                  <option value="">All Motifs</option>
                  {options.motifs?.map(m => <option key={m.id} value={m.id}>{m.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('sub_motif') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Sub Motif</label>
                <Select className="text-sm" {...register('sub_motif_id')}>
                  <option value="">All Sub Motifs</option>
                  {options.sub_motifs?.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('color') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Color</label>
                <Select className="text-sm" {...register('color_id')}>
                  <option value="">All Colors</option>
                  {options.colors?.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('location') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Location</label>
                <Select className="text-sm" {...register('location_id')}>
                  <option value="">All Locations</option>
                  {options.locations?.map(l => <option key={l.id} value={l.id}>{l.name}</option>)}
                </Select>
              </div>
            )}

            {availableFilters.includes('user') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1.5">Inputted By (User)</label>
                <Select className="text-sm" {...register('user_id')}>
                  <option value="">All Users</option>
                  {options.users?.map(u => <option key={u.id} value={u.id}>{u.full_name}</option>)}
                </Select>
              </div>
            )}
            
            <div className="flex gap-2 w-full md:col-span-full lg:col-span-1 lg:ml-auto">
              <Button type="submit" variant="primary" className="flex-1 gap-1.5" title="Apply Filters">
                <Search size={14} />
                <span className="hidden sm:inline">Apply</span>
              </Button>
              <Button type="button" variant="ghost" onClick={handleReset} className="gap-1.5 text-slate-500" title="Reset Filters">
                <FilterX size={14} />
                <span className="hidden sm:inline">Reset</span>
              </Button>
            </div>

          </div>
        </form>
      )}
    </div>
  );
};

export default GlobalFilter;
