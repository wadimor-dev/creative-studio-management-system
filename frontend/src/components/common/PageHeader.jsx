import React from 'react';

const PageHeader = ({ title, description, action, actions }) => {
  const content = actions || action;
  return (
    <div className="mb-6 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900">{title}</h1>
        {description && (
          <p className="mt-1 text-sm text-slate-500">{description}</p>
        )}
      </div>
      {content && (
        <div className="flex-shrink-0">
          {content}
        </div>
      )}
    </div>
  );
};

export default PageHeader;
