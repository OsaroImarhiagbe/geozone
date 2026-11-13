"use client";
import { ArrowRight, Map as MapIcon, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const recentAOIs = [
  { name: "Downtown Development Site", acreage: "12.4 acres", zoning: "C-3" },
  { name: "Riverside Property", acreage: "8.7 acres", zoning: "R-5" },
  { name: "West End Parcel", acreage: "4.2 acres", zoning: "I-1" },
  { name: "Market St. Corridor", acreage: "15.6 acres", zoning: "C-2" },
];

const zoningTone: Record<string, string> = {
  "C-3": "border-red-400/40 bg-red-400/10 text-red-300",
  "C-2": "border-orange-400/40 bg-orange-400/10 text-orange-300",
  "R-5": "border-yellow-400/40 bg-yellow-400/10 text-yellow-300",
  "I-1": "border-purple-400/40 bg-purple-400/10 text-purple-300",
};

export default function RecentAOI() {
  return (
    <section>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="font-mono text-lg font-semibold text-slate-50">
          Recent AOIs
        </h2>

        <Button
          variant="ghost"
          size="sm"
          className="gap-1 font-mono text-cyan-300 hover:bg-cyan-400/10 hover:text-cyan-200"
        >
          View all
          <ArrowRight className="h-3.5 w-3.5" />
        </Button>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {recentAOIs.map((aoi) => (
          <Card
            key={aoi.name}
            className="cursor-pointer gap-0 rounded-lg border border-white/10 bg-[#0A111C] py-0 ring-0 transition-colors hover:border-cyan-400/40 hover:bg-[#0D1726]"
          >
            <CardContent className="flex gap-3 p-3">
              <div className="flex h-16 w-16 shrink-0 items-center justify-center rounded-md border border-white/10 bg-[#070C14]">
                <MapIcon className="h-6 w-6 text-cyan-400/60" />
              </div>

              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-2">
                  <p className="truncate text-sm font-medium text-slate-100">
                    {aoi.name}
                  </p>
                  <MoreHorizontal className="h-4 w-4 shrink-0 text-slate-500" />
                </div>

                <div className="mt-1.5 flex items-center gap-2">
                  <span
                    className={`rounded border px-1.5 py-0.5 font-mono text-[11px] ${zoningTone[aoi.zoning] ?? "border-white/10 text-slate-300"}`}
                  >
                    {aoi.zoning}
                  </span>
                  <span className="font-mono text-xs text-slate-400">
                    {aoi.acreage}
                  </span>
                </div>

                <p className="mt-2 text-[11px] text-slate-500">
                  Recently viewed
                </p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  );
}
