"use client";
import { useRef, useEffect, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { useDashboardStore } from "../store/useDashboardStore";
import { useGetParcels } from "../hooks/useDashboard";
// import { Geocoder } from "@mapbox/search-js-react";
let key: string;
if (process.env.NEXT_PUBLIC_MAP_BOX_KEY) {
  key = process.env.NEXT_PUBLIC_MAP_BOX_KEY;
}

export default function Map() {
  const mapRef = useRef<mapboxgl.Map | null>(null);
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  const min_lng = useDashboardStore((s) => s.min_lng);
  const min_lat = useDashboardStore((s) => s.min_lat);
  const max_lng = useDashboardStore((s) => s.max_lng);
  const max_lat = useDashboardStore((s) => s.max_lat);
  const setMinLng = useDashboardStore((s) => s.setMinLng);
  const setMinLat = useDashboardStore((s) => s.setMinLat);
  const setMaxLng = useDashboardStore((s) => s.setMaxLng);
  const setMaxLat = useDashboardStore((s) => s.setMaxLat);

  const { data: parcelData } = useGetParcels(
    min_lng,
    min_lat,
    max_lng,
    max_lat,
  );

  console.log("Map Box Name:", parcelData);

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
    });
    mapRef.current = map;

    const syncBounds = () => {
      const b = map.getBounds();
      if (!b) return;
      setMinLng(b.getWest());
      setMinLat(b.getSouth());
      setMaxLng(b.getEast());
      setMaxLat(b.getNorth());
    };

    map.on("load", () => {
      map.addSource("alexandria", {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] },
      });
      map.addLayer({
        id: "parcels-fill",
        type: "fill",
        source: "alexandria",
        slot: "top",
        minzoom: 14,
        paint: { "fill-color": "#3b82f6", "fill-opacity": 0.4 },
      });
      map.addLayer({
        id: "parcels-outline",
        type: "line",
        source: "alexandria",
        slot: "top",
        minzoom: 14,
        paint: { "line-color": "#ff0000", "line-width": 3 },
      });
      setMapLoaded(true);
      syncBounds();
    });

    map.on("moveend", syncBounds);

    return () => {
      map.remove();
      mapRef.current = null;
      setMapLoaded(false);
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // 2. Push fetched data into the source (only when everything is ready and valid)
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !mapLoaded || !parcelData) return;
    (
      map.getSource("alexandria") as mapboxgl.GeoJSONSource | undefined
    )?.setData(parcelData);
  }, [parcelData, mapLoaded]);

  return (
    <div
      id="map-container"
      className="relative h-[580px] w-full overflow-hidden rounded-xl"
      ref={mapContainerRef}
    />
  );
}
