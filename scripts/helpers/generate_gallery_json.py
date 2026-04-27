"""
Generate per-page JSON files from the ImgBB upload registry.
Run from the project root: python3 scripts/helpers/generate_gallery_json.py

Preserves the exact image order from each HTML file, including
which images were commented out in news.html.
"""

import json
import os

with open("data/imgbb-uploads.json") as f:
    UPLOADS = json.load(f)


def img(key):
    """Return the ImgBB entry for images/<key>, or raise if missing."""
    if key not in UPLOADS:
        raise KeyError(f"No upload found for: {key}")
    d = UPLOADS[key]
    return {"thumb": d["thumb"], "medium": d["medium"], "full": d["full"]}


# ── gallery.html ─────────────────────────────────────────────────────────────
# Order is taken directly from gallery.html, not alphabetical
gallery_order = [1, 2, 3, 21, 22, 23, 24, 20, 25, 7, 8, 5, 10, 11, 12, 13, 14, 9,
                 15, 16, 17, 18, 19, 6, 4]

gallery_json = [img(f"gallery/{n}.jpg") for n in gallery_order]

with open("data/gallery-images.json", "w") as f:
    json.dump(gallery_json, f, separators=(",", ":"))
print(f"gallery-images.json: {len(gallery_json)} images")


# ── news.html ─────────────────────────────────────────────────────────────────
# Groups and per-group order from news.html (commented-out images excluded)
news_groups = [
    {
        "title": "Unser Modeatelier",
        "images": [
            img("news/atelier/1.jpg"),
            img("news/atelier/3.jpg"),
            img("news/atelier/4.jpg"),
            img("news/atelier/5.jpg"),
            img("news/atelier/6.jpg"),
            img("news/atelier/7.jpg"),
            img("news/atelier/9.jpg"),
            img("news/atelier/8.jpg"),
            img("news/atelier/10.jpg"),
        ],
    },
    {
        "title": "Auszeichnungen und Zertifikate",
        "images": [
            img("news/awards/1.jpg"),
            img("news/awards/2.jpg"),
            img("news/awards/4.jpg"),
            img("news/awards/6.jpg"),
            img("news/awards/7.jpg"),
            img("news/awards/8.jpg"),
        ],
    },
    {
        "title": "Neue Dienstleistung im Modeatelier",
        "images": [
            img("news/photo-studio/1.jpg"),
            img("news/photo-studio/2.jpg"),
            img("news/photo-studio/4.jpg"),
            img("news/photo-studio/5.jpg"),
            img("news/photo-studio/6.jpg"),
            img("news/photo-studio/7.jpg"),
            img("news/photo-studio/8.jpg"),
            img("news/photo-studio/9.jpg"),
            img("news/photo-studio/10.jpg"),
            img("news/photo-studio/11.jpg"),
            img("news/photo-studio/12.jpg"),
            img("news/photo-studio/13.jpg"),
            img("news/photo-studio/14.jpg"),
            img("news/photo-studio/15.jpg"),
            img("news/photo-studio/16.jpg"),
            img("news/photo-studio/17.jpg"),
            img("news/photo-studio/18.jpg"),
        ],
    },
    {
        "title": "Neueste Anfertigungen nach Maß",
        "images": [
            # 2 and 11 and 16 were commented out in original HTML
            img("news/work-examples/1.jpg"),
            img("news/work-examples/3.jpg"),
            img("news/work-examples/4.jpg"),
            img("news/work-examples/5.jpg"),
            img("news/work-examples/6.jpg"),
            img("news/work-examples/7.jpg"),
            img("news/work-examples/8.jpg"),
            img("news/work-examples/9.jpg"),
            img("news/work-examples/10.jpg"),
            img("news/work-examples/12.jpg"),
            img("news/work-examples/13.jpg"),
            img("news/work-examples/14.jpg"),
            img("news/work-examples/15.jpg"),
            img("news/work-examples/17.jpg"),
            img("news/work-examples/18.jpg"),
            img("news/work-examples/19.jpg"),
            img("news/work-examples/20.jpg"),
            img("news/work-examples/21.jpg"),
            img("news/work-examples/22.jpg"),
            img("news/work-examples/23.jpg"),
            img("news/work-examples/24.jpg"),
            img("news/work-examples/25.jpg"),
        ],
    },
]

with open("data/news-images.json", "w") as f:
    json.dump(news_groups, f, separators=(",", ":"))
total_news = sum(len(g["images"]) for g in news_groups)
print(f"news-images.json: {total_news} images across {len(news_groups)} groups")


# ── reviews.html ──────────────────────────────────────────────────────────────
# Named portraits first, then gallery/1..31
reviews_json = [
    img("reviews/Marina.jpg"),
    img("reviews/Libya.jpg"),
    img("reviews/Natalia.jpg"),
    img("reviews/Galina.jpg"),
    img("reviews/Luda.jpg"),
] + [img(f"reviews/gallery/{n}.jpg") for n in range(1, 32)]

with open("data/reviews-images.json", "w") as f:
    json.dump(reviews_json, f, separators=(",", ":"))
print(f"reviews-images.json: {len(reviews_json)} images")
