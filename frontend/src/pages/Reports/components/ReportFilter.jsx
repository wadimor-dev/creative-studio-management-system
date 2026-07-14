import React, { useState, useEffect } from 'react';
import Input from '../../../components/common/Input';
import Select from '../../../components/common/Select';
import Button from '../../../components/common/Button';
import { FilterX, Search } from 'lucide-react';

const userOptions = [
  { value: '', label: 'All Users' },
  { value: '1', label: 'Sarah Connor' },
  { value: '2', label: 'John Doe' },
  { value: '3', label: 'Alice Smith' },
];

const categoryOptions = [
  { value: '', label: 'All Categories' },
  { value: '1', label: 'Design' },
  { value: '2', label: 'Production' },
  { value: '3', label: 'Marketing' },
];

const statusOptions = [
  { value: '', label: 'All Status' },
  { value: 'COMPLETED', label: 'Completed' },
  { value: 'WORKING', label: 'Working' },
  { value: 'PAUSED', label: 'Paused' },
];

const divisionOptions = [
  { value: '', label: 'All Divisions' },
  { value: 'Creative', label: 'Creative' },
  { value: 'Marketing', label: 'Marketing' },
  { value: 'Production', label: 'Production' },
];

const monthOptions = Array.from({ length: 12 }, (_, i) => ({
  value: `${i + 1}`,
  label: new Date(0, i).toLocaleString('en-US', { month: 'long' })
}));

const yearOptions = [
  { value: `${new Date().getFullYear() - 1}`, label: `${new Date().getFullYear() - 1}` },
  { value: `${new Date().getFullYear()}`, label: `${new Date().getFullYear()}` },
  { value: `${new Date().getFullYear() + 1}`, label: `${new Date().getFullYear() + 1}` },
];

const emptyFilters = {
  date: '',
  month: '',
  year: '',
  user_id: '',
  category_id: '',
  status: '',
  division: ''
};

const ReportFilter = ({ activePeriod, filters = {}, onChange }) => {
  const [formState, setFormState] = useState({ ...emptyFilters, ...filters });

  useEffect(() => {
    setFormState((prevState) => ({
      ...prevState,
      ...filters,
    }));
  }, [JSON.stringify(filters)]);

  useEffect(() => {
    setFormState((prevState) => ({
      ...prevState,
      date: activePeriod !== 'monthly' ? prevState.date : '',
      month: activePeriod === 'monthly' ? prevState.month : '',
      year: activePeriod === 'monthly' ? prevState.year : '',
    }));
  }, [activePeriod]);

  const handleChange = (key, value) => {
    setFormState((prevState) => ({
      ...prevState,
      [key]: value,
    }));
  };

  const handleApply = () => {
    const payload = {
      user_id: formState.user_id || undefined,
      category_id: formState.category_id || undefined,
      status: formState.status || undefined,
      division: formState.division || undefined,
    };

    if (activePeriod === 'monthly') {
      payload.month = formState.month || undefined;
      payload.year = formState.year || undefined;
    } else {
      payload.date = formState.date || undefined;
    }

    onChange(payload);
  };

  const handleReset = () => {
    setFormState({ ...emptyFilters });
    onChange({});
  };

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-3 sm:gap-4 items-end">
      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-slate-600 mb-1.5">
          {activePeriod === 'monthly' ? 'Month' : 'Date'}
        </label>
        {activePeriod === 'monthly' ? (
          <div className="grid grid-cols-2 gap-2">
            <Select
              value={formState.month}
              onChange={(e) => handleChange('month', e.target.value)}
              className="text-sm"
            >
              <option value="">Select Month</option>
              {monthOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </Select>
            <Select
              value={formState.year}
              onChange={(e) => handleChange('year', e.target.value)}
              className="text-sm"
            >
              <option value="">Select Year</option>
              {yearOptions.map((option) => (
                <option key={option.value} value={option.value}>{option.label}</option>
              ))}
            </Select>
          </div>
        ) : (
          <Input
            type="date"
            value={formState.date}
            onChange={(e) => handleChange('date', e.target.value)}
            className="text-sm"
          />
        )}
      </div>

      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-slate-600 mb-1.5">
          User (Optional)
        </label>
        <Select
          value={formState.user_id}
          onChange={(e) => handleChange('user_id', e.target.value)}
          className="text-sm"
        >
          {userOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </Select>
      </div>

      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-slate-600 mb-1.5">
          Category (Optional)
        </label>
        <Select
          value={formState.category_id}
          onChange={(e) => handleChange('category_id', e.target.value)}
          className="text-sm"
        >
          {categoryOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </Select>
      </div>

      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-slate-600 mb-1.5">
          Status (Optional)
        </label>
        <Select
          value={formState.status}
          onChange={(e) => handleChange('status', e.target.value)}
          className="text-sm"
        >
          {statusOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </Select>
      </div>

      <div className="lg:col-span-3">
        <label className="block text-xs font-medium text-slate-600 mb-1.5">
          Division (Optional)
        </label>
        <Select
          value={formState.division}
          onChange={(e) => handleChange('division', e.target.value)}
          className="text-sm"
        >
          {divisionOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </Select>
      </div>

      <div className="lg:col-span-3 flex gap-2">
        <Button variant="primary" className="flex-1 gap-1.5" title="Apply Filters" onClick={handleApply}>
          <Search size={14} />
          <span className="hidden sm:inline">Apply</span>
        </Button>
        <Button variant="ghost" className="gap-1.5 text-slate-500" title="Reset Filters" onClick={handleReset}>
          <FilterX size={14} />
          <span className="hidden sm:inline">Reset</span>
        </Button>
      </div>
    </div>
  );
};

export default ReportFilter;
