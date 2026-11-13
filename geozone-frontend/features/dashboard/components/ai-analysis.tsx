"use client";
import { useState } from "react";
import {
  AlertCircle,
  CheckCircle2,
  ListChecks,
  ShieldAlert,
  Sparkles,
  X,
} from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Skeleton } from "@/components/ui/skeleton";
import { useSelectedParcels } from "@/features/dashboard/store/useDashboardStore";
import { useParcelAnalysis } from "@/features/dashboard/hooks/useDashboard";

function Section({
  title,
  icon: Icon,
  items,
  iconClass,
}: {
  title: string;
  icon: React.ElementType;
  items: string[];
  iconClass: string;
}) {
  if (!items.length) return null;
  return (
    <div>
      <h3 className="mb-2 flex items-center gap-2 font-mono text-sm font-semibold text-slate-100">
        <Icon className={`h-4 w-4 ${iconClass}`} />
        {title}
      </h3>
      <ul className="space-y-1.5 pl-6">
        {items.map((item, i) => (
          <li
            key={i}
            className="list-disc text-xs leading-5 text-slate-300 marker:text-slate-600"
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function ParcelAIAnalysis() {
  const parcels = useSelectedParcels((s) => s.parcels);
  const remove = useSelectedParcels((s) => s.remove);
  const clear = useSelectedParcels((s) => s.clear);

  const { mutate, data, isPending, error, reset } = useParcelAnalysis();
  const [analyzedKey, setAnalyzedKey] = useState<string | null>(null);

  const key = parcels
    .map((p) => p.pid)
    .sort()
    .join(",");
  const stale = !!data && analyzedKey !== key;

  const run = () => mutate(parcels, { onSuccess: () => setAnalyzedKey(key) });

  const handleClear = () => {
    clear();
    reset();
    setAnalyzedKey(null);
  };

  return (
    <Card className="gap-0 rounded-lg border border-white/10 bg-[#0A111C] py-0 text-slate-200 ring-0">
      <CardHeader className="border-b border-white/10 p-4">
        <div className="flex items-start justify-between gap-3">
          <div>
            <CardTitle className="flex items-center gap-2 font-mono text-lg font-semibold text-slate-50">
              <Sparkles className="h-4 w-4 text-cyan-300" />
              AI Analysis
            </CardTitle>
            <CardDescription className="mt-1 font-mono text-xs text-slate-400">
              Click parcels on the map to select them, then run the analysis.
            </CardDescription>
          </div>

          <div className="flex items-center gap-2">
            <Badge
              variant="outline"
              className="border-white/15 font-mono text-[11px] text-slate-300"
            >
              {parcels.length} selected
            </Badge>
            {parcels.length > 0 && (
              <Button
                variant="link"
                size="sm"
                onClick={handleClear}
                className="h-auto p-0 font-mono text-xs font-bold text-[#FC3D21]"
              >
                Clear
              </Button>
            )}
          </div>
        </div>

        {parcels.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-2">
            {parcels.map((p) => (
              <Badge
                key={p.pid}
                variant="outline"
                className="gap-1.5 border-white/15 py-1 pl-2 pr-1 font-mono text-[11px] font-normal text-slate-200"
              >
                <span className="max-w-[180px] truncate">
                  {p.address || p.pid}
                </span>
                {p.zone_code && (
                  <span className="text-cyan-300">{p.zone_code}</span>
                )}
                <button
                  onClick={() => remove(p.pid)}
                  aria-label={`Remove ${p.address || p.pid}`}
                  className="rounded p-0.5 text-slate-500 hover:bg-white/10 hover:text-slate-100"
                >
                  <X className="h-3 w-3" />
                </button>
              </Badge>
            ))}
          </div>
        )}
      </CardHeader>

      <CardContent className="space-y-5 p-4">
        {/* Empty */}
        {!parcels.length && !isPending && !data && (
          <p className="py-6 text-center font-mono text-xs text-slate-500">
            No parcels selected yet.
          </p>
        )}

        {/* Ready to run */}
        {!!parcels.length && !isPending && !data && !error && (
          <p className="font-mono text-xs text-slate-400">
            {parcels.length} parcel{parcels.length > 1 ? "s" : ""} ready for
            analysis.
          </p>
        )}

        {/* Loading */}
        {isPending && (
          <div className="space-y-3" aria-busy="true">
            <Skeleton className="h-4 w-1/3 bg-white/10" />
            <Skeleton className="h-3 w-full bg-white/10" />
            <Skeleton className="h-3 w-11/12 bg-white/10" />
            <Skeleton className="h-3 w-4/5 bg-white/10" />
            <Skeleton className="mt-4 h-4 w-1/4 bg-white/10" />
            <Skeleton className="h-3 w-full bg-white/10" />
            <Skeleton className="h-3 w-3/4 bg-white/10" />
          </div>
        )}

        {/* Error */}
        {error && !isPending && (
          <Alert
            variant="destructive"
            className="border-red-500/30 bg-red-500/5"
          >
            <AlertCircle className="h-4 w-4" />
            <AlertTitle className="font-mono text-sm">
              Analysis failed
            </AlertTitle>
            <AlertDescription className="text-xs">
              {error.message}
            </AlertDescription>
          </Alert>
        )}

        {/* Result */}
        {data && !isPending && (
          <>
            {stale && (
              <Alert className="border-amber-400/30 bg-amber-400/5 text-amber-200">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription className="text-xs">
                  Your selection changed since this analysis. Re-run to update
                  it.
                </AlertDescription>
              </Alert>
            )}

            <div>
              <h3 className="mb-2 font-mono text-sm font-semibold text-slate-100">
                Summary
              </h3>
              <p className="text-xs leading-5 text-slate-300">{data.summary}</p>
            </div>

            <Separator className="bg-white/10" />
            <Section
              title="Opportunities"
              icon={CheckCircle2}
              iconClass="text-emerald-400"
              items={data.opportunities}
            />
            <Separator className="bg-white/10" />
            <Section
              title="Constraints"
              icon={ShieldAlert}
              iconClass="text-amber-400"
              items={data.constraints}
            />
            <Separator className="bg-white/10" />
            <Section
              title="Next steps"
              icon={ListChecks}
              iconClass="text-cyan-300"
              items={data.nextSteps}
            />
          </>
        )}
      </CardContent>

      <CardFooter className="flex-col items-stretch gap-3 border-t border-white/10 p-4">
        <Button
          onClick={run}
          disabled={!parcels.length || isPending}
          className="w-full gap-2 bg-cyan-400 font-mono font-semibold text-[#05080F] hover:bg-cyan-300"
        >
          <Sparkles className="h-4 w-4" />
          {isPending
            ? "Analyzing…"
            : data
              ? "Re-run analysis"
              : "Analyze selection"}
        </Button>
        <p className="font-mono text-[11px] leading-4 text-slate-500">
          AI-generated from parcel attributes. Verify against the City of
          Alexandria zoning ordinance before making decisions.
        </p>
      </CardFooter>
    </Card>
  );
}
