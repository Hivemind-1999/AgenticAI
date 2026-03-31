import instructor
import os
from dotenv import load_dotenv
from openai import OpenAI
from database import query_events

load_dotenv()

client = instructor.patch(OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
))

def get_vegas_recommendation(user_request: str):
    # 1. Semantic Search: Find events related to the request
    # This costs $0!
    raw_results = query_events(user_request, n_results=3)
    
    # 2. Augmentation: Prepare the data for the LLM
    context = "\n".join([f"- {r['name']} at {r['start_time']} (Price: {r['price']})" for r in raw_results])
    
    # 3. Generation: The LLM acts as the Concierge
    # Using gpt-4o-mini keeps your $100 budget intact for months.
    response = client.chat.completions.create(
        model="google/gemma-3-4b-it:free",
        messages=[
            {"role": "user", "content": f"You are a helpful Las Vegas local. Use the provided event list to answer the user.\n\nUser Request: {user_request}\n\nAvailable Events:\n{context}"}
        ]
    )
    
    return response.choices[0].message.content

# Test it!
print(get_vegas_recommendation("I'm looking for something free to do this weekend."))