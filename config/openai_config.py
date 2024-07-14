from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv("./cred.env")

client = AzureOpenAI(
   api_key=os.getenv("OPENAI_API_KEY"),
  #  azure_deployment=os.getenv("OPEN_AI_DEPLOYMENT_ID"),
   api_version="2024-02-01",
   azure_endpoint=os.getenv("OPEN_AI_ENDPOINT"),
)

def get_completion(query: str) -> str:
    response = client.chat.completions.create(
      model=os.getenv("OPEN_AI_DEPLOYMENT_ID"),
      messages=[
          {"role": "user", "content": query}
      ],
      max_tokens=1000
      # response_format={ "type": "json_object" }
    )

    return response.choices[0].message.content


def generate_image(heading: str)->str:
  
  PROMPT = f"""
  Ganerate an image for below article
  article heading:  {heading}
  """

  response = client.images.generate(
    model="dalle3",
    prompt=PROMPT,
    size="1024x1024",
    quality="standard",
    response_format='b64_json',
    n=1,
  )

  Image_base64 = response.data[0].b64_json
  return Image_base64