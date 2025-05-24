import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  console.error('[Auth Check] Environment:', process.env.NODE_ENV);
  console.error('[Auth Check] API URL:', process.env.NEXT_PUBLIC_API_URL);
  
  // Log all cookies for debugging
  const allCookies = request.cookies.getAll();
  console.error('[Auth Check] All cookies:', allCookies);
  
  const token = request.cookies.get('auth_token');
  console.error('[Auth Check] Token exists:', !!token);
  if (token) {
    console.error('[Auth Check] Token value:', token.value.substring(0, 10) + '...');
  }
  
  if (!token) {
    console.error('[Auth Check] No token found in cookies');
    return new NextResponse(null, { status: 401 });
  }

  try {
    const verifyUrl = `${process.env.NEXT_PUBLIC_API_URL}/auth/verify`;
    console.error('[Auth Check] Attempting to verify token with backend at:', verifyUrl);
    
    const response = await fetch(verifyUrl, {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    });

    console.error('[Auth Check] Backend verification response status:', response.status);
    
    if (!response.ok) {
      console.error('[Auth Check] Backend verification failed');
      return new NextResponse(null, { status: 401 });
    }

    console.error('[Auth Check] Authentication successful');
    return new NextResponse(null, { status: 200 });
  } catch (error) {
    console.error('[Auth Check] Error during verification:', error);
    return new NextResponse(null, { status: 401 });
  }
} 