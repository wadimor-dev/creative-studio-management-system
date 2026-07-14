import React from 'react';
import Button from './Button';
import { AlertOctagon } from 'lucide-react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen items-center justify-center bg-slate-50 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-8 text-center shadow-lg border border-slate-100">
            <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-rose-100 mb-6">
              <AlertOctagon size={32} className="text-rose-600" />
            </div>
            <h1 className="text-2xl font-bold text-slate-900 mb-2">Oops! Something went wrong.</h1>
            <p className="text-slate-500 mb-8">
              We encountered an unexpected error. Our team has been notified. Please try refreshing the page.
            </p>
            <Button 
              variant="primary" 
              className="w-full justify-center"
              onClick={() => window.location.reload()}
            >
              Refresh Page
            </Button>
            {process.env.NODE_ENV === 'development' && (
              <div className="mt-6 text-left">
                <p className="text-xs font-mono text-rose-500 bg-rose-50 p-3 rounded-lg overflow-auto">
                  {this.state.error?.toString()}
                </p>
              </div>
            )}
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
