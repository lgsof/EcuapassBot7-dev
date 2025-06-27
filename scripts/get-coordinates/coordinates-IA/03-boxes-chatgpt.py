import fitz  # PyMuPDF

def extract_boxes_from_lines(pdf_path, tolerance=1.5):
    doc = fitz.open(pdf_path)
    page = doc[0]

    horizontals = []
    verticals = []

    for shape in page.get_drawings():
        for item in shape["items"]:
            if item[0] != "l":
                continue
            coords = item[1]

            # Validate coords: must be ((x0, y0), (x1, y1))
            if (
                isinstance(coords, tuple)
                and len(coords) == 2
                and all(isinstance(pt, (tuple, list)) and len(pt) == 2 for pt in coords)
            ):
                (x0, y0), (x1, y1) = coords
                if abs(y0 - y1) < tolerance:
                    horizontals.append((min(x0, x1), y0, max(x0, x1), y1))
                elif abs(x0 - x1) < tolerance:
                    verticals.append((x0, min(y0, y1), x1, max(y0, y1)))
            else:
                continue  # skip malformed

    boxes = []
    for h_top in horizontals:
        for h_bottom in horizontals:
            if h_bottom[1] <= h_top[1] + tolerance:
                continue
            for v_left in verticals:
                for v_right in verticals:
                    if v_right[0] <= v_left[0] + tolerance:
                        continue

                    top_y = h_top[1]
                    bottom_y = h_bottom[1]
                    left_x = v_left[0]
                    right_x = v_right[0]

                    if (
                        abs(h_top[0] - left_x) < tolerance and
                        abs(h_top[2] - right_x) < tolerance and
                        abs(h_bottom[0] - left_x) < tolerance and
                        abs(h_bottom[2] - right_x) < tolerance and
                        abs(v_left[1] - top_y) < tolerance and
                        abs(v_left[3] - bottom_y) < tolerance and
                        abs(v_right[1] - top_y) < tolerance and
                        abs(v_right[3] - bottom_y) < tolerance
                    ):
                        x = left_x
                        y = top_y
                        width = right_x - left_x
                        height = bottom_y - top_y
                        boxes.append((x, y, width, height))

    # Deduplicate
    unique = []
    for b in boxes:
        if not any(
            abs(b[0] - u[0]) < tolerance and
            abs(b[1] - u[1]) < tolerance and
            abs(b[2] - u[2]) < tolerance and
            abs(b[3] - u[3]) < tolerance
            for u in unique
        ):
            unique.append(b)

    unique.sort(key=lambda r: (r[1], r[0]))
    return unique


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_boxes.py <pdf_file>")
        sys.exit(1)

    path = sys.argv[1]
    boxes = extract_boxes_from_lines(path)

    if not boxes:
        print("No boxes detected.")
    else:
        for i, (x, y, w, h) in enumerate(boxes, 1):
            print(f"Box {i}: X={x:.2f}, Y={y:.2f}, W={w:.2f}, H={h:.2f}")

