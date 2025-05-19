import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  const response = new NextResponse(null, { status: 200 });
  
  // Clear the auth cookie
  response.cookies.set('auth_token', '', {
    expires: new Date(0),
    path: '/',
  });

  return response;
} 