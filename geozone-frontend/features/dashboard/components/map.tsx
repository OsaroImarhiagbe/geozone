"use client";
import { useRef, useEffect, useState, useMemo } from "react";
// import { usePathname, useRouter, useSearchParams } from "next/navigation";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import {
  useDashboardStore,
  useSelectedParcels,
} from "../store/useDashboardStore";
import { useGetParcels } from "../hooks/useDashboard";
import { zoneFillExpression } from "@/lib/zone-colors";

import ZoneLegend from "@/features/dashboard/components/dashboard-zone-legend";

const key = process.env.NEXT_PUBLIC_MAP_BOX_KEY ?? "";

function Bracket({ className }: { className: string }) {
  return (
    <span
      className={`pointer-events-none absolute h-5 w-5 border-slate-400/60 ${className}`}
    />
  );
}

export default function Map() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const coordsRef = useRef<HTMLSpanElement | null>(null);
  const zoomRef = useRef<HTMLSpanElement | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  // const router = useRouter();
  // const pathname = usePathname();
  // const searchParams = useSearchParams();

  const min_lng = useDashboardStore((s) => s.min_lng);
  const min_lat = useDashboardStore((s) => s.min_lat);
  const max_lng = useDashboardStore((s) => s.max_lng);
  const max_lat = useDashboardStore((s) => s.max_lat);

  const setMinLng = useDashboardStore((s) => s.setMinLng);
  const setMinLat = useDashboardStore((s) => s.setMinLat);
  const setMaxLng = useDashboardStore((s) => s.setMaxLng);
  const setMaxLat = useDashboardStore((s) => s.setMaxLat);

  // Inside Map component
  const parcels = useSelectedParcels((s) => s.parcels);
  console.log("Selected Parcels:", parcels);

  const selectedPids = useMemo(() => parcels.map((p) => p.pid), [parcels]);

  const { data: parcelData } = useGetParcels(
    min_lng,
    min_lat,
    max_lng,
    max_lat,
  );

  // const params = new URLSearchParams(searchParams.toString());

  // params.set("min_lng", min_lng.toString());
  // params.set("min_lat", min_lat.toString());
  // params.set("max_lng", max_lng.toString());
  // params.set("max_lat", max_lat.toString());

  // const queryString = params.toString();

  // // Updates browser URL to: /your-page?min_lng=-77.08...&min_lat=38.79...
  // router.replace(`${pathname}?${queryString}`, { scroll: false });

  // 1. Create the map ONCE
  useEffect(() => {
    const container = mapContainerRef.current;
    if (!container) return;

    const map = new mapboxgl.Map({
      accessToken: key,
      container,
      style: "mapbox://styles/mapbox/standard",
      center: [-77.0469, 38.8048],
      zoom: 15,
      pitch: 45,
    });
    mapRef.current = map;

    map.addControl(
      new mapboxgl.NavigationControl({ visualizePitch: true }),
      "top-right",
    );
    map.addControl(
      new mapboxgl.ScaleControl({ unit: "imperial" }),
      "bottom-right",
    );

    const syncBounds = () => {
      const b = map.getBounds();
      if (!b) return;
      setMinLng(b.getWest());
      setMinLat(b.getSouth());
      setMaxLng(b.getEast());
      setMaxLat(b.getNorth());
    };

    const writeZoom = () => {
      if (zoomRef.current)
        zoomRef.current.textContent = map.getZoom().toFixed(2);
    };

    mapRef.current.on("load", () => {
      map.addSource("alexandria", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      mapRef.current?.addLayer({
        id: "parcels-fill",
        type: "fill",
        source: "alexandria",
        slot: "top",
        minzoom: 14,
        paint: {
          "fill-opacity": 0.6,
          "fill-color": zoneFillExpression,
        },
      });

      mapRef.current?.addLayer({
        id: "parcels-outline",
        type: "line",
        source: "alexandria",
        slot: "top",
        minzoom: 14,
        paint: { "line-color": "#000", "line-width": 1.5 },
      });

      mapRef.current?.addLayer({
        id: "parcels-selected",
        type: "line",
        source: "alexandria",
        slot: "top",
        minzoom: 14,
        filter: ["in", ["get", "pid"], ["literal", []]],
        paint: { "line-color": "#22d3ee", "line-width": 3 },
      });

      setMapLoaded(true);
      syncBounds();
      writeZoom();

      // Pointer cursor on hover
      mapRef.current?.on("mouseenter", "parcels-fill", () => {
        const map = mapRef.current;
        if (map) map.getCanvas().style.cursor = "pointer";
      });
      mapRef.current?.on("mouseleave", "parcels-fill", () => {
        const map = mapRef.current;
        if (map) map.getCanvas().style.cursor = "";
      });

      mapRef.current?.on("click", "parcels-fill", (e) => {
        if (!e.features || e.features.length === 0) return;
        const props = e.features[0]?.properties;
        if (!props) return;

        useSelectedParcels.getState().toggle({
          pid: String(props.pid),
          address: props.address,
          zone_code: props.zone_code,
          land_desc: props.land_desc,
          land_sf: Number(props.land_sf),
        });
      });
    });

    // Update HUD readouts through refs so the map never re-renders React
    mapRef.current.on("mousemove", (e) => {
      if (!coordsRef.current) return;
      const { lat, lng } = e.lngLat;
      coordsRef.current.textContent = `${Math.abs(lat).toFixed(5)}° ${lat >= 0 ? "N" : "S"}  ${Math.abs(lng).toFixed(5)}° ${lng >= 0 ? "E" : "W"}`;
    });
    mapRef.current.on("zoom", writeZoom);
    mapRef.current.on("moveend", syncBounds);

    return () => {
      map.remove();
      mapRef.current = null;
      setMapLoaded(false);
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // 2. Push fetched data into the source
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !mapLoaded || !parcelData) return;
    (
      map.getSource("alexandria") as mapboxgl.GeoJSONSource | undefined
    )?.setData(parcelData);
  }, [parcelData, mapLoaded]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map || !mapLoaded) return;
    map.setFilter("parcels-selected", [
      "in",
      ["get", "pid"],
      ["literal", selectedPids],
    ]);
  }, [mapLoaded, selectedPids]);

  return (
    <div className="relative h-[calc(100vh-260px)] min-h-[680px] min-w-0 overflow-hidden rounded-lg border border-white/10 bg-[#05080F]">
      <div id="map-container" ref={mapContainerRef} className="h-full w-full" />

      {/* Corner brackets */}
      <Bracket className="left-2 top-2 border-l border-t" />
      <Bracket className="right-2 top-2 border-r border-t" />
      <Bracket className="bottom-2 left-2 border-b border-l" />
      <Bracket className="bottom-2 right-2 border-b border-r" />

      {/* Title chip */}
      <div className="pointer-events-none absolute left-5 top-5 flex items-center gap-2 rounded-md border border-white/10 bg-[#070C14] px-3 py-1.5 font-mono text-xs text-slate-300">
        <span className="telemetry-dot h-1.5 w-1.5 rounded-full bg-cyan-400" />
        Alexandria, VA · Parcel Layer
      </div>

      {/* Zoning key */}
      <div className="absolute right-5 bottom-16 z-10">
        <ZoneLegend />
      </div>

      {/* Readout */}
      <div className="pointer-events-none absolute bottom-5 left-5 flex items-center gap-4 rounded-md border border-white/10 bg-[#070C14] px-3 py-1.5 font-mono text-xs tabular-nums text-cyan-200">
        <span ref={coordsRef}>—</span>
        <span className="text-slate-500">|</span>
        <span className="text-slate-400">
          Zoom{" "}
          <span ref={zoomRef} className="text-cyan-200">
            —
          </span>
        </span>
      </div>
    </div>
  );
}
