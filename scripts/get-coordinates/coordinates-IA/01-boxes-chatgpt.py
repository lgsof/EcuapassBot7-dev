import fitz  # PyMuPDF
import sys

def extract_boxes_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    all_boxes = []

    for page_number, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                rect = b["bbox"]  # (x0, y0, x1, y1)
                x = rect[0]
                y = rect[1]
                width = rect[2] - rect[0]
                height = rect[3] - rect[1]
                all_boxes.append({
                    "page": page_number,
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height
                })

    return all_boxes

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_boxes.py <pdf_file>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    boxes = extract_boxes_from_pdf(pdf_file)
    for box in boxes:
        print(f"Page {box['page']}: X={box['x']:.2f}, Y={box['y']:.2f}, W={box['width']:.2f}, H={box['height']:.2f}")

