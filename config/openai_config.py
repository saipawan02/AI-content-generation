import openai
import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv("./cred.env")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


openai.api_key = OPENAI_API_KEY



def get_completion(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0,
    )
    return response


def azure_get_completion(query):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        temperature=0,
        api_endpoint=os.getenv("OPEN_AI_AZURE_ENDPOINT"),
        
    )
    return response

def generate_images(prompt):
    response = openai.Completion.create(
        engine="dalle-2",
        prompt=prompt,
        temperature=0.3,
        n=1,
        stop=None,
        max_tokens=10000,
    )
    return response