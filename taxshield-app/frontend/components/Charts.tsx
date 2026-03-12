import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, BarChart, Bar } from 'recharts';

export function IncomeExpenseChart({ data }: { data: any[] }) {
  return (
    <div className="glass p-4 h-64">
      <h3 className="mb-3">Income vs Expenses</h3>
      <ResponsiveContainer width="100%" height="90%">
        <AreaChart data={data}>
          <XAxis dataKey="name" /><YAxis /><Tooltip />
          <Area type="monotone" dataKey="income" stroke="#ef4444" fill="#ef444444" />
          <Area type="monotone" dataKey="expense" stroke="#ffffff" fill="#ffffff22" />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export function RevenueChart({ data }: { data: any[] }) {
  return (
    <div className="glass p-4 h-64">
      <h3 className="mb-3">Monthly Revenue</h3>
      <ResponsiveContainer width="100%" height="90%">
        <BarChart data={data}><XAxis dataKey="name" /><YAxis /><Tooltip /><Bar dataKey="revenue" fill="#9b111e" /></BarChart>
      </ResponsiveContainer>
    </div>
  );
}
