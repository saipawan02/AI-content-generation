
import google.generativeai as genai
from google.ai import generativelanguage as glm


GOOGLE_API_KEY = "AIzaSyCoSLp4cGbTuGWLskj37JwAbtVTSBAJEIE"

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_completion(query):
    response = model.generate_content(query, generation_config= glm.GenerationConfig(temperature=0.0,))
    print(response.text, type(response.text))
    return response.text.strip()