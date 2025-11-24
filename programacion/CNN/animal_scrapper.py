"""
download_and_resize.py

Downloads images for several animal classes using icrawler (Bing),
deduplicates using perceptual hashing (imagehash), resizes to 40x40 using OpenCV,
and saves images per-class.

Usage:
    python download_and_resize.py
"""

import os
import shutil
from icrawler.builtin import BingImageCrawler
from PIL import Image
import imagehash
import cv2
import numpy as np
from tqdm import tqdm
import time
import threading

# ===== user parameters =====
TARGET_PER_CLASS = 5000     # desired images per class (adjust if too aggressive)
CLASSES = ["dog", "cat", "turtle", "ant", "ladybug"]
OUTPUT_DIR = "images_raw"   # where raw crawled images will be saved
RESIZED_DIR = "images_40x40"  # where final 40x40 images will go
TEMP_DOWNLOAD_PER_CLASS = int(TARGET_PER_CLASS * 1.2)  # download slightly more to allow for failures
CRAWL_THREADS = 4           # icrawler threads
CRAWL_TIMEOUT = 5           # seconds between downloads (sleep) to be polite
# ===========================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(RESIZED_DIR, exist_ok=True)

def crawl_class(query, out_dir, max_num):
    """
    Use icrawler BingImageCrawler to download up to max_num images for a query.
    """
    crawler = BingImageCrawler(storage={'root_dir': out_dir})
    # Filters: you can add 'size' etc to filters dictionary if needed
    # Example: filters = dict(size='large')
    filters = {}
    try:
        crawler.crawl(
            keyword=query,
            max_num=max_num,
            #threads=CRAWL_THREADS,
            #timeout=CRAWL_TIMEOUT,
            filters=filters
        )
    except Exception as e:
        print(f"[crawl] error while crawling {query}: {e}")

def safe_open_image(path):
    """Open an image with PIL and convert to RGB if possible; return PIL.Image or None."""
    try:
        img = Image.open(path)
        img = img.convert("RGB")
        return img
    except Exception:
        return None

def resize_and_save_pil(img_pil, out_path, size=(40,40)):
    """Resize PIL image and save as PNG using OpenCV (ensures consistent format)."""
    # Convert PIL to numpy array (RGB)
    arr = np.array(img_pil)
    # convert to BGR for OpenCV
    arr = arr[:, :, ::-1]
    # resize with INTER_AREA (good for downsampling)
    resized = cv2.resize(arr, size, interpolation=cv2.INTER_AREA)
    # Save as PNG to preserve quality
    cv2.imwrite(out_path, resized)

def process_class(class_name, raw_dir, out_dir, target_count):
    """
    Walk raw_dir, deduplicate by perceptual hash, resize and save to out_dir until target_count reached.
    Images are saved with class_name as prefix.
    """
    os.makedirs(out_dir, exist_ok=True)
    seen_hashes = set()
    saved = 0

    # List files in a deterministic order
    file_list = []
    for root, _, files in os.walk(raw_dir):
        for f in files:
            file_list.append(os.path.join(root, f))
    file_list.sort()

    for path in tqdm(file_list, desc=f"Processing {os.path.basename(raw_dir)}", unit="img"):
        if saved >= target_count:
            break
        # open PIL
        img_pil = safe_open_image(path)
        if img_pil is None:
            continue
        # compute perceptual hash (phash)
        try:
            ph = imagehash.phash(img_pil)
        except Exception:
            continue
        if ph in seen_hashes:
            continue
        # optional: skip too small images
        if img_pil.width < 20 or img_pil.height < 20:
            continue

        # save resized image with class prefix
        out_path = os.path.join(out_dir, f"{class_name}_{saved:06d}.png")
        try:
            resize_and_save_pil(img_pil, out_path, size=(40, 40))
        except Exception:
            continue

        seen_hashes.add(ph)
        saved += 1

    return saved

def main():
    # 1) Crawl each class into a separate raw folder
    for cls in CLASSES:
        raw_cls_dir = os.path.join(OUTPUT_DIR, cls)
        if os.path.exists(raw_cls_dir) and len(os.listdir(raw_cls_dir)) >= TEMP_DOWNLOAD_PER_CLASS:
            print(f"[crawl] raw folder for '{cls}' already has many files; skipping crawling.")
            continue
        print(f"[crawl] starting crawl for '{cls}' -> {raw_cls_dir} (target {TEMP_DOWNLOAD_PER_CLASS})")
        os.makedirs(raw_cls_dir, exist_ok=True)
        crawl_class(cls, raw_cls_dir, TEMP_DOWNLOAD_PER_CLASS)
        # small polite pause between classes
        time.sleep(2)

    # 2) Process each class: dedupe + resize -> final folder
    summary = {}
    for cls in CLASSES:
        raw_cls_dir = os.path.join(OUTPUT_DIR, cls)
        resized_cls_dir = os.path.join(RESIZED_DIR, cls)
        print(f"[process] class '{cls}': raw={raw_cls_dir} -> resized={resized_cls_dir}")
        saved = process_class(cls, raw_cls_dir, resized_cls_dir, TARGET_PER_CLASS)
        summary[cls] = saved
        print(f"[done] class '{cls}': saved {saved}/{TARGET_PER_CLASS}")

    print("Summary:")
    for cls, num in summary.items():
        print(f"  {cls}: {num}")

if __name__ == "__main__":
    main()
