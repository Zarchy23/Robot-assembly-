import os, uuid
from playwright.sync_api import sync_playwright
from config import STORAGE_DIR
import hashlib

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def extract_ads_from_page(url, css_selector=None):
    results = []
    os.makedirs(STORAGE_DIR, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=30000)
        page.wait_for_timeout(2000)
        if css_selector:
            ad_elements = page.query_selector_all(css_selector)
        else:
            ad_elements = page.query_selector_all("div[class*=ad], article[class*=ad]")
        for el in ad_elements:
            try:
                title = el.query_selector("h1,h2,h3") and el.query_selector("h1,h2,h3").inner_text() or ""
                body = el.inner_text()
                link_el = el.query_selector("a")
                landing = link_el.get_attribute("href") if link_el else None
                filename = f"{uuid.uuid4().hex}.png"
                el.screenshot(path=os.path.join(STORAGE_DIR, filename))
                ad_hash = sha256_hex((title or "") + (body or "") + (landing or ""))
                results.append({
                    "title": title,
                    "body": body[:500],
                    "landing_url": landing,
                    "creative_path": os.path.join(STORAGE_DIR, filename),
                    "ad_hash": ad_hash
                })
            except Exception as e:
                print("element error:", e)
        browser.close()
    return results