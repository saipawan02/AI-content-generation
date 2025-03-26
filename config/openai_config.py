import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv("./cred.env")

client_4 = AzureOpenAI(
   api_key=os.getenv("OPENAI_API_KEY_4"),
   api_version="2024-02-01",
   azure_endpoint=os.getenv("OPEN_AI_ENDPOINT_4"),
)


def get_completion(query: str) -> str:
    response = client_4.chat.completions.create(
      model=os.getenv("OPEN_AI_DEPLOYMENT_ID_4"),
      messages=[
          {"role": "user", "content": query}
      ],
      response_format={ "type": "json_object" }
    )

    return response.choices[0].message.content


client_image = AzureOpenAI(
   api_key=os.getenv("OPENAI_API_KEY_IMAGE"),
   api_version="2024-02-01",
   azure_endpoint=os.getenv("OPEN_AI_ENDPOINT_IMAGE"),
)

def generate_image(heading: str)->str:
  
  PROMPT = f"""
  Ganerate an image for below article
  article heading:  {heading}
  """

  response = client_image.images.generate(
    model="dalle3",
    prompt=PROMPT,
    size="1024x1024",
    quality="standard",
    response_format='b64_json',
    n=1,
  )

  Image_base64 = response.data[0].b64_json
  return Image_base64