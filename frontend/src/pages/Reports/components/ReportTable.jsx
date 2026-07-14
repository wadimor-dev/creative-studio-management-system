import React, { useState } from 'react';
import Badge from '../../../components/common/Badge';
import { Camera, Eye } from 'lucide-react';
import Modal from '../../../components/common/Modal';

const ReportTable = ({ data, isLoading }) => {
  const [selectedEvidences, setSelectedEvidences] = useState(null);
  const [isEvidenceModalOpen, setIsEvidenceModalOpen] = useState(false);
  
  const [selectedDetail, setSelectedDetail] = useState(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="w-full flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-500"></div>
      </div>
    );
  }

  if (!data || data.length === 0) {
    return (
      <div className="w-full text-center py-12 text-slate-500">
        No records found for the selected period and filters.
      </div>
    );
  }

  const handleOpenEvidence = (evidences) => {
    setSelectedEvidences(evidences);
    setIsEvidenceModalOpen(true);
  };
  
  const handleOpenDetail = (item) => {
    setSelectedDetail(item);
    setIsDetailModalOpen(true);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'COMPLETED': return 'success';
      case 'WORKING': return 'info';
      case 'PAUSED': return 'warning';
      default: return 'neutral';
    }
  };

  return (
    <>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-100 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              <th className="px-6 py-4 whitespace-nowrap">Tanggal</th>
              <th className="px-6 py-4 whitespace-nowrap">Employee</th>
              <th className="px-6 py-4 whitespace-nowrap">Division</th>
              <th className="px-6 py-4 whitespace-nowrap">Category</th>
              <th className="px-6 py-4 whitespace-nowrap">Activity</th>
              <th className="px-6 py-4 whitespace-nowrap">Duration</th>
              <th className="px-6 py-4 whitespace-nowrap">Assets Used</th>
              <th className="px-6 py-4 whitespace-nowrap text-center">Evidence</th>
              <th className="px-6 py-4 whitespace-nowrap">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {data.map((item) => (
              <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                <td className="px-6 py-4 text-sm text-slate-900 whitespace-nowrap">
                  {item.date ? new Date(item.date).toLocaleDateString() : '-'}
                </td>
                <td className="px-6 py-4 text-sm font-medium text-slate-900 whitespace-nowrap">
                  {item.employee}
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 whitespace-nowrap">
                  {item.division}
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 whitespace-nowrap">
                  {item.category}
                </td>
                <td className="px-6 py-4 text-sm font-medium text-brand-600 whitespace-nowrap cursor-pointer hover:underline" onClick={() => handleOpenDetail(item)}>
                  {item.activity}
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 whitespace-nowrap">
                  {item.duration}
                </td>
                <td className="px-6 py-4 text-sm text-slate-500 whitespace-nowrap">
                  {item.assets && item.assets.length > 0 ? item.assets.join(', ') : '-'}
                </td>
                <td className="px-6 py-4 text-sm text-center whitespace-nowrap">
                  {item.evidence_count > 0 ? (
                    <button 
                      onClick={() => handleOpenEvidence(item.evidences)}
                      className="inline-flex items-center justify-center px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded text-xs transition-colors"
                    >
                      <Camera size={14} className="mr-1" /> {item.evidence_count}
                    </button>
                  ) : (
                    <span className="text-slate-300">-</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <Badge variant={getStatusColor(item.status)}>{item.status}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Evidence Modal */}
      <Modal 
        isOpen={isEvidenceModalOpen} 
        onClose={() => setIsEvidenceModalOpen(false)}
        title="Activity Evidence"
      >
        <div className="space-y-4">
          {selectedEvidences && selectedEvidences.length > 0 ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {selectedEvidences.map(ev => (
                <div key={ev.id} className="border border-slate-200 rounded-lg overflow-hidden">
                  <div className="bg-slate-50 px-3 py-2 border-b border-slate-200 flex justify-between items-center">
                    <Badge variant={ev.type === 'BEFORE' ? 'info' : (ev.type === 'AFTER' ? 'success' : 'warning')}>
                      {ev.type}
                    </Badge>
                    <span className="text-xs text-slate-500">
                      {new Date(ev.time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                  </div>
                  <div className="p-2 bg-slate-100 flex justify-center">
                    <img src={`http://localhost:8000${ev.url}`} alt={ev.type} className="max-h-48 object-contain rounded" />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-slate-500">No evidence available.</p>
          )}
        </div>
      </Modal>

      {/* Activity Detail Modal */}
      <Modal 
        isOpen={isDetailModalOpen} 
        onClose={() => setIsDetailModalOpen(false)}
        title="Activity Detail"
      >
        {selectedDetail && (
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-slate-500 uppercase">Activity Name</p>
                <p className="font-medium text-slate-900">{selectedDetail.activity}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase">Category</p>
                <p className="font-medium text-slate-900">{selectedDetail.category}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase">Start Time</p>
                <p className="font-medium text-slate-900">{selectedDetail.start_time ? new Date(selectedDetail.start_time).toLocaleString() : '-'}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase">Finish Time</p>
                <p className="font-medium text-slate-900">{selectedDetail.end_time ? new Date(selectedDetail.end_time).toLocaleString() : '-'}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase">Duration</p>
                <p className="font-medium text-slate-900">{selectedDetail.duration}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 uppercase">Status</p>
                <Badge variant={getStatusColor(selectedDetail.status)}>{selectedDetail.status}</Badge>
              </div>
            </div>
            
            <div>
              <p className="text-xs text-slate-500 uppercase mb-1">Assets Used</p>
              <div className="flex flex-wrap gap-2">
                {selectedDetail.assets && selectedDetail.assets.length > 0 ? (
                  selectedDetail.assets.map((asset, i) => (
                    <span key={i} className="px-2 py-1 bg-slate-100 border border-slate-200 rounded text-sm text-slate-700">{asset}</span>
                  ))
                ) : (
                  <span className="text-sm text-slate-500">-</span>
                )}
              </div>
            </div>
            
            <div>
              <p className="text-xs text-slate-500 uppercase mb-1">Notes</p>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <p className="text-sm text-slate-700 whitespace-pre-wrap">{selectedDetail.notes || 'No notes available.'}</p>
              </div>
            </div>
            
            <div>
              <p className="text-xs text-slate-500 uppercase mb-2">Evidence ({selectedDetail.evidence_count})</p>
              {selectedDetail.evidence_count > 0 ? (
                 <button 
                 onClick={() => handleOpenEvidence(selectedDetail.evidences)}
                 className="inline-flex items-center px-3 py-2 bg-brand-50 hover:bg-brand-100 text-brand-700 rounded-lg text-sm font-medium transition-colors"
               >
                 <Eye size={16} className="mr-2" /> View All Evidences
               </button>
              ) : (
                <span className="text-sm text-slate-500">No evidence attached.</span>
              )}
            </div>
          </div>
        )}
      </Modal>
    </>
  );
};

export default ReportTable;
