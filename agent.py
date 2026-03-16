import instructor
from openai import OpenAI
from database import query_events

client = instructor.patch(OpenAI(api_key="YOUR_API_KEY"))

def get_vegas_recommendation(user_request: str):
    # 1. Semantic Search: Find events related to the request
    # This costs $0!
    raw_results = query_events(user_request, n_results=3)
    
    # 2. Augmentation: Prepare the data for the LLM
    context = "\n".join([f"- {r['name']} at {r['start_time']} (Price: {r['price']})" for r in raw_results])
    
    # 3. Generation: The LLM acts as the Concierge
    # Using gpt-4o-mini keeps your $100 budget intact for months.
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful Las Vegas local. Use the provided event list to answer the user."},
            {"role": "user", "content": f"User Request: {user_request}\n\nAvailable Events:\n{context}"}
        ]
    )
    
    return response.choices[0].message.content

# Test it!
print(get_vegas_recommendation("I'm looking for something free to do this weekend."))