"use client";

export function SketchfabEmbed({
  modelId,
  title,
  height = 500,
}: {
  modelId: string;
  title: string;
  height?: number;
}) {
  return (
    <div
      className="rounded-md overflow-hidden border border-stone-200 bg-black"
      style={{ height }}
    >
      <iframe
        title={title}
        frameBorder="0"
        allow="autoplay; fullscreen; xr-spatial-tracking"
        allowFullScreen
        src={`https://sketchfab.com/models/${modelId}/embed?autospin=0.4&ui_theme=dark&ui_infos=0&ui_controls=1`}
        style={{ width: "100%", height: "100%" }}
      />
    </div>
  );
}
