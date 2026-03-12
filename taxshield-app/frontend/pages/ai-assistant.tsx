import { FormEvent, useState } from 'react';
import AppLayout from '../layouts/AppLayout';
import { api } from '../services/api';

export default function AIAssistantPage() {
  const [question, setQuestion] = useState('How much have we spent this month?');
  const [answer, setAnswer] = useState('Ask TaxShield AI about VAT, CIT, PAYE, and transactions.');
  const ask = async (e: FormEvent) => { e.preventDefault(); const { data } = await api.post('/assistant/query', { question }); setAnswer(data.answer); };
  return <AppLayout><h2 className='text-2xl mb-3'>TaxShield AI Assistant</h2><form onSubmit={ask} className='glass p-4 grid gap-3 max-w-2xl'><input className='p-2 rounded bg-black/40' value={question} onChange={(e)=>setQuestion(e.target.value)} /><button className='bg-red-700 p-2 rounded'>Ask AI</button><p className='text-green-200'>{answer}</p></form></AppLayout>;
}
