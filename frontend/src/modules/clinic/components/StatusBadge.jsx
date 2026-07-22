import React from 'react';
import { visitStatusBadge, visitStatusLabel } from '../helpers';

const StatusBadge = ({ status }) => (
  <span
    className={`inline-block px-2 py-0.5 rounded text-xs font-medium ${visitStatusBadge(status)}`}
  >
    {visitStatusLabel(status)}
  </span>
);

export default StatusBadge;
