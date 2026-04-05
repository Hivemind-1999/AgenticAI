from datetime import datetime

import chromadb
from chromadb.utils import embedding_functions
from schema import VegasEvent
from typing import List

# 1. Initialize the Client (Creates a 'vegas_storage' folder in your project)
client = chromadb.PersistentClient(path="./vegas_storage")

# 2. Choose a free embedding model (Runs locally on your CPU)
default_ef = embedding_functions.DefaultEmbeddingFunction()

COLLECTION_NAME = "vegas_events"

def get_collection():
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=default_ef
    )

def save_events_to_db(events: List[VegasEvent]):
    collection = get_collection()
    for event in events:
        content_string = f"{event.name} at {event.location}. Category: {event.category}. {event.description} Price: {event.price}."
        
        collection.add(
            ids=[event.link],
            documents=[content_string],
            metadatas=[{
                "name": event.name,
                "location": event.location,
                "category": event.category,
                "description": event.description,
                "price": event.price,
                "start_time": event.start_time.isoformat(),
                "start_timestamp": event.start_time.timestamp(),
                "link": event.link,
                "attendees": event.attendees or 0
            }]
        )
    print(f"Successfully indexed {len(events)} events to ChromaDB.")

def query_events(user_query: str, n_results: int = 3):
    collection = get_collection()
    results = collection.query(
        query_texts=[user_query],
        n_results=n_results
    )
    return results['metadatas'][0]

def cleanup_old_events():
    collection = get_collection()
    now_timestamp = datetime.now().timestamp()
    collection.delete(
        where={"start_timestamp": {"$lt": now_timestamp}}
    )
    print("Cleaned up expired events from ChromaDB.")

def wipe_database():
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    get_collection()
    print("Database wiped successfully.")

def get_all_events():
    collection = get_collection()
    results = collection.get()
    events = []
    for i, metadata in enumerate(results['metadatas']):
        events.append({
            "id": results['ids'][i],
            "metadata": metadata
        })
    return events

def print_all_events():
    events = get_all_events()
    if not events:
        print("No events in database.")
        return
    
    print(f"\n📋 Total events in database: {len(events)}\n")
    for i, event in enumerate(events, 1):
        meta = event['metadata']
        print(f"{i}. {meta.get('name', 'N/A')}")
        print(f"   📍 Location: {meta.get('location', 'N/A')}")
        print(f"   📅 Start: {meta.get('start_time', 'N/A')}")
        print(f"   💰 Price: {meta.get('price', 'N/A')}")
        print(f"   👥 Attendees: {meta.get('attendees', 'N/A')}")
        print(f"   🏷️ Category: {meta.get('category', 'N/A')}")
        print(f"   📝 Description: {meta.get('description', 'N/A')}")
        print(f"   🔗 Link: {meta.get('link', 'N/A')}")
        print()
