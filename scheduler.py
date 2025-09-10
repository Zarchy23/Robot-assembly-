from apscheduler.schedulers.background import BackgroundScheduler
from scraper_worker import extract_ads_from_page
import requests, time
from datetime import datetime

TARGETS = [
    {"advertiser_id":1, "tracked_site_id":1, "url":"https://example.com/ads", "selector": None},
]

API_INGEST = "http://localhost:5000/ads"

def job():
    print("Running scrape job:", datetime.utcnow())
    for t in TARGETS:
        try:
            ads = extract_ads_from_page(t["url"], t.get("selector"))
            for a in ads:
                payload = {
                    "advertiser_id": t["advertiser_id"],
                    "tracked_site_id": t["tracked_site_id"],
                    "ad_hash": a["ad_hash"],
                    "title": a["title"],
                    "body": a["body"],
                    "landing_url": a["landing_url"],
                    "creative_path": a["creative_path"]
                }
                r = requests.post(API_INGEST, json=payload, timeout=10)
                print("ingest status", r.status_code)
        except Exception as e:
            print("target error", t["url"], e)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', minutes=60)
    scheduler.start()
    print("Scheduler started")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        scheduler.shutdown()