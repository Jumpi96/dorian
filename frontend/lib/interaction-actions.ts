'use server';

import { cookies } from 'next/headers';
import { revalidatePath } from 'next/cache';
import { Interaction } from './types';

export async function getInteractions(): Promise<Interaction[]> {
  const cookieStore = await cookies();
  const token = cookieStore.get('auth_token')?.value;

  if (!token) {
    throw new Error('Not authenticated');
  }

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/interactions`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  if (!response.ok) {
    throw new Error('Failed to fetch interactions');
  }

  return response.json();
} 