import fitz  # PyMuPDF

def extract_visual_boxes_first_page(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]  # Only the first page

    # Extract drawing objects (lines, rectangles, etc.)
    shapes = page.get_drawings()
    rects = []

    for shape in shapes:
        for item in shape["items"]:
            if item[0] == "re":  # Rectangle
                x, y, w, h = item[1]
                rects.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })

    # Sort top-left to bottom-right: first by Y (top to bottom), then X (left to right)
    rects.sort(key=lambda r: (r["y"], r["x"]))

    return rects

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_visual_rects.py <pdf_file>")
        sys.exi

