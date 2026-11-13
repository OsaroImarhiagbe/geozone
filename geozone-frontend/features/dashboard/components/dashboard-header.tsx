"use client";
import { useEffect, useState } from "react";
import { Separator } from "@/components/ui/separator";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { ChevronDown, Sun } from "lucide-react";
import Link from "next/link";
const nav = ["Zoning", "Insights"];

export default function DashboardHeader() {
  const [utc, setUtc] = useState("");

  useEffect(() => {
    const tick = () => setUtc(new Date().toLocaleString().slice(11, 19));
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header className="sticky top-0 z-30 flex h-[64px] shrink-0 items-center justify-between gap-2 border-b border-white/10 bg-[#070C14] px-4">
      <div className="flex items-center gap-6">
        <nav className="hidden items-center gap-1 font-mono text-sm md:flex">
          {nav.map((item, i) => (
            <Link
              href="/"
              key={item}
              className={`relative rounded-md px-3 py-1.5 transition-colors hover:cursor-pointer text-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400/60 ${
                i === 0 ? "text-cyan-300" : "text-slate-500"
              }`}
            >
              {item}
              {i === 0 && (
                <span className="absolute inset-x-3 -bottom-[13px] h-px bg-cyan-400" />
              )}
            </Link>
          ))}
        </nav>
      </div>

      <div className="flex items-center gap-4">
        <span className="hidden font-mono text-xs tabular-nums text-slate-400 lg:block">
          {utc && `${utc} UTC`}
        </span>

        <Button variant="ghost" size="icon" className="cursor-pointer">
          <Sun className="h-4 w-4 text-slate-300" />
        </Button>

        <Separator orientation="vertical" className="h-6 bg-white/10" />

        <button className="flex items-center gap-2 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400/60">
          <Avatar className="h-8 w-8 ring-1 ring-cyan-400/40">
            <AvatarFallback className="bg-[#0B1726] font-mono text-xs text-cyan-200">
              EI
            </AvatarFallback>
          </Avatar>
          <span className="hidden text-sm font-medium text-slate-100 md:block">
            Emmanuel I.
          </span>
          <ChevronDown className="h-4 w-4 text-slate-500" />
        </button>
      </div>
    </header>
  );
}
