from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY", "").strip()

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
                messages=[{"role": "user", "content": "which model of chatgpt am i using?"}],
                model="gpt-4o-mini",
            )

print(api_key)

print(response)