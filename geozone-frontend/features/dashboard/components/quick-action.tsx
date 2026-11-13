"use client";
import { Card, CardContent } from "@/components/ui/card";
import type { LucideIcon } from "lucide-react";
export default function QuickAction({
  icon: Icon,
  title,
  description,
  active = false,
}: {
  icon?: LucideIcon;
  title: string;
  description: string;
  active?: boolean;
}) {
  return (
    <Card
      className={`group cursor-pointer gap-0 rounded-lg border max-w-xl py-0 text-slate-200 ring-0 transition-colors ${
        active
          ? "border-cyan-400/50 bg-cyan-400/[0.07]"
          : "border-white/10 bg-[#0A111C] hover:border-cyan-400/30 hover:bg-[#0D1726]"
      }`}
    >
      <CardContent className="flex min-h-[88px] items-center gap-3 p-4">
        <div
          className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-md border ${
            active
              ? "border-cyan-400/40 bg-cyan-400/10 text-cyan-300"
              : "border-white/10 bg-white/5 text-slate-400 group-hover:text-cyan-300"
          }`}
        >
          {Icon && <Icon className="h-5 w-5" />}
        </div>

        <div>
          <p className="font-mono text-sm font-bold leading-tight text-slate-50">
            {title}
          </p>
          <p className="mt-1 font-mono text-xs leading-4 text-slate-400">
            {description}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
