import React from 'react';
import AppRoutes from './routes';
import { AuthProvider } from './contexts/AuthContext';
import ErrorBoundary from './components/common/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </ErrorBoundary>
  );
}

export default App;
