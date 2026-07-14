import api from '../axios';
import { ENDPOINTS } from '../endpoints';

export const reportService = {
  getReports: async (params) => {
    // params can include: type, date, month, year, user_id, category_id, status, division, page, size
    return api.get(ENDPOINTS.REPORTS, { params });
  }
};
