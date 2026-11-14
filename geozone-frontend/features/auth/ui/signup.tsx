"use client";
import Link from "next/link";
import { Layers, MapPinned, Orbit, Sparkles } from "lucide-react";
import { SignupForm } from "@/features/auth/components/signup-form";

const features = [
  {
    icon: MapPinned,
    title: "Live parcel layers",
    text: "Parcels load for exactly the area you're viewing.",
  },
  {
    icon: Layers,
    title: "Zoning at a glance",
    text: "Color-coded districts with height, FAR, and setback rules.",
  },
  {
    icon: Sparkles,
    title: "AI parcel analysis",
    text: "Select a parcel and get opportunities, constraints, and next steps.",
  },
];

const zoneChips = [
  { code: "C-3", color: "#e11d48" },
  { code: "CRMU/M", color: "#f472b6" },
  { code: "OCM(50)", color: "#c084fc" },
  { code: "R8", color: "#facc15" },
  { code: "W-1", color: "#60a5fa" },
  { code: "POS", color: "#4ade80" },
];

export default function SignupPage() {
  return (
    <div className="grid min-h-svh bg-[#060A11] lg:grid-cols-[minmax(0,1fr)_minmax(0,1.15fr)]">
      {/* Form side */}
      <div className="space-bg flex flex-col gap-4 p-6 md:p-10">
        <Link
          href="/"
          className="flex items-center justify-center gap-2.5 md:justify-start"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-md border border-cyan-400/40 bg-cyan-400/10">
            <Orbit className="h-4 w-4 text-cyan-300" />
          </div>
          <span className="font-mono text-xl font-bold tracking-tight text-slate-50">
            GeoZone
          </span>
        </Link>

        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-sm">
            <div className="mb-8">
              <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-cyan-300">
                Create account
              </p>
              <h1 className="font-mono text-3xl font-semibold tracking-tight text-slate-50">
                Create your account
              </h1>
              <p className="mt-2 font-mono text-sm text-slate-400">
                Start exploring zoning data in minutes.
              </p>
            </div>

            <SignupForm />
          </div>
        </div>

        <p className="text-center font-mono text-xs text-slate-600 md:text-left">
          © {new Date().getFullYear()} GeoZone · Alexandria, VA
        </p>
      </div>

      {/* Showcase side */}
      <div className="relative hidden overflow-hidden border-l border-white/10 bg-[#0A111C] lg:block">
        <svg
          aria-hidden
          viewBox="0 0 800 1000"
          preserveAspectRatio="xMidYMid slice"
          className="absolute inset-0 h-full w-full"
        >
          <g
            transform="rotate(-24 400 500)"
            fill="none"
            stroke="#94a3b8"
            strokeWidth="1"
          >
            <ellipse cx="400" cy="500" rx="130" ry="60" opacity="0.28" />
            <ellipse cx="400" cy="500" rx="220" ry="104" opacity="0.22" />
            <ellipse cx="400" cy="500" rx="320" ry="156" opacity="0.17" />
            <ellipse cx="400" cy="500" rx="430" ry="214" opacity="0.12" />
            <ellipse cx="400" cy="500" rx="550" ry="280" opacity="0.08" />
          </g>
          <g transform="rotate(-24 400 500)">
            <circle cx="720" cy="500" r="4" fill="#22d3ee" />
            <circle cx="180" cy="500" r="3" fill="#94a3b8" opacity="0.6" />
            <circle cx="400" cy="344" r="3" fill="#94a3b8" opacity="0.6" />
          </g>
        </svg>

        <div className="relative z-10 flex h-full flex-col justify-between p-12 xl:p-16">
          <div className="flex w-fit items-center gap-2 rounded-md border border-white/10 bg-[#070C14] px-3 py-1.5 font-mono text-xs text-slate-300">
            <span className="telemetry-dot h-1.5 w-1.5 rounded-full bg-emerald-400" />
            Parcel feed live
          </div>

          <div className="max-w-lg">
            <h2 className="font-mono text-4xl font-semibold leading-tight tracking-tight text-slate-50 xl:text-5xl">
              Start mapping
              <br />
              <span className="text-cyan-300">your next site.</span>
            </h2>
            <p className="mt-4 font-mono text-sm leading-6 text-slate-400">
              Save areas of interest, compare zoning across parcels, and get
              AI-assisted analysis in one workspace.
            </p>

            <ul className="mt-10 space-y-5">
              {features.map(({ icon: Icon, title, text }) => (
                <li key={title} className="flex gap-4">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-white/10 bg-white/5">
                    <Icon className="h-4 w-4 text-cyan-300" />
                  </div>
                  <div>
                    <p className="font-mono text-sm font-semibold text-slate-100">
                      {title}
                    </p>
                    <p className="mt-0.5 text-xs leading-5 text-slate-400">
                      {text}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div className="flex flex-wrap gap-2">
            {zoneChips.map((z) => (
              <span
                key={z.code}
                className="flex items-center gap-2 rounded-md border border-white/10 bg-[#070C14] px-2.5 py-1 font-mono text-xs text-slate-300"
              >
                <span
                  className="h-2.5 w-2.5 rounded-[3px] border border-white/25"
                  style={{ backgroundColor: z.color }}
                />
                {z.code}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
