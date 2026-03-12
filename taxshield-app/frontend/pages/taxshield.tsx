import { useEffect, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function TaxShieldPage() {
  const [data, setData] = useState<any>({});
  useEffect(() => { api.get('/banking/wallets').then((r) => setData(r.data)); }, []);
  return <AppLayout><h2 className='text-2xl mb-3'>Tax Transparency</h2><div className='glass p-4 space-y-2'><p>Estimated Tax: ₦{data.estimated || 0}</p><p>Profit Formula: {data.formulas?.profit}</p><p>CIT Formula: {data.formulas?.cit}</p><p>VAT Formula: {data.formulas?.vat}</p></div></AppLayout>;
}
