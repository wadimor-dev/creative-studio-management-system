import React from 'react';
import Card from '../../../components/common/Card';
import Badge from '../../../components/common/Badge';

const RecentTransactions = ({ data }) => {
  return (
    <Card className="overflow-hidden">
      <div className="px-6 py-5 border-b border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900">Recent Transactions</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Type</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Item</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Qty</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Location (Src → Dest)</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">User</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {data.slice(0, 5).map((tx) => (
              <tr key={tx.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{new Date(tx.date || tx.created_at).toLocaleDateString()}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  <Badge variant={tx.type === 'IN' ? 'success' : tx.type === 'TRANSFER' ? 'info' : tx.type === 'OUT' ? 'warning' : 'default'}>
                    {tx.type}
                  </Badge>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                  {tx.item?.sku} - {tx.item?.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500 font-medium">{tx.quantity}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                  {tx.source_location?.name || '-'} → {tx.destination_location?.name || '-'}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">{tx.user?.username || tx.user?.email || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
};

export default RecentTransactions;
