import { useEffect } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';
import { useAppStore } from '../store/useAppStore';
import StatCard from '../components/StatCard';
import { IncomeExpenseChart, RevenueChart } from '../components/Charts';

export default function DashboardPage() {
  const { dashboard, setDashboard } = useAppStore();

  useEffect(() => {
    api.get('/banking/dashboard').then((r) => setDashboard(r.data));
  }, [setDashboard]);

  const chartData = [{ name: 'Now', income: dashboard?.monthly_income || 0, expense: dashboard?.monthly_expenses || 0 }];
  const revData = [{ name: 'Estimate', revenue: dashboard?.monthly_income || 0 }];

  return (
    <AppLayout>
      <h2 className="text-3xl font-bold mb-4">Futuristic UBA SME Dashboard</h2>
      <div className="grid md:grid-cols-4 gap-3 mb-4">
        <StatCard label="Account Balance" value={`₦${dashboard?.account_balance?.toLocaleString?.() || 0}`} />
        <StatCard label="Profit" value={`₦${dashboard?.profit?.toLocaleString?.() || 0}`} />
        <StatCard label="Estimated Annual Tax" value={`₦${dashboard?.estimated_annual_tax?.toLocaleString?.() || 0}`} />
        <StatCard label="VAT/CIT Wallet" value={`₦${dashboard?.vat_wallet || 0} / ₦${dashboard?.cit_wallet || 0}`} />
      </div>
      <div className="grid md:grid-cols-2 gap-4 mb-4"><IncomeExpenseChart data={chartData} /><RevenueChart data={revData} /></div>
      <div className="glass p-4">
        <h3 className="mb-2">Recent Transactions</h3>
        <div className="space-y-2">
          {dashboard?.recent_transactions?.map((tx: any) => (
            <div key={tx.id} className="flex justify-between border-b border-white/10 pb-2 text-sm">
              <span>{tx.category} - {tx.description}</span><span>₦{tx.amount.toLocaleString()}</span>
            </div>
          ))}
        </div>
      </div>
    </AppLayout>
  );
}
