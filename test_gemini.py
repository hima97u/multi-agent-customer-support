from google import genai
from decouple import config

client = genai.Client(api_key=config("GEMINI_API_KEY"))

response = client.models.generate_content(
    model= config("MODEL_NAME"),
    contents="write longest increasing subsequence cpp code",
)

print(response.text)