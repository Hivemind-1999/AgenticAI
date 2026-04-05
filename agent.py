import instructor
import os
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError
from database import query_events
from typing import Dict, Any

load_dotenv()

class AIRequestor:
    def __init__(self, api_key: str):
        self.client = instructor.patch(OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        ))

    def make_request(self, model: str, messages: list, task_type: str) -> Dict[str, Any]:
        """Unified AI request function with detailed error handling"""
        try:
            response = self.client.chat.completions.create(
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

load_dotenv()

ai_requestor = AIRequestor(api_key=os.getenv("OPENAI_API_KEY"))

def get_vegas_recommendation(user_request: str):
    raw_results = query_events(user_request, n_results=3)

    context = "\n".join([
        f"- {r['name']} at {r.get('location', 'Las Vegas')} | {r['start_time']} | {r['price']}\n  {r.get('description', '')}"
        for r in raw_results
    ])

    messages = [
        {"role": "user", "content": f"You are a helpful Las Vegas local. Use the provided event list to answer the user.\n\nUser Request: {user_request}\n\nAvailable Events:\n{context}"}
    ]

    result = ai_requestor.make_request(
        model="google/gemma-3-4b-it:free",
        messages=messages,
        task_type="recommendation"
    )

    if result["success"]:
        return result["data"]
    else:
        return f"⚠️ {result['error']} (Model: {result['model']})"

if __name__ == "__main__":
    print(get_vegas_recommendation("I'm looking for something free to do this weekend."))
