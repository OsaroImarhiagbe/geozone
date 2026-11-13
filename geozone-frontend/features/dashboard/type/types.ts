// types/parcels.ts
export interface ParcelProperties {
  pid: string | null;
  address: string | null;
  zone_code: string | null;
  land_desc: string | null;
  land_sf: number | null;
}

export type ParcelGeometry =
  | { type: "Polygon"; coordinates: number[][][] }
  | { type: "MultiPolygon"; coordinates: number[][][][] };

export interface ParcelFeature {
  type: "Feature";
  properties: ParcelProperties;
  geometry: ParcelGeometry;
}

export interface ParcelFeatureCollection {
  type: "FeatureCollection";
  name: string;
  features: ParcelFeature[];
}

export interface BBox {
  minLng: number;
  minLat: number;
  maxLng: number;
  maxLat: number;
}

export interface Bounding {
  min_lng: number;
  min_lat: number;
  max_lng: number;
  max_lat: number;
  setMinLng: (min_lng: number) => void;
  setMinLat: (min_lat: number) => void;
  setMaxLng: (max_lng: number) => void;
  setMaxLat: (max_lat: number) => void;
}

// features/dashboard/type/analysis.ts
export type SelectedParcel = {
  pid: string;
  address?: string;
  zone_code?: string;
  land_desc?: string;
  land_sf?: number;
};

export type ParcelAnalysis = {
  summary: string;
  opportunities: string[];
  constraints: string[];
  nextSteps: string[];
};
