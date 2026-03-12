import Link from 'next/link';
import { ReactNode } from 'react';

const links = [
  ['Dashboard', '/dashboard'],
  ['Transactions', '/transactions'],
  ['Transfer', '/transfer-money'],
  ['Receive', '/receive-money'],
  ['TaxShield', '/taxshield'],
  ['VAT Wallet', '/vat-wallet'],
  ['CIT Wallet', '/cit-wallet'],
  ['Payroll', '/payroll'],
  ['Analytics', '/analytics'],
  ['AI Assistant', '/ai-assistant'],
  ['Settings', '/settings'],
];

export default function AppLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen flex">
      <aside className="w-64 p-5 glass m-4 hidden md:block">
        <h1 className="text-2xl font-bold text-red-300 mb-4">TaxShield</h1>
        <nav className="space-y-2">
          {links.map(([label, href]) => (
            <Link key={href} href={href} className="block px-3 py-2 rounded-lg hover:bg-white/10">{label}</Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 p-4 md:p-8">{children}</main>
    </div>
  );
}
