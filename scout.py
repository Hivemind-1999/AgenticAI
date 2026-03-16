from playwright.sync_api import sync_playwright
from schema import VegasEvent
from datetime import datetime
import dateutil.parser

def get_meetup_events(target_count=50):
    url = "https://www.meetup.com/find/?eventType=inPerson&sortField=DATETIME&location=us--nv--Las+Vegas&source=EVENTS"
    event_list = []
    seen_names = set()
    now = datetime.now().astimezone()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Set to False if you want to watch
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        page.goto(url, wait_until="networkidle")
        
        # Quick check for the empty-results trap
        page.wait_for_timeout(2000)
        if page.get_by_role("heading", name="Become an organizer").is_visible():
            page.get_by_role("button", name="Or reset filters").click()
            page.wait_for_timeout(2000)

        attempts = 0
        while len(event_list) < target_count and attempts < 10:
            # Incremental scroll to trigger lazy loading
            for _ in range(4):
                page.mouse.wheel(0, 800)
                page.wait_for_timeout(400)
            page.wait_for_timeout(1500)

            # Targeted extraction using the structure identified in your snippet
            cards = page.locator('a:has(h3):has(time)').all()

            for locator in cards:
                try:
                    name = locator.locator('h3').first.inner_text().strip()
                    if not name or name in seen_names or len(event_list) >= target_count:
                        continue

                    # Extract Time
                    raw_ts = locator.locator('time').first.get_attribute('datetime')
                    if not raw_ts: continue
                    
                    start_dt = dateutil.parser.parse(raw_ts.split('[')[0])
                    if start_dt.tzinfo is None:
                        start_dt = start_dt.replace(tzinfo=now.tzinfo)

                    if start_dt < now:
                        continue
                    
                    # --- PRICE EXTRACTION ---
                    # Look for the badge/span containing a '$' sign
                    price_text = "Free"
                    price_element = locator.get_by_text("$")
                    if price_element.count() > 0:
                        price_text = price_element.first.inner_text().strip()

                    link = locator.get_attribute('href') or ""
                    full_link = link if link.startswith('http') else f"https://www.meetup.com{link}"

                    event_list.append(VegasEvent(
                        name=name,
                        venue="Las Vegas",
                        start_time=start_dt.replace(tzinfo=None),
                        category="Meetup",
                        link=full_link,
                        price=price_text # New parameter
                    ))
                    seen_names.add(name)

                except Exception:
                    continue

            attempts += 1

        browser.close()
    
    return event_list

if __name__ == "__main__":
    from database import save_events_to_db # Import your new db functions
    
    results = get_meetup_events(50)
    if results:
        save_events_to_db(results)
        print("Scouted and Stored!")
        
    #results.sort(key=lambda x: x.start_time)
    
    #print(f"Total Events Found: {len(results)}")
    #for e in results:
    #    print(f"{e.start_time.strftime('%m/%d %I:%M %p')} | {e.price} | {e.name}")