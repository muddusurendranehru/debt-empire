/**
 * Debt Empire v2.0 - Dashboard (Protected)
 * Requires authentication
 * Redirects to login if not authenticated
 */

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';

const API_URL = 'http://localhost:8000';

export default function Dashboard() {
  const router = useRouter();
  const [masters, setMasters] = useState(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');
  const [user, setUser] = useState(null);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    // Get user info
    loadUserInfo();
    loadMasters();
  }, []);

  const loadUserInfo = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`${API_URL}/api/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setUser(data);
        setAuthenticated(true);
      } else {
        // Token invalid, redirect to login
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('email');
        router.push('/login');
      }
    } catch (error) {
      console.error('Error loading user info:', error);
      router.push('/login');
    }
  };

  const loadMasters = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      const response = await fetch(`${API_URL}/api/masters`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setMasters(data);
      } else if (response.status === 401) {
        // Unauthorized, redirect to login
        localStorage.removeItem('token');
        router.push('/login');
      } else {
        setMessage('Error loading loan data');
      }
    } catch (error) {
      console.error('Error loading masters:', error);
      setMessage('Error loading loan data');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_id');
    localStorage.removeItem('email');
    router.push('/login');
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
      return;
    }

    setUploading(true);
    setMessage('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const monthName = prompt('Enter month name (e.g., feb26):') || 
        new Date().toLocaleDateString('en-US', { month: 'short', year: '2-digit' }).toLowerCase();

      const response = await fetch(`${API_URL}/api/upload-csv?month_name=${monthName}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData,
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`Success! Parsed ${result.loans_parsed} loans. Files: ${result.files_generated.join(', ')}`);
        loadMasters(); // Reload masters
      } else {
        setMessage(`Error: ${result.detail || result.error || 'Upload failed'}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      setMessage(`Error: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const formatCurrency = (amount) => {
    if (!amount) return 'Rs 0';
    const lakhs = amount / 100000;
    return `Rs ${lakhs.toFixed(2)}L`;
  };

  if (!authenticated) {
    return (
      <div style={{ padding: '20px', textAlign: 'center' }}>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div style={{ fontFamily: 'system-ui, sans-serif', padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <Head>
        <title>Dashboard - Debt Empire v2.0</title>
      </Head>

      <header style={{ borderBottom: '2px solid #333', paddingBottom: '20px', marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1>Debt Empire v2.0</h1>
          <p>Monthly Ritual Dashboard</p>
          {user && <p style={{ fontSize: '14px', color: '#666' }}>Logged in as: {user.email}</p>}
        </div>
        <button
          onClick={handleLogout}
          style={{
            padding: '10px 20px',
            backgroundColor: '#c33',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: '500'
          }}
        >
          Logout
        </button>
      </header>

      {/* Upload Section */}
      <section style={{ marginBottom: '40px', padding: '20px', border: '2px dashed #ccc', borderRadius: '8px' }}>
        <h2>Upload LoanLens CSV</h2>
        <input
          type="file"
          accept=".csv"
          onChange={handleFileUpload}
          disabled={uploading}
          style={{ marginTop: '10px' }}
        />
        {uploading && <p>Processing...</p>}
        {message && (
          <p style={{ 
            marginTop: '10px', 
            padding: '10px', 
            backgroundColor: message.includes('Error') ? '#fee' : '#efe',
            borderRadius: '4px'
          }}>
            {message}
          </p>
        )}
      </section>

      {/* Masters Summary */}
      {loading ? (
        <p>Loading...</p>
      ) : masters ? (
        <section>
          <h2>Portfolio Overview</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '30px' }}>
            <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
              <h3>Total Loans</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>
                {Object.keys(masters.loans || {}).length}
              </p>
            </div>
            <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
              <h3>Total Outstanding</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>
                {formatCurrency(masters.total_exposure)}
              </p>
            </div>
            <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
              <h3>Total Monthly EMI</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>
                {formatCurrency(masters.total_emi)}
              </p>
            </div>
            <div style={{ padding: '15px', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
              <h3>Total Savings (70% OTS)</h3>
              <p style={{ fontSize: '24px', fontWeight: 'bold' }}>
                {formatCurrency(masters.total_savings)}
              </p>
            </div>
          </div>

          {/* Loans Table */}
          <h3>Loan Details</h3>
          <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
            <thead>
              <tr style={{ backgroundColor: '#333', color: 'white' }}>
                <th style={{ padding: '10px', textAlign: 'left' }}>Provider</th>
                <th style={{ padding: '10px', textAlign: 'left' }}>Account Ref</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>Outstanding</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>EMI</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>Tenure</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>OTS (70%)</th>
                <th style={{ padding: '10px', textAlign: 'right' }}>Savings</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(masters.loans || {}).map(([key, loan]) => (
                <tr key={key} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '10px' }}>{loan.provider}</td>
                  <td style={{ padding: '10px' }}>{loan.account_ref || '—'}</td>
                  <td style={{ padding: '10px', textAlign: 'right' }}>
                    {formatCurrency(loan.outstanding)}
                  </td>
                  <td style={{ padding: '10px', textAlign: 'right' }}>
                    Rs {(loan.emi / 1000).toFixed(0)}k
                  </td>
                  <td style={{ padding: '10px', textAlign: 'right' }}>
                    {loan.tenure_months} months
                  </td>
                  <td style={{ padding: '10px', textAlign: 'right' }}>
                    {formatCurrency(loan.ots_amount_70pct)}
                  </td>
                  <td style={{ padding: '10px', textAlign: 'right' }}>
                    {formatCurrency(loan.savings)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {masters.last_updated && (
            <p style={{ marginTop: '20px', color: '#666', fontSize: '14px' }}>
              Last updated: {masters.last_updated}
            </p>
          )}
        </section>
      ) : (
        <p>No data available. Upload a CSV to get started.</p>
      )}
    </div>
  );
}
