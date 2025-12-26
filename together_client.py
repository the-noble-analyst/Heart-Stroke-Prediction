import os
from together import Together

def get_together_client():
    api_key = os.getenv("TOGETHER_API_KEY")
    return Together(api_key=api_key)
