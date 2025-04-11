import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Optional: If you have a custom stylesheet
import App from './App';  // Your main App component

// Render the app in the 'root' div element in index.html
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);