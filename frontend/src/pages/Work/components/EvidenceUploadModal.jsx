import React, { useState } from 'react';
import Button from '../../../components/common/Button';

const EvidenceUploadModal = ({ isOpen, onClose, type, activityId, title, buttonLabel, onSubmit }) => {
  const [file, setFile] = useState(null);
  const [description, setDescription] = useState('');
  const [preview, setPreview] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [assets, setAssets] = useState([]);

  if (!isOpen) return null;

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(selected);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit(activityId, type, file, description, assets);
      // Reset after success
      setFile(null);
      setPreview(null);
      setDescription('');
      setAssets([]);
      onClose();
    } catch (error) {
      console.error('Upload failed', error);
      // Here you could add a toast error message
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setFile(null);
    setPreview(null);
    setDescription('');
    setAssets([]);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
      <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl dark:bg-gray-800">
        <h3 className="mb-4 text-xl font-bold text-gray-900 dark:text-white">{title}</h3>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Ambil Foto (Kamera)
            </label>
            <div className="mt-1 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10 dark:border-gray-600">
              <div className="text-center">
                {preview ? (
                  <img src={preview} alt="Preview" className="mx-auto h-48 rounded-lg object-cover" />
                ) : (
                  <svg className="mx-auto h-12 w-12 text-gray-300" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                    <path fillRule="evenodd" d="M1.5 6a2.25 2.25 0 012.25-2.25h16.5A2.25 2.25 0 0122.5 6v12a2.25 2.25 0 01-2.25 2.25H3.75A2.25 2.25 0 011.5 18V6zM3 16.06V18c0 .414.336.75.75.75h16.5A.75.75 0 0021 18v-1.94l-2.69-2.689a1.5 1.5 0 00-2.12 0l-.88.879.97.97a.75.75 0 11-1.06 1.06l-5.16-5.159a1.5 1.5 0 00-2.12 0L3 16.061zm10.125-7.81a1.125 1.125 0 112.25 0 1.125 1.125 0 01-2.25 0z" clipRule="evenodd" />
                  </svg>
                )}
                <div className="mt-4 flex text-sm leading-6 text-gray-600 dark:text-gray-400">
                  <label htmlFor="file-upload" className="relative cursor-pointer rounded-md bg-white font-semibold text-primary-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-primary-600 focus-within:ring-offset-2 hover:text-primary-500 dark:bg-gray-800 dark:text-primary-400">
                    <span>Pilih Foto atau Buka Kamera</span>
                    <input 
                      id="file-upload" 
                      name="file-upload" 
                      type="file" 
                      className="sr-only" 
                      accept="image/*" 
                      capture="environment"
                      onChange={handleFileChange}
                    />
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Catatan (Opsional)
            </label>
            <textarea
              className="w-full rounded-xl border border-gray-300 p-3 text-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              rows="2"
              placeholder="Tambahkan catatan jika diperlukan..."
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />
          </div>

          
          {type === 'BEFORE' && (
            <div className="rounded-xl border border-gray-200 bg-gray-50 p-4 dark:border-gray-700 dark:bg-gray-900/50">
              <h4 className="mb-3 text-sm font-medium text-gray-900 dark:text-white">Pinjam Asset (Opsional)</h4>
              
              {assets.map((a, index) => (
                <div key={index} className="mb-2 flex gap-2">
                  <input type="number" placeholder="Item ID" value={a.item_id} onChange={(e) => {
                    const newAssets = [...assets];
                    newAssets[index].item_id = parseInt(e.target.value) || '';
                    setAssets(newAssets);
                  }} className="w-1/2 rounded-lg border-gray-300 text-sm dark:bg-gray-800 dark:text-white" />
                  
                  <input type="number" placeholder="Location ID" value={a.location_id} onChange={(e) => {
                    const newAssets = [...assets];
                    newAssets[index].location_id = parseInt(e.target.value) || '';
                    setAssets(newAssets);
                  }} className="w-1/4 rounded-lg border-gray-300 text-sm dark:bg-gray-800 dark:text-white" />
                  
                  <input type="number" placeholder="Qty" value={a.quantity} onChange={(e) => {
                    const newAssets = [...assets];
                    newAssets[index].quantity = parseInt(e.target.value) || '';
                    setAssets(newAssets);
                  }} className="w-1/4 rounded-lg border-gray-300 text-sm dark:bg-gray-800 dark:text-white" />
                </div>
              ))}
              
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setAssets([...assets, { item_id: '', location_id: 1, quantity: 1 }])}
                className="mt-2"
              >
                + Tambah Asset
              </Button>
            </div>
          )}
          
          {type === 'AFTER' && (
            <div className="rounded-xl border border-blue-100 bg-blue-50 p-4 dark:border-blue-900/30 dark:bg-blue-900/10">
              <p className="text-sm text-blue-800 dark:text-blue-300">
                <span className="font-medium">Info:</span> Semua asset yang Anda pinjam pada sesi ini akan dikembalikan secara otomatis.
              </p>
            </div>
          )}

          <div className="mt-6 flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              size="md"
              onClick={handleClose}
              disabled={isSubmitting}
            >
              Batal
            </Button>
            <Button
              type="submit"
              variant="primary"
              size="md"
              disabled={!file || isSubmitting}
              isLoading={isSubmitting}
            >
              {isSubmitting ? 'Mengunggah...' : buttonLabel}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EvidenceUploadModal;
