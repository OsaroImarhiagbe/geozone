"use client";
import { Bookmark, Building2 } from "lucide-react";
import Map from "@/features/dashboard/components/map";
// import RecentAOI from "@/features/dashboard/components/recent-aoi";
import AOISummary from "@/features/dashboard/components/aoi-summary";
import QuickAction from "@/features/dashboard/components/quick-action";
import ParcelAIAnalysis from "../components/ai-analysis";

export default function DashboardScreen() {
  return (
    <section className="space-bg relative min-h-screen text-slate-200">
      <div className="relative mx-auto w-full max-w-[1700px] space-y-4 p-4 lg:p-6">
        {/* Header */}
        <div className="flex flex-wrap items-end justify-between gap-3">
          <div>
            <h1 className="font-mono text-2xl font-semibold tracking-tight text-slate-50">
              Welcome back, Emmanuel
            </h1>
            <p className="mt-1 font-mono text-sm text-slate-400">
              Explore zoning data, analyze properties, and make informed real
              estate decisions.
            </p>
          </div>

          <div className="flex items-center gap-2 rounded-md border border-cyan-400/20 bg-cyan-400/5 px-3 py-1.5 font-mono text-xs text-cyan-300">
            <span className="telemetry-dot h-1.5 w-1.5 rounded-full bg-emerald-400" />
            Parcel feed live
          </div>
        </div>

        {/* Quick Actions */}
        <section className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          <QuickAction
            icon={Building2}
            title="Get AI Summary"
            description="View zoning, land use, and development rules"
          />
          <QuickAction
            icon={Bookmark}
            title="Save & Organize"
            description="Save AOIs for later or add to a project"
          />
        </section>

        {/* Main workspace: map is the hero */}
        <section className="grid min-w-0 gap-4 xl:grid-cols-[minmax(0,1fr)_380px]">
          <Map />
          <div className="min-w-0 xl:h-[calc(100vh-260px)] xl:min-h-[680px]">
            {/* <AOISummary /> */}
            <ParcelAIAnalysis />
          </div>
        </section>

        {/* <RecentAOI /> */}
      </div>
    </section>
  );
}
