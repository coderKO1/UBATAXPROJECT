import AppLayout from '../layouts/AppLayout';

export default function SettingsPage() {
  return <AppLayout><h2 className='text-2xl mb-3'>Settings & Notifications</h2><div className='glass p-4 space-y-2'><button className='bg-red-700 p-2 rounded w-full'>Enable Email Alerts</button><button className='bg-red-700 p-2 rounded w-full'>Enable Salary Reminders</button><button className='bg-red-700 p-2 rounded w-full'>Enable Tax Threshold Alerts</button><button className='bg-red-700 p-2 rounded w-full'>Generate Monthly Report</button></div></AppLayout>;
}
