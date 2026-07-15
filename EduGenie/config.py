import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the variables from your .env file into the system memory
load_dotenv()

# 2. Grab the API key from memory using the variable name you assigned in your .env file
API_KEY = os.environ.get("GEMINI_API_KEY")

# 3. Pass that key to the Google library config
genai.configure(api_key=API_KEY)