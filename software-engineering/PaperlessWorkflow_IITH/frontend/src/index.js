import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import './index.css'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <LocalizationProvider dateAdapter={AdapterDayjs}>
  <GoogleOAuthProvider clientId='112391562895-h6drpui9566iqthca1uc8c43u6u5c0ru.apps.googleusercontent.com'>
    <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
    </React.StrictMode>
  </GoogleOAuthProvider>
  </LocalizationProvider>
);

