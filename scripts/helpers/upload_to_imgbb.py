"""
Upload gallery images to ImgBB and save CDN URLs to a progress file.
Run from the project root: python3 scripts/helpers/upload_to_imgbb.py

Resumable: already-uploaded images are skipped.
Progress is saved after every upload in data/imgbb-uploads.json.
"""

import os
import json
import time
import base64
import urllib.request
import urllib.parse
import urllib.error

API_KEY = "868bd4e377fdbce30e5ee44f8e1c7f4f"
UPLOAD_URL = "https://api.imgbb.com/1/upload"
PROGRESS_FILE = "data/imgbb-uploads.json"

# Galleries to upload: relative path from images/ → label for logging
GALLERIES = [
    "gallery",
    "news/atelier",
    "news/awards",
    "news/photo-studio",
    "news/work-examples",
    "reviews",          # named portraits (Marina.jpg etc)
    "reviews/gallery",
]

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)


def upload_image(path, name):
    with open(path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    data = urllib.parse.urlencode({
        "key": API_KEY,
        "image": image_b64,
        "name": name,
    }).encode("utf-8")

    req = urllib.request.Request(UPLOAD_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    if not result.get("success"):
        raise ValueError(f"ImgBB error: {result}")

    d = result["data"]
    return {
        "thumb": d["thumb"]["url"],
        "medium": d.get("medium", {}).get("url") or d["display_url"],
        "full": d["url"],
        "width": int(d.get("width", 0)),
        "height": int(d.get("height", 0)),
    }


def main():
    progress = load_progress()

    for gallery in GALLERIES:
        folder = os.path.join("images", gallery)
        if not os.path.isdir(folder):
            print(f"  Skipping missing folder: {folder}")
            continue

        files = sorted(
            f for f in os.listdir(folder)
            if os.path.splitext(f)[1].lower() in IMAGE_EXTS
        )

        print(f"\n[{gallery}] {len(files)} images")

        for filename in files:
            key = f"{gallery}/{filename}"
            if key in progress:
                print(f"  SKIP {key}")
                continue

            filepath = os.path.join(folder, filename)
            name = os.path.splitext(filename)[0]

            for attempt in range(3):
                try:
                    result = upload_image(filepath, name)
                    progress[key] = result
                    save_progress(progress)
                    size_kb = os.path.getsize(filepath) // 1024
                    print(f"  OK   {key} ({size_kb} KB) → {result['full']}")
                    break
                except Exception as e:
                    wait = (attempt + 1) * 5
                    print(f"  ERR  {key} attempt {attempt+1}: {e}")
                    if attempt < 2:
                        print(f"       retrying in {wait}s...")
                        time.sleep(wait)
                    else:
                        print(f"  FAIL {key} — giving up")

            # Stay within API rate limits
            time.sleep(0.5)

    uploaded = len(progress)
    print(f"\nDone. {uploaded} images in {PROGRESS_FILE}")


if __name__ == "__main__":
    main()
