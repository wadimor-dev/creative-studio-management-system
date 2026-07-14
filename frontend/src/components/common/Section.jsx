import React from 'react';

const Section = ({ title, description, children, className = '', action }) => {
  return (
    <section className={`mb-8 ${className}`}>
      {(title || description || action) && (
        <div className="mb-4 flex items-center justify-between">
          <div>
            {title && <h2 className="text-lg font-semibold text-slate-900">{title}</h2>}
            {description && <p className="text-sm text-slate-500 mt-1">{description}</p>}
          </div>
          {action && <div>{action}</div>}
        </div>
      )}
      {children}
    </section>
  );
};

export default Section;
