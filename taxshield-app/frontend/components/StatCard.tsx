import { motion } from 'framer-motion';

export default function StatCard({ label, value }: { label: string; value: string }) {
  return (
    <motion.div whileHover={{ scale: 1.03 }} className="glass p-4">
      <p className="text-gray-300 text-sm">{label}</p>
      <p className="text-2xl font-semibold mt-1">{value}</p>
    </motion.div>
  );
}
