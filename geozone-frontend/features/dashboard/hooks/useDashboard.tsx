import { useQuery, useMutation } from "@tanstack/react-query";
import { ParcelService } from "../service/parcel";
import axios from "axios";

// features/dashboard/hooks/useParcelAnalysis.ts
import type {
  ParcelAnalysis,
  SelectedParcel,
} from "@/features/dashboard/type/types";

const key = process.env.NEXT_PUBLIC_MAP_BOX_KEY;

const parcels = new ParcelService();
export const useGetParcels = (
  min_lng: number,
  min_lat: number,
  max_lng: number,
  max_lat: number,
) => {
  return useQuery({
    // Include bbox in key so query refetches when user pans/zooms
    queryKey: ["parcels", min_lng, min_lat, max_lng, max_lat],
    queryFn: async () => {
      const response = await parcels.get_parcels(
        min_lng,
        min_lat,
        max_lng,
        max_lat,
      );
      console.log("response data", response.features);
      console.log("response data 2:", response.type, response.features.length);
      return response;
    },
    enabled: !!(min_lng && min_lat && max_lng && max_lat),
  });
};

export const useGetLocation = () => {
  return useMutation({
    mutationFn: async (search_text: string) => {
      const response = await axios.get(
        `https://api.mapbox.com/search/geocode/v6/forward?q=${search_text}&access_token=${key}`,
      );

      return response;
    },
  });
};

export function useParcelAnalysis() {
  return useMutation<ParcelAnalysis, Error, SelectedParcel[]>({
    mutationFn: async (parcels) => {
      const res = await fetch("/api/parcel-analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ parcels }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => null);
        throw new Error(body?.error ?? "Analysis failed. Try again.");
      }
      return res.json();
    },
  });
}
