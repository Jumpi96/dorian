import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function GET(request: NextRequest) {
  const token = request.cookies.get('auth_token');
  
  console.log('Auth check - Token exists:', !!token);
  if (token) {
    console.log('Auth check - Token value:', token.value.substring(0, 10) + '...');
  }
  
  if (!token) {
    console.log('Auth check - No token found in cookies');
    return new NextResponse(null, { status: 401 });
  }

  try {
    // Verify the token with the backend
    console.log('Auth check - Attempting to verify token with backend');
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/verify`, {
      headers: {
        'Authorization': `Bearer ${token.value}`
      }
    });

    console.log('Auth check - Backend verification response status:', response.status);
    
    if (!response.ok) {
      console.log('Auth check - Backend verification failed');
      return new NextResponse(null, { status: 401 });
    }

    console.log('Auth check - Authentication successful');
    return new NextResponse(null, { status: 200 });
  } catch (error) {
    console.error('Auth check - Error during verification:', error);
    return new NextResponse(null, { status: 401 });
  }
} 