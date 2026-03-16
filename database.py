from datetime import datetime

import chromadb
from chromadb.utils import embedding_functions
from schema import VegasEvent
from typing import List

# 1. Initialize the Client (Creates a 'vegas_storage' folder in your project)
client = chromadb.PersistentClient(path="./vegas_storage")

# 2. Choose a free embedding model (Runs locally on your CPU)
default_ef = embedding_functions.DefaultEmbeddingFunction()

# 3. Get or Create a 'Collection' (Think of this as a Table in a database)
collection = client.get_or_create_collection(
    name="vegas_events", 
    embedding_function=default_ef
)

def save_events_to_db(events: List[VegasEvent]):
    for event in events:
        # We turn the event details into a single string for the AI to "read"
        content_string = f"{event.name} at {event.venue}. Category: {event.category}. Price: {event.price}."
        
        collection.add(
            ids=[event.link], # Use the link as a unique ID
            documents=[content_string],
            metadatas=[{
                "name": event.name,
                "price": event.price,
                "start_time": event.start_time.isoformat(),
                "link": event.link
            }]
        )
    print(f"Successfully indexed {len(events)} events to ChromaDB.")

def query_events(user_query: str, n_results: int = 3):
    # This is how the AI 'finds' things
    results = collection.query(
        query_texts=[user_query],
        n_results=n_results
    )
    return results['metadatas']

def cleanup_old_events():
    now_iso = datetime.now().isoformat()
    # Delete everything where start_time is less than 'now'
    collection.delete(
        where={"start_time": {"$lt": now_iso}}
    )
    print("Cleaned up expired events from ChromaDB.")