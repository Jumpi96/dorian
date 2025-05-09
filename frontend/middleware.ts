import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('auth_token')
  const isAuthPage = request.nextUrl.pathname === '/login-success'

  // If trying to access auth page, allow it
  if (isAuthPage) {
    return NextResponse.next()
  }

  // If no token and trying to access protected route, redirect to home
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ['/dashboard/:path*', '/login-success'],
} 