from google import genai
from django.conf import settings

client = genai.client(api_key=settings.GEMINI_API_KEY)
model = settings.MODEL_NAME




# COMONENT : 1 --> Sage job description



# COMPONENT : 2 -> support tools --> tool schemas  , that AI agents will read to execute best suitable func. from tools.py



# COMPONENT : 3 -> execute_tool() --> bridge b/w py funcns (or tools)



# COMONENT : 4 -> agent loop --> while loop that loops untill the task is done





