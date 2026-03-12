import { useEffect, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function VATWalletPage() {
  const [wallet, setWallet] = useState(0);
  useEffect(() => { api.get('/banking/wallets').then((r) => setWallet(r.data.vat_wallet)); }, []);
  return <AppLayout><div className='glass p-8'><h2 className='text-3xl'>VAT Wallet</h2><p className='text-4xl mt-4'>₦{wallet.toLocaleString()}</p></div></AppLayout>;
}
