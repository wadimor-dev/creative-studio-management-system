import React from 'react';

const DashboardSection = ({ title, description, children }) => {
  return (
    <section className="mb-5 sm:mb-8">
      <div className="mb-4">
        {title && <h2 className="text-lg font-semibold text-slate-900">{title}</h2>}
        {description && <p className="text-sm text-slate-500 mt-1">{description}</p>}
      </div>
      {children}
    </section>
  );
};

export default DashboardSection;
