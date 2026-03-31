import instructor
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Create client with same configuration as agent.py
client = instructor.patch(OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
))

def test_api_connection():
    """Test the API connection with a simple message"""
    try:
        print("Testing API connection to OpenRouter...")
        print(f"Using model: google/gemma-3-4b-it:free")
        
        response = client.chat.completions.create(
            model="google/gemma-3-4b-it:free",
            messages=[
                {"role": "user", "content": "Hello! Can you respond with a short greeting to confirm you're working?"}
            ]
        )
        
        print("\n✅ API Connection Successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"\n❌ API Connection Failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_connection()