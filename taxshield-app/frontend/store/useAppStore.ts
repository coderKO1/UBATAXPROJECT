import { create } from 'zustand';

type Tx = { id: number; amount: number; type: string; date: string; sender: string; receiver: string; category: string; description: string };

type State = {
  token: string;
  dashboard: any;
  transactions: Tx[];
  setToken: (token: string) => void;
  setDashboard: (dashboard: any) => void;
  setTransactions: (transactions: Tx[]) => void;
};

export const useAppStore = create<State>((set) => ({
  token: '',
  dashboard: null,
  transactions: [],
  setToken: (token) => set({ token }),
  setDashboard: (dashboard) => set({ dashboard }),
  setTransactions: (transactions) => set({ transactions }),
}));
