import { NextRequest, NextResponse } from 'next/server';

type SessisonIdType = string;
type AccessTokenType = string;
const LoginPath = '/login';

async function refershToken(sessionId: SessisonIdType): Promise<undefined | AccessTokenType> {
  const token = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/token/refresh`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
    }),
  }).then((res) => (res.ok ? res : undefined));

  if (token !== undefined) {
    const tokenData = await token.json();
    return tokenData.access_token;
  }
  return undefined;
}

async function checkAuth(accessToken: AccessTokenType): Promise<boolean> {
  const isSucceeded = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/users/me`, {
    method: 'GET',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
      Authorization: `Bearer ${accessToken}`,
    },
  }).then(async (res) => res.ok);

  return isSucceeded;
}

function redirectToLoginPage(request: NextRequest): NextResponse {
  return NextResponse.redirect(new URL(LoginPath, request.url));
}

function redirectToHomePage(request: NextRequest): NextResponse {
  return NextResponse.redirect(new URL('/', request.url));
}

async function middleware(request: NextRequest) {
  const response = await NextResponse.next();
  const sessionId: SessisonIdType | undefined = request.cookies.get('session_id')?.value;
  let accessToken: AccessTokenType | undefined = request.cookies.get('access_token')?.value;

  console.log(request.nextUrl.pathname);
  if (request.nextUrl.pathname === LoginPath && accessToken !== undefined) {
    if (await checkAuth(accessToken)) {
      return redirectToHomePage(request);
    }

    if (sessionId !== undefined) {
      accessToken = await refershToken(sessionId);
      console.log(accessToken);
      if (accessToken !== undefined && (await checkAuth(accessToken))) {
        return redirectToHomePage(request);
      }
    }
  }
  // If accessToken is not validated or null.
  if (accessToken === undefined || (accessToken !== undefined && !(await checkAuth(accessToken)))) {
    if (sessionId !== undefined) {
      accessToken = await refershToken(sessionId);

      // Check the accessToken was refreshed
      if (
        accessToken === undefined ||
        (accessToken !== undefined && !(await checkAuth(accessToken)))
      ) {
        return redirectToLoginPage(request);
      }
      response.cookies.set({
        name: 'access_token',
        value: accessToken,
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        domain: request.nextUrl.domainLocale?.domain,
      });
    }

    if (request.nextUrl.pathname !== LoginPath) {
      return redirectToLoginPage(request);
    }

    return response;
  }

  return response;
}

export const config = {
  matcher: ['/', '/login'],
};

export default middleware;
