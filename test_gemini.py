from google import genai
from decouple import config

client = genai.Client(api_key=config("GEMINI_API_KEY"))

response = client.models.generate_content(
    model= config("MODEL_NAME"),
    contents="Hii what is 50 * 2"
)

print(response.text)