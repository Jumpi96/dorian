'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  login: () => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if the auth_token cookie exists
    const checkAuth = async () => {
      console.log('Auth check - Starting client-side auth check');
      try {
        console.log('Auth check - Making request to /api/auth/check');
        const response = await fetch('/api/auth/check', {
          credentials: 'include', // Important: This ensures cookies are sent
        });
        console.log('Auth check - Response status:', response.status);
        setIsAuthenticated(response.ok);
      } catch (error) {
        console.error('Auth check - Error during auth check:', error);
        setIsAuthenticated(false);
      }
    };
    
    checkAuth();
  }, []);

  const login = () => {
    window.location.href = `${process.env.NEXT_PUBLIC_API_URL}/auth/login`;
  };

  const logout = async () => {
    try {
      await fetch('/api/auth/logout', {
        method: 'POST',
        credentials: 'include',
      });
    } finally {
      setIsAuthenticated(false);
    }
  };

  return React.createElement(
    AuthContext.Provider,
    { value: { isAuthenticated, login, logout } },
    children
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 