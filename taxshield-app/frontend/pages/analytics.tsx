import { useEffect, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';
import { RevenueChart } from '../components/Charts';

export default function AnalyticsPage() {
  const [a, setA] = useState<any>(null);
  useEffect(() => { api.get('/analytics').then((r) => setA(r.data)); }, []);
  const rev = (a?.monthly_income || []).map((r:any) => ({ name: `M${r.month}`, revenue: r.amount }));
  return <AppLayout><h2 className='text-2xl mb-4'>Financial Analytics</h2><div className='grid md:grid-cols-3 gap-3 mb-4'><div className='glass p-4'>Profit: ₦{a?.profit || 0}</div><div className='glass p-4'>Estimated Tax: ₦{a?.estimated_tax || 0}</div><div className='glass p-4'>Payroll Cost: ₦{a?.payroll_costs || 0}</div></div><RevenueChart data={rev} /></AppLayout>;
}
