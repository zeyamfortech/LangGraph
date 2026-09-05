import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

print("ENDPOINT :", os.getenv("LANGSMITH_ENDPOINT"))
print("API KEY  :", os.getenv("LANGSMITH_API_KEY"))
print("PROJECT  :", os.getenv("LANGSMITH_PROJECT"))
print("TRACING  :", os.getenv("LANGSMITH_TRACING"))