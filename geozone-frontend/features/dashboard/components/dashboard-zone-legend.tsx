"use client";
import { useState } from "react";
import { ChevronDown, ChevronRight, ChevronUp, Layers } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ZONE_FALLBACK, ZONE_FAMILIES } from "@/lib/zone-colors";

function Swatch({ color, small = false }: { color: string; small?: boolean }) {
  return (
    <span
      aria-hidden
      className={`shrink-0 rounded-[3px] border border-white/25 ${
        small ? "h-2.5 w-2.5" : "mt-0.5 h-3.5 w-3.5"
      }`}
      style={{ backgroundColor: color }}
    />
  );
}

function Row({
  color,
  code,
  description,
}: {
  color: string;
  code: string;
  description: string;
}) {
  return (
    <div className="flex items-start gap-2.5 py-1">
      <Swatch color={color} />
      <div className="min-w-0">
        <p className="font-mono text-xs font-semibold leading-tight text-slate-100">
          {code}
        </p>
        <p className="mt-0.5 text-[11px] leading-4 text-slate-500">
          {description}
        </p>
      </div>
    </div>
  );
}

export default function ZoneLegend() {
  const [open, setOpen] = useState(true);
  const [expanded, setExpanded] = useState<Set<string>>(new Set());

  const toggleFamily = (id: string) =>
    setExpanded((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <Card
      className="w-72 gap-0 rounded-md border border-white/10 bg-[#070C14] py-0 text-slate-200 ring-0"
      aria-label="Zoning color key"
    >
      <CardHeader className="flex flex-row items-center justify-between gap-2 px-3 py-2">
        <CardTitle className="flex items-center gap-2 font-mono text-xs font-semibold text-slate-100">
          <Layers className="h-3.5 w-3.5 text-cyan-300" />
          Zoning Key
        </CardTitle>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          aria-label={open ? "Collapse zoning key" : "Expand zoning key"}
          className="h-6 w-6 text-slate-400 hover:bg-white/5 hover:text-slate-100"
        >
          {open ? (
            <ChevronUp className="h-4 w-4" />
          ) : (
            <ChevronDown className="h-4 w-4" />
          )}
        </Button>
      </CardHeader>

      {open && (
        <CardContent className="max-h-[420px] overflow-y-auto border-t border-white/10 p-1.5 [scrollbar-color:rgba(148,163,184,0.3)_transparent] [scrollbar-width:thin]">
          {ZONE_FAMILIES.map((family) => {
            const isOpen = expanded.has(family.id);
            const swatches = family.compact
              ? [family.zones[0].color]
              : family.zones.map((zn) => zn.color);

            return (
              <div key={family.id}>
                <button
                  onClick={() => toggleFamily(family.id)}
                  aria-expanded={isOpen}
                  className="flex w-full items-center gap-2 rounded px-1.5 py-1.5 text-left hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan-400/60"
                >
                  {isOpen ? (
                    <ChevronDown className="h-3.5 w-3.5 shrink-0 text-slate-500" />
                  ) : (
                    <ChevronRight className="h-3.5 w-3.5 shrink-0 text-slate-500" />
                  )}
                  <span className="min-w-0 flex-1 truncate font-mono text-xs font-medium text-slate-200">
                    {family.label}
                  </span>
                  <span className="flex shrink-0 items-center gap-0.5">
                    {swatches.map((c, i) => (
                      <Swatch key={i} color={c} small />
                    ))}
                  </span>
                  <Badge
                    variant="outline"
                    className="h-4 shrink-0 border-white/15 px-1.5 font-mono text-[10px] font-normal text-slate-400"
                  >
                    {family.zones.length}
                  </Badge>
                </button>

                {isOpen && (
                  <div className="mb-1 ml-5 border-l border-white/10 pl-3">
                    {family.compact ? (
                      <Row
                        color={family.zones[0].color}
                        code={family.compact.code}
                        description={family.compact.description}
                      />
                    ) : (
                      family.zones.map((zn) => (
                        <Row
                          key={zn.code}
                          color={zn.color}
                          code={zn.code}
                          description={zn.description}
                        />
                      ))
                    )}
                  </div>
                )}
              </div>
            );
          })}

          <div className="mt-1 flex items-center gap-2.5 border-t border-white/10 px-1.5 pb-1 pt-2.5">
            <Swatch color={ZONE_FALLBACK.color} small />
            <p className="font-mono text-xs text-slate-400">
              {ZONE_FALLBACK.label}
            </p>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
