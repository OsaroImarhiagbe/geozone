// import { api } from "@/api/apiClient";
import { ParcelFeatureCollection } from "../type/types";

import axios from "axios";
export class ParcelService {
  async get_parcels(
    min_lng: number,
    min_lat: number,
    max_lng: number,
    max_lat: number,
  ) {
    const response = await axios.get<ParcelFeatureCollection>(
      "http://localhost:8000/api/v1/parcels/bbox",
      {
        params: {
          min_lng: min_lng,
          min_lat: min_lat,
          max_lng: max_lng,
          max_lat: max_lat,
        },
      },
    );
    console.log("parcel server respose:", response);
    return JSON.parse(response.data) as ParcelFeatureCollection;
  }
}
