import { FormEvent, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

const narrations = ['Business Expense','Inventory Purchase','Salary Payment','Operational Expense','Customer Payment','Personal Transfer','Investment','Loan Repayment'];

export default function TransferPage() {
  const [form, setForm] = useState({ amount: 0, receiver: '', category: narrations[0], description: '' });
  const [msg, setMsg] = useState('');
  const submit = async (e: FormEvent) => { e.preventDefault(); await api.post('/banking/transfer', form); setMsg('Transfer successful'); };
  return <AppLayout><h2 className='text-2xl mb-4'>Transfer Money</h2><form onSubmit={submit} className='glass p-4 grid gap-3 max-w-xl'><input className='p-2 rounded bg-black/40' type='number' placeholder='Amount' onChange={(e)=>setForm({...form, amount: Number(e.target.value)})} /><input className='p-2 rounded bg-black/40' placeholder='Receiver' onChange={(e)=>setForm({...form, receiver: e.target.value})} /><select className='p-2 rounded bg-black/40' onChange={(e)=>setForm({...form, category: e.target.value})}>{narrations.map(n=><option key={n}>{n}</option>)}</select><input className='p-2 rounded bg-black/40' placeholder='Description' onChange={(e)=>setForm({...form, description: e.target.value})} /><button className='bg-red-700 p-2 rounded'>Send Transfer</button>{msg && <p>{msg}</p>}</form></AppLayout>;
}
