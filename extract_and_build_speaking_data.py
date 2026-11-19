import fitz, os, re, json
from PIL import Image

DOWNLOADS_DIR = '/Users/yangcoi/Downloads/drive-download-20261119T040421Z-1-001'
OUT_IMG_DIR = '/Users/yangcoi/Documents/JDP2/speaking_images'
OUT_JSON_PATH = '/Users/yangcoi/Documents/JDP2/jpd123_speaking_pictures.json'

os.makedirs(OUT_IMG_DIR, exist_ok=True)

def normalize_text(t):
    if not t: return ''
    # convert full-width numbers
    trans = str.maketrans('０１２３４５６７８９', '0123456789')
    return t.translate(trans).strip()

def crop_image(page, bbox, out_path, margin=4):
    rect = fitz.Rect(bbox)
    clip_rect = fitz.Rect(
        max(0, rect.x0 - margin),
        max(0, rect.y0 - margin),
        min(page.rect.width, rect.x1 + margin),
        min(page.rect.height, rect.y1 + margin)
    )
    pix = page.get_pixmap(clip=clip_rect, dpi=200)
    pix.save(out_path)
    return out_path

print("Starting extraction of Speaking picture materials...")
