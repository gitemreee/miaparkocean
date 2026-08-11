import {
  Trees, Waves, Footprints, Sparkles, Lamp, Flower2, Car, ShieldCheck, Dumbbell,
  ShoppingBag, Building2, HeartPulse, Milestone, GraduationCap,
  PiggyBank, Vote, Landmark, ScrollText,
  BookMarked, MonitorSmartphone, UserCheck, Layers, FileSearch, KeyRound,
  Percent, Lock, TrendingDown, Handshake, Train,
  type LucideIcon,
} from "lucide-react";

const icons: Record<string, LucideIcon> = {
  Trees, Waves, Footprints, Sparkles, Lamp, Flower2, Car, ShieldCheck, Dumbbell,
  ShoppingBag, Building2, HeartPulse, Milestone, GraduationCap,
  PiggyBank, Vote, Landmark, ScrollText,
  BookMarked, MonitorSmartphone, UserCheck, Layers, FileSearch, KeyRound,
  Percent, Lock, TrendingDown, Handshake, Train,
};

export function Icon({ name, className }: { name: string; className?: string }) {
  const Cmp = icons[name] ?? Sparkles;
  return <Cmp className={className} strokeWidth={1.4} aria-hidden="true" />;
}
