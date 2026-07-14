import Image from "next/image";
import fs from "fs";
import path from "path";

export function MuscariaGrid() {
  const dir = path.join(process.cwd(), "public", "masks");
  let files: string[] = [];
  try {
    files = fs.readdirSync(dir).filter((f) => f.endsWith(".png"));
  } catch {
    files = [];
  }

  const sample = files.slice(0, 12);

  return (
    <div className="my-6 not-prose">
      <div className="grid grid-cols-4 md:grid-cols-6 gap-2">
        {sample.map((f) => (
          <div
            key={f}
            className="aspect-square bg-stone-900 rounded overflow-hidden border border-stone-300"
          >
            <Image
              src={`/masks/${f}`}
              alt={`A. muscaria silhouette from iNaturalist observation`}
              width={200}
              height={200}
              className="w-full h-full object-contain invert"
            />
          </div>
        ))}
      </div>
      <p className="text-sm text-stone-600 mt-3 text-center">
        Sample of the {" "}
        <em>A. muscaria</em> silhouette corpus (12 of {files.length || 55} shown)
        after automated color-threshold segmentation and convex-hull filling.
      </p>
    </div>
  );
}
