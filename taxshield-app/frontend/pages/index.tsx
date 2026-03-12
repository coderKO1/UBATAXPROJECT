import { FormEvent, useState } from 'react';
import { useRouter } from 'next/router';
import { api } from '../services/api';

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState('demo@taxshield.com');
  const [password, setPassword] = useState('password123');
  const [error, setError] = useState('');

  const submit = async (e: FormEvent) => {
    e.preventDefault();
    try {
      const { data } = await api.post('/auth/login', { email, password });
      localStorage.setItem('token', data.access_token);
      router.push('/dashboard');
    } catch {
      setError('Invalid credentials');
    }
  };

  return (
    <div className="min-h-screen grid place-items-center p-4">
      <form onSubmit={submit} className="glass p-8 w-full max-w-md space-y-4">
        <h1 className="text-3xl font-bold text-red-300">TaxShield Login</h1>
        <input className="w-full p-3 rounded bg-black/30" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="w-full p-3 rounded bg-black/30" value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
        {error && <p className="text-red-400">{error}</p>}
        <button className="w-full bg-red-700 hover:bg-red-600 p-3 rounded">Login</button>
      </form>
    </div>
  );
}
