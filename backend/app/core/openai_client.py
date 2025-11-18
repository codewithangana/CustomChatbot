from openai import OpenAI
from app.core.config import settings  

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)  


def generate_answer(prompt: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message["content"]

