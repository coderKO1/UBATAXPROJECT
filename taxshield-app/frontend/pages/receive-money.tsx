import { FormEvent, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function ReceivePage() {
  const [form, setForm] = useState({ amount: 0, sender: '', category: 'Customer Payment', description: 'Payment received' });
  const [msg, setMsg] = useState('');
  const submit = async (e: FormEvent) => { e.preventDefault(); await api.post('/banking/receive', form); setMsg('Funds received'); };
  return <AppLayout><h2 className='text-2xl mb-4'>Receive Money</h2><form onSubmit={submit} className='glass p-4 grid gap-3 max-w-xl'><input className='p-2 rounded bg-black/40' type='number' placeholder='Amount' onChange={(e)=>setForm({...form, amount: Number(e.target.value)})} /><input className='p-2 rounded bg-black/40' placeholder='Sender' onChange={(e)=>setForm({...form, sender: e.target.value})} /><button className='bg-red-700 p-2 rounded'>Confirm Receipt</button>{msg && <p>{msg}</p>}</form></AppLayout>;
}
