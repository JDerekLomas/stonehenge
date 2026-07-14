"""
Extract embedded images from a Google-Sheet-exported XLSX and map each
image back to the carving/axe row it was anchored to.

For each XLSX:
  1. Read all xl/media/*.jpg|png files
  2. Read xl/drawings/drawingN.xml to get image->cell anchor
  3. Read xl/worksheets/sheetN.xml to find the row's ID column value
  4. Save each image as data/{corpus}/F{id}.jpg
"""

import base64
import json
import re
import zipfile
from io import BytesIO
from pathlib import Path
from xml.etree import ElementTree as ET

import pandas as pd

ROOT = Path(__file__).parent.parent

# XLSX namespaces
NS = {
    "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "xdr": "http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def col_letter_to_num(letter):
    n = 0
    for c in letter:
        n = n * 26 + (ord(c.upper()) - ord("A") + 1)
    return n - 1


def parse_drawing(drawing_xml: bytes, rels_xml: bytes):
    """Return list of {image_target, from_row, from_col} for each image
    in this drawing file. Both one-cell-anchor and two-cell-anchor
    ('twoCellAnchor') are supported."""
    # Parse rels: rel id -> media/imageN.png
    rels = {}
    if rels_xml:
        root = ET.fromstring(rels_xml)
        for rel in root:
            rid = rel.attrib.get("Id")
            target = rel.attrib.get("Target", "")
            if "/media/" in target or target.startswith("../media"):
                rels[rid] = target

    tree = ET.fromstring(drawing_xml)
    results = []
    for anchor_tag in ("oneCellAnchor", "twoCellAnchor", "absoluteAnchor"):
        for anchor in tree.iter(f"{{{NS['xdr']}}}{anchor_tag}"):
            frm = anchor.find(f"{{{NS['xdr']}}}from")
            if frm is None:
                # absoluteAnchor has no from; try to skip
                continue
            col_el = frm.find(f"{{{NS['xdr']}}}col")
            row_el = frm.find(f"{{{NS['xdr']}}}row")
            if col_el is None or row_el is None:
                continue
            col = int(col_el.text)
            row = int(row_el.text)

            # Find blip inside the pic descendant
            blip = None
            for pic in anchor.iter(f"{{{NS['xdr']}}}pic"):
                for b in pic.iter(f"{{{NS['a']}}}blip"):
                    blip = b
                    break
            if blip is None:
                continue
            rid = blip.attrib.get(f"{{{NS['r']}}}embed")
            target = rels.get(rid)
            if not target:
                continue
            # Normalize path — drawing rels are relative to xl/drawings/, so
            # target "../media/imageN.jpg" resolves to "xl/media/imageN.jpg"
            if target.startswith("../"):
                target = "xl/" + target[3:]
            elif target.startswith("/"):
                target = target.lstrip("/")
            else:
                target = "xl/drawings/" + target
            results.append({"target": target, "row": row, "col": col})
    return results


def parse_sheet_ids(sheet_xml: bytes, id_col_idx: int, shared_strings: list):
    """Return a dict row_index -> id_value (numeric or string) for the given
    column index (0-based). Row index is 0-based to match anchor coords."""
    tree = ET.fromstring(sheet_xml)
    ids = {}
    for row_el in tree.iter(f"{{{NS['main']}}}row"):
        r = int(row_el.attrib.get("r", "0")) - 1  # 1-based -> 0-based
        for c_el in row_el.iter(f"{{{NS['main']}}}c"):
            ref = c_el.attrib.get("r", "")
            m = re.match(r"([A-Z]+)(\d+)", ref)
            if not m:
                continue
            col_idx = col_letter_to_num(m.group(1))
            if col_idx != id_col_idx:
                continue
            t_attr = c_el.attrib.get("t", "n")
            v_el = c_el.find(f"{{{NS['main']}}}v")
            if v_el is None:
                is_el = c_el.find(f"{{{NS['main']}}}is")
                if is_el is not None:
                    t = is_el.find(f"{{{NS['main']}}}t")
                    ids[r] = t.text if t is not None else None
                continue
            raw = v_el.text
            if t_attr == "s":
                ids[r] = shared_strings[int(raw)]
            else:
                ids[r] = raw
    return ids


def parse_shared_strings(ss_xml: bytes):
    if not ss_xml:
        return []
    tree = ET.fromstring(ss_xml)
    ss = []
    for si in tree.iter(f"{{{NS['main']}}}si"):
        # Combine all <t> under this si
        parts = []
        for t in si.iter(f"{{{NS['main']}}}t"):
            if t.text:
                parts.append(t.text)
        ss.append("".join(parts))
    return ss


def parse_sheet_relationships(rels_xml: bytes):
    """Return {rid: target} mapping for a sheet's relationships."""
    if not rels_xml:
        return {}
    tree = ET.fromstring(rels_xml)
    return {r.attrib["Id"]: r.attrib["Target"] for r in tree}


def parse_sheet_drawing_ref(sheet_xml: bytes):
    """Return the r:id of the sheet's <drawing> element, or None."""
    tree = ET.fromstring(sheet_xml)
    for d in tree.iter(f"{{{NS['main']}}}drawing"):
        return d.attrib.get(f"{{{NS['r']}}}id")
    return None


def process_xlsx(xlsx_path: Path, id_col_idx: int, corpus_name: str,
                 id_prefix: str = "F", sheet_idx: int = 1):
    """Extract images from the specified sheet_idx (1-based) and map each to
    its ID column value."""
    out_dir = ROOT / "data" / corpus_name
    out_dir.mkdir(exist_ok=True, parents=True)

    z = zipfile.ZipFile(xlsx_path)

    shared_strings = parse_shared_strings(
        z.read("xl/sharedStrings.xml") if "xl/sharedStrings.xml" in z.namelist() else b""
    )

    sheet_path = f"xl/worksheets/sheet{sheet_idx}.xml"
    sheet_rels_path = f"xl/worksheets/_rels/sheet{sheet_idx}.xml.rels"
    if sheet_path not in z.namelist():
        print(f"Sheet {sheet_idx} not found in {xlsx_path}")
        return

    sheet_xml = z.read(sheet_path)
    ids_by_row = parse_sheet_ids(sheet_xml, id_col_idx, shared_strings)

    drawing_rid = parse_sheet_drawing_ref(sheet_xml)
    if not drawing_rid:
        print(f"Sheet {sheet_idx} has no drawing reference")
        return

    sheet_rels = parse_sheet_relationships(
        z.read(sheet_rels_path) if sheet_rels_path in z.namelist() else b""
    )
    drawing_target = sheet_rels.get(drawing_rid)
    if not drawing_target:
        print(f"Drawing rel {drawing_rid} not found")
        return
    if drawing_target.startswith("../"):
        drawing_path = "xl/" + drawing_target[3:]
    elif drawing_target.startswith("/xl"):
        drawing_path = drawing_target.lstrip("/")
    else:
        drawing_path = "xl/" + drawing_target

    drawing_xml = z.read(drawing_path)
    rels_key = drawing_path.replace("drawings/", "drawings/_rels/") + ".rels"
    rels_xml = z.read(rels_key) if rels_key in z.namelist() else b""

    anchors = parse_drawing(drawing_xml, rels_xml)
    print(f"  Sheet {sheet_idx}: {len(anchors)} image anchors, "
          f"{len(ids_by_row)} rows with IDs")

    saved = 0
    for a in anchors:
        row = a["row"]
        # Try nearest ID row within 1-row tolerance (images sometimes anchor
        # to the row above their cell)
        rid = None
        for offset in (0, -1, 1, -2, 2):
            if row + offset in ids_by_row:
                rid = ids_by_row[row + offset]
                break
        if rid is None:
            continue
        rid_clean = rid.replace(".", "_").replace("/", "_").strip()
        if not rid_clean:
            continue
        media = a["target"]
        if media not in z.namelist():
            continue
        blob = z.read(media)
        ext = Path(media).suffix or ".jpg"
        # Use ID_prefix like F for carvings, A for axes
        out_path = out_dir / f"{id_prefix}{rid_clean}{ext}"
        out_path.write_bytes(blob)
        saved += 1

    print(f"  Saved {saved} images to {out_dir}")
    return saved


def main():
    print("=== Rock Carvings and Axeheads sheet ===")
    xlsx_path = ROOT / "data" / "raw" / "rock_carvings.xlsx"
    if not xlsx_path.exists():
        # Save from the cached tool result
        cache = Path("/Users/dereklomas/.claude/projects/-Users-dereklomas-stonehenge/3c08e3a2-4ff0-477c-a18b-9358bd91878b/tool-results/mcp-claude_ai_Google_Drive-download_file_content-1784041271408.txt")
        d = json.load(open(cache))
        xlsx_path.parent.mkdir(parents=True, exist_ok=True)
        xlsx_path.write_bytes(base64.b64decode(d["content"]))
        print(f"  Wrote {xlsx_path.stat().st_size} bytes to {xlsx_path}")

    # 'Carving#' is column B (index 1) on the first sheet.
    process_xlsx(xlsx_path, id_col_idx=1, corpus_name="carving_images",
                 id_prefix="F", sheet_idx=1)


if __name__ == "__main__":
    main()
