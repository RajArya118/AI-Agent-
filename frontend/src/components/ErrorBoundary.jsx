import React from 'react';
import { AlertTriangle, RotateCw } from 'lucide-react';

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('BuildPilot Frontend Caught Exception:', error, errorInfo);
  }

  handleReload = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen w-screen flex items-center justify-center bg-gray-50 dark:bg-neutral-900 p-6">
          <div className="max-w-md w-full bg-white dark:bg-neutral-800 rounded-3xl border border-gray-200 dark:border-neutral-700 p-8 shadow-xl text-center space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-amber-500/10 text-amber-500 flex items-center justify-center mx-auto">
              <AlertTriangle className="w-8 h-8" />
            </div>
            <h2 className="text-xl font-extrabold text-gray-900 dark:text-gray-100">
              Something went wrong
            </h2>
            <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
              BuildPilot encountered an unexpected runtime error. You can reload the application to restore state.
            </p>
            {this.state.error?.message && (
              <pre className="p-3 rounded-xl bg-gray-100 dark:bg-neutral-900 text-left text-[11px] font-mono text-red-500 overflow-auto max-h-32">
                {this.state.error.message}
              </pre>
            )}
            <button
              onClick={this.handleReload}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold transition-all shadow-md"
            >
              <RotateCw className="w-4 h-4" />
              <span>Reload Application</span>
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
