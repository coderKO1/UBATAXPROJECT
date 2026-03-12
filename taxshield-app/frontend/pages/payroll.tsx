import { FormEvent, useEffect, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function PayrollPage() {
  const [employees, setEmployees] = useState<any[]>([]);
  const [form, setForm] = useState({ name: '', salary: 0, pension: 0, nhis: 0 });
  const [message, setMessage] = useState('');
  const load = () => api.get('/payroll/employees').then((r) => setEmployees(r.data));
  useEffect(() => { load(); }, []);
  const submit = async (e: FormEvent) => { e.preventDefault(); await api.post('/payroll/employees', form); setForm({ name: '', salary: 0, pension: 0, nhis: 0 }); load(); };
  const validate = async () => { const { data } = await api.post('/payroll/validate-salary'); setMessage(`Validated ${data.records.length} salary payments`); load(); };
  return <AppLayout><h2 className='text-2xl mb-3'>Payroll Management</h2><div className='grid md:grid-cols-2 gap-4'><form onSubmit={submit} className='glass p-4 grid gap-2'><input className='p-2 rounded bg-black/40' placeholder='Name' value={form.name} onChange={(e)=>setForm({...form,name:e.target.value})}/><input className='p-2 rounded bg-black/40' type='number' placeholder='Salary' onChange={(e)=>setForm({...form,salary:Number(e.target.value)})}/><input className='p-2 rounded bg-black/40' type='number' placeholder='Pension' onChange={(e)=>setForm({...form,pension:Number(e.target.value)})}/><input className='p-2 rounded bg-black/40' type='number' placeholder='NHIS' onChange={(e)=>setForm({...form,nhis:Number(e.target.value)})}/><button className='bg-red-700 p-2 rounded'>Add Employee</button></form><div className='glass p-4'><button onClick={validate} className='bg-red-700 p-2 rounded mb-3'>Validate Salary</button>{message && <p>{message}</p>}<div className='space-y-2 mt-2'>{employees.map((e)=><div key={e.id}>{e.name} - ₦{e.salary.toLocaleString()}</div>)}</div></div></div></AppLayout>;
}
