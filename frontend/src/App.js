import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { AuthProvider } from './contexts/AuthContext';
import { theme, GlobalStyle } from './theme';
import PrivateRoute from './components/PrivateRoute';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import CreateAgreement from './components/CreateAgreement';
import { login } from './services/api';
import Clients from './components/Clients';

function App() {
  useEffect(() => {
    const testApiConnection = async () => {
      try {
        const response = await login('username', 'password');
        console.log('API connection successful:', response.data);
      } catch (error) {
        console.error('API connection failed:', error);
      }
    };

    testApiConnection();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <AuthProvider>
        <Router>
          <GlobalStyle />
          <Navbar />
          <div className="App">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route 
                path="/dashboard" 
                element={
                  <PrivateRoute>
                    <Dashboard />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/profile" 
                element={
                  <PrivateRoute>
                    <Profile />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/create-agreement" 
                element={
                  <PrivateRoute>
                    <CreateAgreement />
                  </PrivateRoute>
                } 
              />
              <Route 
                path="/clients" 
                element={
                  <PrivateRoute>
                    <Clients />
                  </PrivateRoute>
                } 
              />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;