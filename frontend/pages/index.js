/**
 * Debt Empire v2.0 - Home Page
 * Redirects to dashboard if authenticated, otherwise to login
 */

import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      router.push('/dashboard');
    } else {
      router.push('/login');
    }
  }, []);

  return (
    <div style={{ padding: '20px', textAlign: 'center' }}>
      <Head>
        <title>Debt Empire</title>
      </Head>
      <p>Redirecting...</p>
    </div>
  );
}
