import os
from dotenv import load_dotenv
from scout import get_meetup_events
from database import save_events_to_db, cleanup_old_events, wipe_database
from schema import MeetupEnricher, process_meetup_event

load_dotenv()

def run_full_sync(wipe_first: bool = False):
    if wipe_first:
        print("🗑️ Wiping database...")
        wipe_database()

    print("🧹 Cleaning up expired events...")
    cleanup_old_events()

    print("🕵️‍♂️ Scouting Meetup.com for new Vegas events...")
    raw_events = get_meetup_events(target_count=5)

    if not raw_events:
        print("⚠️ Sync failed: No events found.")
        return

    print(f"🔍 Enriching {len(raw_events)} events with Tavily + LLM...")
    enricher = MeetupEnricher(
        tavily_key=os.getenv("TAVILY_API_KEY"),
        openrouter_key=os.getenv("OPENAI_API_KEY")
    )

    enriched_events = []
    for i, raw in enumerate(raw_events):
        try:
            event = process_meetup_event(raw, enricher)
            enriched_events.append(event)
            print(f"  ✅ [{i+1}/{len(raw_events)}] {event.name}")
        except Exception as e:
            print(f"  ❌ [{i+1}/{len(raw_events)}] Failed: {raw['name']} - {e}")

    if enriched_events:
        print(f"📥 Saving {len(enriched_events)} events to ChromaDB...")
        save_events_to_db(enriched_events)
        print("✅ Sync Complete!")
    else:
        print("⚠️ Sync failed: No events were enriched.")
