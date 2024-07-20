import fitz
import os

# To get better resolution
# zoom_x = 2.0  # horizontal zoom
# zoom_y = 2.0  # vertical zoom
# mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

# filename = "invoice_101.pdf"


def pdf_to_image(filename, page):
    basename = os.path.basename(filename)
    base_filename, ext = os.path.splitext(basename)
    pathname = os.path.dirname(filename)
    out_filename = os.path.join(pathname, f"{page}.png")
    page = page - 1
    doc = fitz.open(filename)
    doc_page = doc.load_page(page)
    pix = doc_page.get_pixmap()
    pix.save(out_filename)
    return f"{page+1}"
