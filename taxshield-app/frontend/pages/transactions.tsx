import { useEffect, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function TransactionsPage() {
  const [rows, setRows] = useState<any[]>([]);
  const [q, setQ] = useState('');
  useEffect(() => { api.get('/banking/transactions').then((r) => setRows(r.data)); }, []);
  const filtered = rows.filter((r) => r.category.toLowerCase().includes(q.toLowerCase()) || r.description.toLowerCase().includes(q.toLowerCase()));
  return <AppLayout><h2 className='text-2xl mb-4'>Transactions</h2><input className='p-2 mb-3 rounded bg-black/40 w-full' placeholder='Search/category filter' value={q} onChange={(e)=>setQ(e.target.value)} /><div className='glass p-4 space-y-2'>{filtered.map((r)=> <div key={r.id} className='flex justify-between text-sm'><span>{r.date.slice(0,10)} • {r.category} • {r.sender}→{r.receiver}</span><span>₦{r.amount.toLocaleString()}</span></div>)}</div></AppLayout>;
}
