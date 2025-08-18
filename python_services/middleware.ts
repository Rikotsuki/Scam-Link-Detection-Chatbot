import { NextRequest, NextResponse } from 'next/server'
import { jwtVerify } from 'jose'

// Configuration
const JWT_SECRET = new TextEncoder().encode(
  process.env.JWT_SECRET || 'fallback-secret-key-change-in-production'
)

// Protected routes patterns
const PROTECTED_ROUTES = [
  '/dashboard',
  '/dashboard/:path*',
  '/anime',
  '/anime/:path*',
  '/admin',
  '/admin/:path*',
  '/api/protected/:path*'
]

// Admin-only routes
const ADMIN_ROUTES = [
  '/admin',
  '/admin/:path*',
  '/api/admin/:path*'
]

// Auth routes (redirect if already logged in)
const AUTH_ROUTES = [
  '/login',
  '/register',
  '/forgot-password'
]

/**
 * Check if a path matches any of the given patterns
 */
function matchesRoutes(pathname: string, routes: string[]): boolean {
  return routes.some(route => {
    if (route.endsWith('*')) {
      const basePath = route.slice(0, -1)
      return pathname.startsWith(basePath)
    }
    return pathname === route
  })
}

/**
 * Verify session token (simplified for middleware)
 */
async function verifySessionToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, JWT_SECRET)
    return {
      userId: payload.userId as string,
      role: payload.role as string,
      exp: payload.exp as number,
    }
  } catch {
    return null
  }
}

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl
  const sessionToken = request.cookies.get('session-token')?.value

  // Skip middleware for static files and API routes that don't need auth
  if (
    pathname.startsWith('/_next/') ||
    pathname.startsWith('/static/') ||
    pathname.includes('.') ||
    pathname === '/api/auth/login' ||
    pathname === '/api/auth/register'
  ) {
    return NextResponse.next()
  }

  let session = null
  if (sessionToken) {
    session = await verifySessionToken(sessionToken)
    
    // Clear invalid/expired tokens
    if (!session || session.exp < Math.floor(Date.now() / 1000)) {
      const response = NextResponse.next()
      response.cookies.delete('session-token')
      session = null
    }
  }

  // Handle auth routes (login, register, etc.)
  if (matchesRoutes(pathname, AUTH_ROUTES)) {
    if (session) {
      // Already logged in, redirect to dashboard
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
    return NextResponse.next()
  }

  // Handle protected routes
  if (matchesRoutes(pathname, PROTECTED_ROUTES)) {
    if (!session) {
      // Not logged in, redirect to login with return URL
      const loginUrl = new URL('/login', request.url)
      loginUrl.searchParams.set('from', pathname)
      return NextResponse.redirect(loginUrl)
    }

    // Check admin routes
    if (matchesRoutes(pathname, ADMIN_ROUTES) && session.role !== 'admin') {
      return NextResponse.redirect(new URL('/unauthorized', request.url))
    }
  }

  // Handle API routes
  if (pathname.startsWith('/api/protected/') || pathname.startsWith('/api/admin/')) {
    if (!session) {
      return NextResponse.json(
        { error: 'Authentication required' },
        { status: 401 }
      )
    }

    if (pathname.startsWith('/api/admin/') && session.role !== 'admin') {
      return NextResponse.json(
        { error: 'Admin access required' },
        { status: 403 }
      )
    }
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api/auth (authentication routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!api/auth|_next/static|_next/image|favicon.ico).*)',
  ],
} 