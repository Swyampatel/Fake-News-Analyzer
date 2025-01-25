import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import FakeNewsDashboard from './FakeNewsDashboard';

// Suppress ResizeObserver Error
const resizeObserverError = window.ResizeObserver.prototype.observe;
window.ResizeObserver.prototype.observe = function () {
  try {
    resizeObserverError.apply(this, arguments);
  } catch (e) {
    console.warn('ResizeObserver Error suppressed:', e);
  }
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <FakeNewsDashboard />
  </React.StrictMode>
);
