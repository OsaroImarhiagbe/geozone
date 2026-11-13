"use client";
import { ArrowRight, Lightbulb, MapPin, Pencil, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useMemo } from "react";

import { useSelectedParcels } from "@/features/dashboard/store/useDashboardStore";

const tabs = ["Zoning", "Land Use", "Property Details"];

export default function AOISummary() {
  const parcels = useSelectedParcels((state) => state.parcels);

  const selectedParcel = useMemo(() => {
    const first = parcels[0];

    if (!first) return null;

    return {
      pid: first.pid,
      address: first.address,
      zone_code: first.zone_code,
      land_desc: first.land_desc,
      land_sf: first.land_sf,
    };
  }, [parcels]);
  return (
    <Card className="h-full gap-0 overflow-hidden rounded-lg border border-cyan-400/20 bg-[#0A111C] py-0 text-slate-200 ring-0">
      <CardHeader className="shrink-0 border-b border-white/10 p-4">
        <div className="flex items-center justify-between">
          <CardTitle className="font-mono text-lg font-semibold text-slate-50">
            Parcel Summary
          </CardTitle>

          <Button
            variant="link"
            size="sm"
            className="font-mono text-sm font-bold text-[#FC3D21] hover:cursor-pointer"
          >
            Save
          </Button>
        </div>

        <div className="mt-3 flex gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-md border border-cyan-400/30 bg-cyan-400/10">
            <MapPin className="h-4 w-4 text-cyan-300" />
          </div>

          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <p className="font-mono text-sm font-medium text-slate-50">
                {selectedParcel?.land_desc ?? "-"}
              </p>
              <Pencil className="h-3.5 w-3.5 text-slate-500" />
            </div>

            <p className="mt-1 font-mono text-xs text-slate-400">
              12.4 acres&nbsp;&nbsp;•&nbsp;&nbsp;Polygon
            </p>
            {/* <p className="mt-1 font-mono text-xs tabular-nums text-slate-500">
              {min_lng}° N, {max_lat}° W
            </p> */}
          </div>
        </div>
      </CardHeader>

      <CardContent className="min-h-0 flex-1 overflow-auto p-4 [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden hover:cursor-pointer">
        {/* Tabs */}
        <div className="mb-5 flex gap-2 border-b border-white/10 text-xs">
          {tabs.map((tab, i) => (
            <Button
              key={tab}
              variant="ghost"
              className={`font-mono transition-colors hover:cursor-pointer ${
                i === 0
                  ? "font-medium text-cyan-300"
                  : "text-slate-500 hover:text-slate-200"
              }`}
            >
              {tab}
            </Button>
          ))}
        </div>

        {/* Current Zoning */}
        <div className="rounded-lg border border-emerald-400/20 bg-emerald-400/[0.05] p-4">
          <div className="flex gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-md border border-emerald-400/30 bg-emerald-400/10">
              <Sparkles className="h-5 w-5 text-emerald-300" />
            </div>

            <div>
              <p className="font-mono text-xs font-medium text-emerald-300">
                Current Zone
              </p>
              <p className="mt-0.5 font-mono text-2xl font-semibold text-slate-50">
                {selectedParcel?.zone_code ?? "-"}
              </p>
              <p className="font-mono text-sm text-slate-300">
                {selectedParcel?.land_desc}
              </p>
            </div>
          </div>

          <p className="mt-3 font-mono text-xs leading-5 text-slate-400">
            {selectedParcel?.land_desc}
          </p>

          <Button
            variant="link"
            size="sm"
            className="mt-2 h-auto p-0 font-mono text-cyan-300 hover:text-cyan-200"
          >
            View zoning details
            <ArrowRight className="ml-1 h-3 w-3" />
          </Button>
        </div>

        {/* Key Information */}
        <div className="mt-6">
          <h3 className="mb-1 font-mono text-sm font-semibold text-slate-100">
            Key Zoning Information
          </h3>

          <div className="divide-y divide-white/10">
            <div className="flex items-center justify-between py-3 text-xs">
              <span className="text-slate-400">Parcel ID</span>
              <span className="font-mono font-medium tabular-nums text-cyan-100">
                {selectedParcel?.pid ?? "—"}
              </span>
            </div>
            <div className="flex items-center justify-between py-3 text-xs">
              <span className="text-slate-400">Zoning District</span>
              <span className="font-mono font-medium tabular-nums text-cyan-100">
                {selectedParcel?.zone_code ?? "-"}
              </span>
            </div>
            <div className="flex items-center justify-between py-3 text-xs">
              <span className="text-slate-400">Address</span>
              <span className="font-mono font-medium tabular-nums text-cyan-100">
                {selectedParcel?.address ?? "-"}
              </span>
            </div>
            <div className="flex items-center justify-between py-3 text-xs">
              <span className="text-slate-400">Land SF</span>
              <span className="font-mono font-medium tabular-nums text-cyan-100">
                {selectedParcel?.land_sf ?? "-"}
              </span>
            </div>
          </div>
        </div>

        {/* Nearby Zoning
        <div className="mt-5">
          <h3 className="mb-3 font-mono text-sm font-semibold text-slate-100">
            Nearby Zoning
          </h3>

          <div className="space-y-3">
            <NearbyZoning
              color="bg-red-400"
              name="C-3 (General Commercial)"
              distance="0.2 mi"
            />
            <NearbyZoning
              color="bg-yellow-400"
              name="R-5 (Residential)"
              distance="0.4 mi"
            />
            <NearbyZoning
              color="bg-purple-400"
              name="I-1 (Light Industrial)"
              distance="0.6 mi"
            />
          </div>
        </div> */}

        {/* Tip */}
        <div className="mt-6 flex gap-3 rounded-lg border border-cyan-400/20 bg-cyan-400/[0.06] p-3">
          <Lightbulb className="mt-0.5 h-4 w-4 shrink-0 text-cyan-300" />
          <p className="text-xs leading-5 text-cyan-100/80">
            You can save this AOI to your projects or adjust the boundary for a
            more detailed analysis.
          </p>
        </div>
      </CardContent>
    </Card>
  );
}

// function NearbyZoning({
//   color,
//   name,
//   distance,
// }: {
//   color: string;
//   name: string;
//   distance: string;
// }) {
//   return (
//     <div className="flex items-center justify-between text-xs">
//       <div className="flex items-center gap-2">
//         <span className={`h-3.5 w-3.5 rounded-sm ${color}`} />
//         <span className="text-slate-300">{name}</span>
//       </div>
//       <span className="font-mono tabular-nums text-slate-500">{distance}</span>
//     </div>
//   );
// }
