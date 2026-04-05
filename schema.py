import os
import json
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from tavily import TavilyClient
from openai import OpenAI, RateLimitError
from typing import Dict, Any, Tuple

# 1. Your Event Struct
class VegasEvent(BaseModel):
    name: str
    location: str
    start_time: datetime
    category: str
    description: str
    price: str = "Free"
    attendees: Optional[int]
    link: Optional[str] = None

# 2. The Enrichment Tool
class MeetupEnricher:
    def __init__(self, tavily_key: str, openrouter_key: str):
        self.tavily = TavilyClient(api_key=tavily_key)
        self.ai_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
        )

    def _make_ai_request(self, model: str, messages: list, task_type: str) -> Dict[str, Any]:
        """Unified AI request function with detailed error handling"""
        try:
            response = self.ai_client.chat.completions.create(
                model=model,
                messages=messages
            )
            return {
                "success": True,
                "data": response.choices[0].message.content,
                "model": model,
                "task_type": task_type
            }
        except RateLimitError as e:
            return {
                "success": False,
                "error": f"Rate limit exceeded for model {model}",
                "exception": str(e),
                "model": model,
                "task_type": task_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error occurred for model {model}",
                "exception": str(e),
                "model": model,
                "task_type": task_type
            }

def get_event_details(self, url: str):
        print(f"  🔗 Extracting from: {url}")
        extraction = self.tavily.extract(urls=[url])
        results = extraction.get('results', [])
        print(f"  📄 Tavily results count: {len(results)}")

        if not results or not results[0].get('raw_content'):
            print("  ⚠️ No content extracted from URL")
            return "General", "No description available."

        raw_text = results[0]['raw_content'][:4000]

        messages = [
            {
                "role": "user",
                "content": "You are a helpful assistant that summarizes events. "
                           "Return a JSON object with 'category' (a short phrase) "
                           "and 'description' (exactly 2 sentences)."
            },
            {
                "role": "user",
                "content": f"Summarize this event content: {raw_text}"
            }
        ]

        result = self._make_ai_request(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=messages,
            task_type="event_enrichment"
        )

        if result["success"]:
            try:
                res_data = json.loads(result["data"])
                return res_data.get("category", "General"), res_data.get("description", "No description available.")
            except json.JSONDecodeError:
                return "General", "Invalid response format"
        else:
            print(f"  ❌ {result['error']} (Model: {result['model']})")
            return "General", "Details unavailable"

# 3. Execution Logic
def process_meetup_event(scraped_data: dict, enricher: MeetupEnricher):
    # Call our tool
    category, description = enricher.get_event_details(scraped_data['link'])
    
    # Create the Pydantic instance
    return VegasEvent(
        name=scraped_data['name'],
        location=scraped_data['location'],
        start_time=scraped_data['start_time'],
        attendees=scraped_data['attendees'],
        link=scraped_data['link'],
        price=scraped_data.get('price', 'Free'),
        category=category,
        description=description
    )

# Example Usage:
# enricher = MeetupEnricher(tavily_key="tvly-xxx", openrouter_key="sk-or-xxx")
# event = process_meetup_event(my_scraped_dict, enricher)