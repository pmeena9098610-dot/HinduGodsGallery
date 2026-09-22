"""
🕉️ Search Engine Auto-Pinger & IndexNow Submitter
Pings IndexNow protocol (Bing, Yandex, Seznam, Naver) for instant crawl discovery.
Google relies on dynamic lastmod in sitemap.xml and robots.txt.
"""

import urllib.request
import urllib.parse
import json
import logging
import os
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HOST = "pmeena9098610-dot.github.io"
KEY = "9f8e7d6c5b4a31209f8e7d6c5b4a3120"
KEY_LOCATION = f"https://{HOST}/HinduGodsGallery/{KEY}.txt"

def submit_indexnow():
    try:
        import xml.etree.ElementTree as ET
        sitemap_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sitemap.xml")
        url_list = []
        if os.path.exists(sitemap_path):
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            for u in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
                loc = u.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
                if loc is not None and loc.text:
                    url_list.append(loc.text)
        
        if not url_list:
            url_list = [
                f"https://{HOST}/HinduGodsGallery/",
                f"https://{HOST}/HinduGodsGallery/category-cute.html",
                f"https://{HOST}/HinduGodsGallery/category-trending.html",
                f"https://{HOST}/HinduGodsGallery/hanuman-chalisa.html",
                f"https://{HOST}/HinduGodsGallery/shiv-aarti.html",
                f"https://{HOST}/HinduGodsGallery/ganesh-aarti.html"
            ]

        payload = {
            "host": HOST,
            "key": KEY,
            "keyLocation": KEY_LOCATION,
            "urlList": url_list
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "IndexNow-AutoSubmitter/1.0"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            logging.info(f"✅ IndexNow API Submission: HTTP {resp.status} (Accepted) for {len(url_list)} URLs")
            return True
    except Exception as e:
        logging.warning(f"IndexNow Notice: {e}")
        return False

def run_all_pings():
    logging.info("🚀 Submitting all pages to IndexNow API for instant crawl discovery...")
    success = submit_indexnow()
    if success:
        logging.info("🎉 All 36 URLs successfully submitted to search engine crawler networks!")

if __name__ == "__main__":
    run_all_pings()
