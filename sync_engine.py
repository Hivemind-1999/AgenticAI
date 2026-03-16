from scout import get_meetup_events
from database import save_events_to_db, cleanup_old_events

def run_full_sync():
    print("🧹 Cleaning up expired events...")
    cleanup_old_events()

    print("🕵️‍♂️ Scouting Meetup.com for new Vegas events...")
    # Fetch 50 fresh events
    new_events = get_meetup_events(target_count=50)

    if new_events:
        print(f"📥 Saving {len(new_events)} events to ChromaDB...")
        save_events_to_db(new_events)
        print("✅ Sync Complete!")
    else:
        print("⚠️ Sync failed: No events found.")