import { create } from "zustand";
import { Bounding } from "../type/types";

// features/dashboard/store/useSelectedParcels.ts

import type { SelectedParcel } from "@/features/dashboard/type/types";

export const useDashboardStore = create<Bounding>((set) => ({
  min_lng: -77.14537,
  min_lat: 38.7844,
  max_lng: -77.01988,
  max_lat: 38.84699,
  setMinLng: (min_lng: number) => set({ min_lng: min_lng }),
  setMinLat: (min_lat: number) => set({ min_lat: min_lat }),
  setMaxLng: (max_lng: number) => set({ max_lng: max_lng }),
  setMaxLat: (max_lat: number) => set({ max_lat: max_lat }),
}));

type ParcelsState = {
  parcels: SelectedParcel[];
  toggle: (p: SelectedParcel) => void;
  remove: (pid: string) => void;
  clear: () => void;
};

export const useSelectedParcels = create<ParcelsState>((set) => ({
  parcels: [],
  toggle: (p) =>
    set((s) =>
      s.parcels[0]?.pid === p.pid ? { parcels: [] } : { parcels: [p] },
    ),
  remove: (pid) =>
    set((s) => ({ parcels: s.parcels.filter((x) => x.pid !== pid) })),
  clear: () => set({ parcels: [] }),
}));
