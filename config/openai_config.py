import openai
import os
from dotenv import load_dotenv

load_dotenv("./cred.env")

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.azure_endpoint = os.getenv("OPEN_AI_ENDPOINT")

openai.api_type = "azure"
openai.api_version = "2024-02-01"

def get_completion(query):
    response = openai.chat.completions.create(
        model=os.getenv("OPEN_AI_DEPLOYMENT_ID"),
        messages=[
            {"role": "user", "content": query}
        ],
    )
    return response.choices[0].message.content  

def generate_image(heading: str)->str:
  
  PROMPT = f"""
  Ganerate an image for below article
  article heading:  {heading}
  """

  response = openai.images.generate(
    model="dalle3",
    prompt=PROMPT,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  return image_url