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
SITEMAP_INDEX_URL = f"{SITE_URL}sitemap_index.xml"
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

def list_sitemaps(creds):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.get(api_url, headers=headers)
    if resp.status_code == 200:
        return resp.json().get("sitemap", [])
    return []

def delete_sitemap_via_api(creds, sitemap_link):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    encoded_sitemap = urllib.parse.quote(sitemap_link, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_sitemap}"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.delete(api_url, headers=headers)
    return resp.status_code in [200, 204], resp.status_code, resp.text

def submit_sitemap_via_api(creds, sitemap_link):
    encoded_site = urllib.parse.quote(SITE_URL, safe="")
    encoded_sitemap = urllib.parse.quote(sitemap_link, safe="")
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/sitemaps/{encoded_sitemap}"
    headers = {"Authorization": f"Bearer {creds.token}"}
    resp = requests.put(api_url, headers=headers)
    return resp.status_code in [200, 204], resp.status_code, resp.text

def submit_indexing_api(creds, url, retries=2):
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {creds.token}"
    }
    body = {"url": url, "type": "URL_UPDATED"}
    for attempt in range(retries):
        try:
            resp = requests.post(endpoint, headers=headers, json=body, timeout=15)
            return resp.status_code == 200, resp.status_code, resp.text
        except Exception as e:
            if attempt == retries - 1:
                return False, 0, str(e)
            time.sleep(1.0)
    return False, 0, "Max retries exceeded"

def main():
    print("=" * 65)
    print("🕉️ HinduGodsGallery - Google API Manager & Auto-Submitter")
    print("=" * 65)
    
    sa_path = find_service_account()
    if not sa_path:
        print("❌ service_account.json not found.")
        return False
        
    print(f"🔑 Using Service Account from: {sa_path}")
    creds = get_credentials(sa_path)
    sa_email = creds.service_account_email
    print(f"📧 Service Account Email: {sa_email}")
    
    has_perm, status, text = check_permissions(creds)
    if not has_perm:
        print(f"\n⚠️ Permission Check Failed: HTTP {status}")
        return False
    
    print("\n✅ Permission Verified! Checking Search Console Sitemaps...")
    current_sitemaps = list_sitemaps(creds)
    for sm in current_sitemaps:
        path = sm.get("path", "")
        # Remove feed.xml if present in sitemaps (feed.xml is RSS feed, causes Unknown type in GSC)
        if "feed.xml" in path:
            print(f"  🗑️ Removing non-sitemap feed '{path}'...")
            del_ok, del_sc, _ = delete_sitemap_via_api(creds, path)
            print(f"     Deleted: {'✅ Success' if del_ok else f'❌ Error {del_sc}'}")

    print("\n📤 Submitting Clean Sitemaps via Search Console API...")
    ok_idx, code_idx, _ = submit_sitemap_via_api(creds, SITEMAP_INDEX_URL)
    print(f"  - sitemap_index.xml: {'✅ Success (HTTP 204/200)' if ok_idx else f'❌ Error {code_idx}'}")
    
    ok1, code1, _ = submit_sitemap_via_api(creds, SITEMAP_URL)
    print(f"  - sitemap.xml: {'✅ Success (HTTP 204/200)' if ok1 else f'❌ Error {code1}'}")
    
    # Submitting URLs via Indexing API
    if os.path.exists(SITEMAP_PATH):
        tree = ET.parse(SITEMAP_PATH)
        urls = [loc.text.strip() for loc in tree.getroot().findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc") if loc is not None]
        print(f"\n🚀 Submitting URLs to Google Indexing API (Daily Quota: 200)...")
        success = 0
        quota_exceeded = False
        for i, u in enumerate(urls, 1):
            try:
                if creds.expired:
                    creds.refresh(Request())
                ok, sc, msg = submit_indexing_api(creds, u)
                if ok:
                    success += 1
                elif sc == 429:
                    print(f"  ℹ️ Google Indexing API Daily Quota reached (200 requests/day). All URLs already queued for today!")
                    quota_exceeded = True
                    break
                else:
                    print(f"  [{i}/{len(urls)}] Notice: HTTP {sc} for {u}")
                if i % 25 == 0:
                    print(f"  [{i}/{len(urls)}] Progress: {success} OK")
                time.sleep(0.2)
            except Exception as e:
                print(f"  [{i}/{len(urls)}] Exception: {e}")
                break
        if not quota_exceeded:
            print(f"\n🎉 Done! {success} URLs submitted successfully to Google.")
    return True

if __name__ == "__main__":
    main()
