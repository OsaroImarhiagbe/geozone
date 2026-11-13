// features/dashboard/lib/zone-colors.ts
// Single source of truth for zone colors: the map paint expression, the legend,
// and any chip that needs a zone color all read from here.
import type { ExpressionSpecification } from "mapbox-gl";

export type ZoneEntry = { code: string; description: string; color: string };
export type ZoneFamily = {
  id: string;
  label: string;
  zones: ZoneEntry[];
  // When set, the legend shows ONE row for the whole family instead of listing every code
  compact?: { code: string; description: string };
};

const z = (code: string, description: string, color: string): ZoneEntry => ({
  code,
  description,
  color,
});

// Coordinated Development Districts are site-specific (#18 doesn't exist in the data),
// so they share one color instead of 21 indistinguishable shades.
const CDD_COLOR = "#2dd4bf";
const CDD_NUMBERS = [
  ...Array.from({ length: 17 }, (_, i) => String(i + 1)),
  "17a",
  "19",
  "20",
  "21",
  "22",
];

export const ZONE_FAMILIES: ZoneFamily[] = [
  {
    id: "single-family",
    label: "Residential, single-family",
    zones: [
      z("R20", "Single Family, 20,000 sf lot", "#fef08a"),
      z("R12", "Single Family, 12,000 sf lot", "#fde047"),
      z("R8", "Single Family, 8,000 sf lot", "#facc15"),
      z("R5", "Single Family, 5,000 sf lot", "#eab308"),
      z("R2-5", "Single or Two Family, 5,000 sf lot", "#ca8a04"),
    ],
  },
  {
    id: "multi-family",
    label: "Residential, townhouse & apartment",
    zones: [
      z("RT", "Townhouse", "#fed7aa"),
      z("RB", "Townhouse", "#fdba74"),
      z("RM", "Townhouse", "#fb923c"),
      z("RA", "Multi-Family", "#f97316"),
      z("RCX", "Medium Density Apartment", "#ea580c"),
      z("RC", "High Density Apartment", "#c2410c"),
      z("RD", "High Density Apartment (none after 1965)", "#9a3412"),
    ],
  },
  {
    id: "commercial",
    label: "Commercial",
    zones: [
      z("CL", "Commercial Low", "#fecaca"),
      z("CSL", "Commercial Service Low", "#fca5a5"),
      z("NR", "Neighborhood Retail", "#f87171"),
      z("KR", "King Street Urban Retail", "#fb7185"),
      z("CC", "Commercial Community", "#ef4444"),
      z("CG", "Commercial General", "#e11d48"),
      z("CR", "Commercial Regional", "#dc2626"),
      z("CD", "Commercial Downtown", "#be123c"),
      z("CDX", "Commercial Downtown, Old Town North", "#9f1239"),
    ],
  },
  {
    id: "mixed-use",
    label: "Commercial residential mixed use",
    zones: [
      z("CRMU/L", "Mixed Use (Low)", "#f9a8d4"),
      z("CRMU/M", "Mixed Use (Medium)", "#f472b6"),
      z("CRMU/H", "Mixed Use (High)", "#ec4899"),
      z("CRMU/X", "Mixed Use (Old Town North)", "#db2777"),
    ],
  },
  {
    id: "office",
    label: "Office",
    zones: [
      z("OC", "Office Commercial", "#d8b4fe"),
      z("OCM(50)", "Office Commercial Medium (50)", "#c084fc"),
      z("OCM(100)", "Office Commercial Medium (100)", "#a855f7"),
      z("OCH", "Office Commercial High", "#9333ea"),
      z("CO", "Commercial Office Planned Development", "#7c3aed"),
    ],
  },
  {
    id: "cdd",
    label: "Coordinated development districts",
    compact: {
      code: "CDD #1–#22",
      description: "Site-specific districts, shown in one color",
    },
    zones: CDD_NUMBERS.map((n) =>
      z(`CDD#${n}`, `Coordinated Development District #${n}`, CDD_COLOR),
    ),
  },
  {
    id: "industrial",
    label: "Industrial & utility",
    zones: [
      z("I", "Industrial", "#e2e8f0"),
      z("DD", "Wholesale Business", "#cbd5e1"),
      z("UT", "Utility and Transportation", "#94a3b8"),
    ],
  },
  {
    id: "water-open",
    label: "Waterfront & open space",
    zones: [
      z("W-1", "Waterfront Mixed Use", "#60a5fa"),
      z("WPR", "Waterfront Park and Recreation", "#38bdf8"),
      z("POS", "Public Open Space", "#4ade80"),
    ],
  },
];

export const ZONE_FALLBACK = { label: "Other / unmapped", color: "#64748b" };

// code -> color, for chips and any non-map UI
export const ZONE_COLOR_BY_CODE: Record<string, string> = Object.fromEntries(
  ZONE_FAMILIES.flatMap((f) => f.zones.map((zn) => [zn.code, zn.color])),
);

export const getZoneColor = (code?: string | null) =>
  (code && ZONE_COLOR_BY_CODE[code]) || ZONE_FALLBACK.color;

// Mapbox `match` needs unique labels, so group codes that share a color (the CDDs)
const byColor = new Map<string, string[]>();
const seen = new Set<string>();
for (const zn of ZONE_FAMILIES.flatMap((f) => f.zones)) {
  if (seen.has(zn.code)) continue;
  seen.add(zn.code);
  byColor.set(zn.color, [...(byColor.get(zn.color) ?? []), zn.code]);
}

export const zoneFillExpression: ExpressionSpecification = [
  "match",
  ["to-string", ["get", "zone_code"]],
  ...[...byColor.entries()].flatMap(([color, codes]) => [codes, color]),
  ZONE_FALLBACK.color,
] as ExpressionSpecification;
