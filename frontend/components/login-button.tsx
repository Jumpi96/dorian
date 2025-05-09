'use client';

import { useAuth } from '@/lib/auth';
import { Button } from '@/components/ui/button';

export function LoginButton() {
  const { login, logout, isAuthenticated } = useAuth();

  return (
    <Button
      onClick={isAuthenticated ? logout : login}
      variant="outline"
    >
      {isAuthenticated ? 'Logout' : 'Login with Google'}
    </Button>
  );
} 