from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY", "").strip()

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
                messages=[{"role": "user", "content": "Hello"}],
                model="gpt-3.5-turbo",
            )

print(api_key)

print(response)