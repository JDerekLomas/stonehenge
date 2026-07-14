"use client";

import { useEffect, useRef, useState } from "react";

type Feature = {
  type: "Feature";
  properties: {
    artefact_id: number;
    object: string;
    class: string;
    site: string;
    county: string;
    region: string;
    dist_km_from_stonehenge: number;
    near_stonehenge: boolean;
  };
  geometry: { type: "Point"; coordinates: [number, number] };
};

type GeoJSON = {
  type: "FeatureCollection";
  features: Feature[];
  stonehenge: { lat: number; lon: number };
  near_radius_km: number;
};

const CLASS_COLOR: Record<string, string> = {
  "Class 2": "#2c7fb8",
  "Class 3": "#41b6c4",
  "Class 4": "#a1dab4",
  "Class 5": "#fdae61",
};
const CLASS_LABEL: Record<string, string> = {
  "Class 2": "Class 2 (Flat, ~2200-1900 BC)",
  "Class 3": "Class 3 (Flat, ~2000-1750 BC)",
  "Class 4": "Class 4 (Low-flanged, ~1800-1600 BC)",
  "Class 5": "Class 5 (Flanged, ~1700-1450 BC)",
};

const ALL_CLASSES = ["Class 2", "Class 3", "Class 4", "Class 5"];

export function FindspotMap() {
  const mapRef = useRef<HTMLDivElement>(null);
  const [enabled, setEnabled] = useState<Set<string>>(new Set(ALL_CLASSES));
  const [data, setData] = useState<GeoJSON | null>(null);
  const layersRef = useRef<Record<string, unknown>>({});
  const mapInstance = useRef<unknown>(null);

  useEffect(() => {
    fetch("/data/axe_findspots.geojson")
      .then((r) => r.json())
      .then(setData)
      .catch((e) => console.error("Failed to load findspots:", e));
  }, []);

  useEffect(() => {
    if (!data || !mapRef.current || mapInstance.current) return;
    let cancelled = false;

    (async () => {
      const L = (await import("leaflet")).default;
      await import("leaflet/dist/leaflet.css");
      if (cancelled) return;

      const map = L.map(mapRef.current!, {
        center: [52.5, -1.8],
        zoom: 6,
        scrollWheelZoom: false,
      });
      mapInstance.current = map;

      L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          maxZoom: 12,
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }
      ).addTo(map);

      // Stonehenge marker
      const stonehengeIcon = L.divIcon({
        html: `<div style="width:22px;height:22px;background:#b91c1c;border:2px solid #fff;border-radius:50%;box-shadow:0 1px 3px rgba(0,0,0,0.4);"></div>`,
        iconSize: [22, 22],
        iconAnchor: [11, 11],
        className: "",
      });
      L.marker([data.stonehenge.lat, data.stonehenge.lon], {
        icon: stonehengeIcon,
      })
        .bindPopup("<strong>Stonehenge</strong>")
        .addTo(map);

      // 100 km radius circle
      L.circle([data.stonehenge.lat, data.stonehenge.lon], {
        radius: data.near_radius_km * 1000,
        color: "#b91c1c",
        weight: 1.5,
        fillOpacity: 0.04,
        dashArray: "6 6",
      }).addTo(map);

      // Per-class layer groups
      const groups: Record<string, unknown> = {};
      for (const cls of ALL_CLASSES) {
        const grp = L.layerGroup();
        data.features
          .filter((f) => f.properties.class === cls)
          .forEach((f) => {
            const [lon, lat] = f.geometry.coordinates;
            L.circleMarker([lat, lon], {
              radius: 5,
              color: "#ffffff",
              weight: 1,
              fillColor: CLASS_COLOR[cls] ?? "#888",
              fillOpacity: 0.85,
            })
              .bindPopup(
                `<strong>${f.properties.object}</strong><br/>` +
                  `${f.properties.class}<br/>` +
                  `${f.properties.site}<br/>` +
                  `<em>${f.properties.county}</em><br/>` +
                  `${f.properties.dist_km_from_stonehenge} km from Stonehenge`
              )
              .addTo(grp as never);
          });
        (grp as never as { addTo: (m: unknown) => void }).addTo(map);
        groups[cls] = grp;
      }
      layersRef.current = groups;
    })();

    return () => {
      cancelled = true;
    };
  }, [data]);

  useEffect(() => {
    if (!layersRef.current || !mapInstance.current) return;
    const map = mapInstance.current as { addLayer: (l: unknown) => void; removeLayer: (l: unknown) => void };
    for (const cls of ALL_CLASSES) {
      const grp = layersRef.current[cls];
      if (!grp) continue;
      if (enabled.has(cls)) map.addLayer(grp);
      else map.removeLayer(grp);
    }
  }, [enabled]);

  const toggle = (cls: string) =>
    setEnabled((prev) => {
      const next = new Set(prev);
      if (next.has(cls)) next.delete(cls);
      else next.add(cls);
      return next;
    });

  const counts = data
    ? Object.fromEntries(
        ALL_CLASSES.map((cls) => [
          cls,
          data.features.filter((f) => f.properties.class === cls).length,
        ])
      )
    : {};
  const nearCounts = data
    ? Object.fromEntries(
        ALL_CLASSES.map((cls) => [
          cls,
          data.features.filter(
            (f) => f.properties.class === cls && f.properties.near_stonehenge
          ).length,
        ])
      )
    : {};

  return (
    <div className="my-8 not-prose">
      <div className="flex flex-wrap gap-2 mb-4">
        {ALL_CLASSES.map((cls) => (
          <button
            key={cls}
            onClick={() => toggle(cls)}
            className={`px-3 py-1.5 rounded-full text-xs border transition-colors ${
              enabled.has(cls)
                ? "text-white border-transparent"
                : "text-stone-600 bg-white border-stone-300"
            }`}
            style={
              enabled.has(cls)
                ? { backgroundColor: CLASS_COLOR[cls] }
                : undefined
            }
          >
            {CLASS_LABEL[cls]}
            {data ? ` — ${nearCounts[cls]}/${counts[cls]} near` : ""}
          </button>
        ))}
      </div>
      <div ref={mapRef} className="w-full" />
      <p className="text-sm text-stone-600 mt-3 text-center">
        Figure 5. British Early Bronze Age axe findspots (n = 275) colored by
        Needham class. Click a class label to toggle. Dashed circle: 100 km
        radius around Stonehenge.
      </p>
    </div>
  );
}
