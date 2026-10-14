"""
🕉️ Google Search Console & Indexing API Manager for HinduGodsGallery
Automates sitemap submission and instant URL indexing via Google APIs.
"""

import os
import sys
import time
import json
import urllib.parse
import xml.etree.ElementTree as ET

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "replace")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "replace")

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-auth", "google-auth-httplib2", "requests"])
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request
    import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITEMAP_PATH = os.path.join(BASE_DIR, "sitemap.xml")
SITE_URL = "https://pmeena9098610-dot.github.io/HinduGodsGallery/"
SITEMAP_URL = f"{SITE_URL}sitemap.xml"
FEED_URL = f"{SITE_URL}feed.xml"

# Shared or local service account file
SERVICE_ACCOUNT_PATHS = [
    os.path.join(BASE_DIR, "service_account.json"),
    r"C:\Users\Bappa official\OneDrive\Desktop\image2pdfpro\service_account.json",
    r"C:\Users\Bappa official\Desktop\Imge2pdfpro\service_account.json"
]

def find_service_account():
    for p in SERVICE_ACCOUNT_PATHS:
        if os.path.exists(p):
            return p
    return None

def get_credentials(sa_path):
    SCOPES = [
        "https://www.googleapis.com/auth/webmasters",
        "https://www.googleapis.com/auth/indexing"
    ]
    creds = service_account.Credentials.from_service_account_file(sa_path, scopes=SCOPES)
    creds.refresh(Request())
    return creds

def check_permissions(creds):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.get(api_url, headers=headers)
    return resp.status_code == 200, resp.status_code, resp.text

def submit_sitemap_via_api(creds, sitemap_link):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    encoded_sitemap = urllib.parse.quote(sitemap_link, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_sitemap}"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.put(api_url, headers=headers)
    return resp.status_code == 204 or resp.status_code == 200, resp.status_code, resp.text

def submit_indexing_api(creds, url):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds.token}"
    }
    body = {"url": url, "type": "URL_UPDATED"}
    resp = requests.post(endpoint, headers=headers, json=body, timeout=20)
    return resp.status_code == 200, resp.status_code, resp.text

def main():
    print("=" * 65)
    print("🕉️ HinduGodsGallery - Google API Manager & Auto-Submitter")
    print("=" * 65)
    
    sa_path = find_service_account()
    if not sa_path:
        print("❌ service_account.json not found.")
        return
        
    print(f"🔑 Using Service Account from: {sa_path}")
    creds = get_credentials(sa_path)
    sa_email = creds.service_account_email
    print(f"📧 Service Account Email: {sa_email}")
    
    has_perm, status, text = check_permissions(creds)
    if not has_perm:
        print("\n" + "!" * 65)
        print("⚠️ PERMISSION NOTICE FOR GOOGLE SEARCH CONSOLE:")
        print(f"Status Code: {status}")
        print("To enable 100% full hands-free automation:")
        print(f"1. Open Google Search Console for {SITE_URL}")
        print("2. Go to: Settings (सेटिंग्स) -> Users and permissions (उपयोगकर्ता और अनुमतियां)")
        print("3. Click 'Add User' (उपयोगकर्ता जोड़ें)")
        print(f"4. Email: {sa_email}")
        print("5. Permission: Owner (मालिक)")
        print("Once added, this script can submit all sitemaps & URLs via API!")
        print("!" * 65 + "\n")
        return False
    
    print("\n✅ Permission Verified! Submitting Sitemaps via Search Console API...")
    ok1, code1, _ = submit_sitemap_via_api(creds, SITEMAP_URL)
    print(f"  - sitemap.xml: {'✅ Success' if ok1 else f'❌ Error {code1}'}")
    
    ok2, code2, _ = submit_sitemap_via_api(creds, FEED_URL)
    print(f"  - feed.xml: {'✅ Success' if ok2 else f'❌ Error {code2}'}")
    
    # Submitting URLs via Indexing API
    if os.path.exists(SITEMAP_PATH):
        tree = ET.parse(SITEMAP_PATH)
        urls = [loc.text.strip() for loc in tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if loc is not None]
        print(f"\n🚀 Submitting {min(len(urls), 200)} URLs to Google Indexing API...")
        success = 0
        for i, u in enumerate(urls[:200], 1):
            if creds.expired:
                creds.refresh(Request())
            ok, sc, _ = submit_indexing_api(creds, u)
            if ok:
                success += 1
                if i % 25 == 0 or i == len(urls):
                    print(f"  [{i}/{len(urls)}] Progress: {success} URLs submitted OK")
            time.sleep(0.1)
        print(f"\n🎉 Done! {success} URLs submitted to Google for instant crawling.")
    return True

if __name__ == "__main__":
    main()
