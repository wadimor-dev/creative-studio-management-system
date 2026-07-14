import api from '../api/axios';

const workEvidenceService = {
  uploadEvidence: async (activityId, type, file, description) => {
    const formData = new FormData();
    formData.append('type', type);
    formData.append('file', file);
    if (description) {
      formData.append('description', description);
    }

    const response = await api.post(`/work-activities/${activityId}/evidence`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response;
  },
  getEvidences: async (activityId) => {
    const response = await api.get(`/work-activities/${activityId}/evidences`);
    return response;
  },
};

export default workEvidenceService;
