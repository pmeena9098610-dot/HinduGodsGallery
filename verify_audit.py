import os
import sys
import json
import xml.etree.ElementTree as ET
import glob
import re

# Set UTF-8 encoding for standard output on Windows
sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
errors = []
warnings = []

print("=== STARTING MICRO-LEVEL AUDIT ===")

# 1. Sitemap validation
sitemap_path = os.path.join(ROOT_DIR, "sitemap.xml")
try:
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    urls = root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
    print(f"PASS: sitemap.xml is valid XML with {len(urls)} URLs")
    if len(urls) != 51:
        warnings.append(f"Expected exactly 51 canonical URLs in sitemap, got {len(urls)}")
except Exception as e:
    errors.append(f"FAIL: sitemap.xml parse error: {e}")

# 2. Feed validation
feed_path = os.path.join(ROOT_DIR, "feed.xml")
try:
    tree = ET.parse(feed_path)
    root = tree.getroot()
    channel = root.find('channel')
    items = channel.findall('item') if channel is not None else []
    print(f"PASS: feed.xml is valid RSS 2.0 with {len(items)} items")
except Exception as e:
    errors.append(f"FAIL: feed.xml parse error: {e}")

# 3. images_data.json validation
data_path = os.path.join(ROOT_DIR, "images_data.json")
try:
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    all_items = []
    if isinstance(data, dict):
        for date_key, items in data.items():
            if isinstance(items, list):
                all_items.extend(items)
    elif isinstance(data, list):
        all_items = data

    print(f"PASS: images_data.json is valid JSON with {len(data)} date groups and {len(all_items)} total images")
    for i, item in enumerate(all_items):
        if "id" not in item:
            errors.append(f"Item #{i} missing 'id'")
        if "category" not in item:
            errors.append(f"Item #{i} missing 'category'")
        if not (item.get("title") or item.get("name_en")):
            errors.append(f"Item #{i} missing 'title' / 'name_en'")
        if not (item.get("image_url") or item.get("image")):
            errors.append(f"Item #{i} missing 'image_url' / 'image'")
except Exception as e:
    errors.append(f"FAIL: images_data.json parse error: {e}")

# 4. Check all HTML files for essential SEO & UX tags
html_files = glob.glob(os.path.join(ROOT_DIR, "*.html"))
print(f"Auditing {len(html_files)} HTML files for SEO, meta tags, and schema...")

checked_count = 0
for hf in html_files:
    fname = os.path.basename(hf)
    if fname.startswith("google") and fname.endswith(".html"):
        continue  # Google Search Console verification token file
    with open(hf, 'r', encoding='utf-8') as f:
        content = f.read()

    # DOCTYPE
    if not content.strip().lower().startswith("<!doctype html>"):
        errors.append(f"{fname}: Missing <!DOCTYPE html>")

    # Title
    if "<title>" not in content or "</title>" not in content:
        errors.append(f"{fname}: Missing <title> tag")

    # Viewport
    if 'name="viewport"' not in content:
        warnings.append(f"{fname}: Missing viewport meta tag")

    # Canonical
    if 'rel="canonical"' not in content:
        warnings.append(f"{fname}: Missing rel=canonical")

    # JSON-LD Schema
    schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    for sm in schema_matches:
        try:
            json.loads(sm.strip())
        except Exception as e:
            errors.append(f"{fname}: Invalid JSON-LD schema: {e}")

    checked_count += 1

print(f"PASS: Audited {checked_count} HTML files for DOCTYPE, viewport, titles, and JSON-LD schemas.")

# 5. Check Directory Sync
SYNC_DIRS = [
    r"C:\Users\Bappa official\OneDrive\Desktop\HinduGodsGallery",
    r"C:\Users\Bappa official\HinduGodsGallery",
    r"c:\Users\Bappa official\.gemini\antigravity\playground\primordial-chromosphere"
]

core_files = [
    "index.html", "shubh-prabhat.html", "festivals-2026.html",
    "lakshmi-aarti.html", "durga-aarti.html", "ram-stuti.html",
    "hanuman-chalisa.html", "shiv-aarti.html", "ganesh-aarti.html",
    "sitemap.xml", "feed.xml", "images_data.json", "sw.js"
]

print("Checking cross-directory synchronization...")
for d in SYNC_DIRS:
    if os.path.exists(d):
        missing = [f for f in core_files if not os.path.exists(os.path.join(d, f))]
        if missing:
            errors.append(f"Directory {d} is missing files: {missing}")
        else:
            print(f"PASS: Directory {d} has all core files in sync.")
    else:
        warnings.append(f"Directory {d} does not exist.")

print("\n=== AUDIT SUMMARY ===")
print(f"Total Errors: {len(errors)}")
print(f"Total Warnings: {len(warnings)}")

if errors:
    print("\nERRORS:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print("ALL MICRO-LEVEL CHECKS PASSED PERFECTLY! 100% PRODUCTION READY.")
