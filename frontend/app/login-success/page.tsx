'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function LoginSuccess() {
  const router = useRouter();

  useEffect(() => {
    // Get token from URL
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');

    if (token) {
      // Store token in localStorage and cookie
      localStorage.setItem('auth_token', token);
      document.cookie = `auth_token=${token}; path=/`;
      // Redirect to dashboard
      router.push('/dashboard');
    } else {
      // If no token, redirect to home
      router.push('/');
    }
  }, [router]);

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="text-center">
        <h1 className="text-2xl font-semibold">Processing login...</h1>
        <p className="mt-2 text-gray-600">Please wait while we complete your authentication.</p>
      </div>
    </div>
  );
} 