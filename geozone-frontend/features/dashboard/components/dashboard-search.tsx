"use client";
import { Search, Target } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function DashboardSearch() {
  return (
    <div className="flex gap-3">
      <div className="relative flex-1">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-cyan-400/70" />

        <Input
          placeholder="Search by address, city, county, or coordinates..."
          className="h-11 border-white/10 bg-[#0A111C] pl-10 pr-14 font-mono text-slate-100 placeholder:text-slate-500 focus-visible:border-cyan-400/60 focus-visible:ring-cyan-400/20"
        />

        <kbd className="pointer-events-none absolute right-3 top-1/2 hidden -translate-y-1/2 rounded border border-white/10 bg-white/5 px-1.5 py-0.5 font-mono text-[10px] text-slate-400 sm:block">
          ⌘K
        </kbd>
      </div>

      <Button
        variant="outline"
        size="icon"
        aria-label="Locate on map"
        className="h-11 w-11 border-white/10 bg-[#0A111C] text-cyan-300 hover:border-cyan-400/50 hover:bg-cyan-400/10 hover:text-cyan-200"
      >
        <Target className="h-4 w-4" />
      </Button>
    </div>
  );
}
