import os
import openai

# prompt len should be 1000 words
PROMPT = """
Ganerate an image for below article

article:
# OpenAI and Worldcoin: Exploring Partnership Amidst Regulatory Scrutiny\n\n**Partnership Discussions and AI Solutions**\n\nOpenAI, led by Sam Altman, is reportedly in discussions with Worldcoin, a cryptocurrency-based identity verification and universal basic income firm, for a potential partnership. This collaboration aims to utilize OpenAI's expertise in artificial intelligence to enhance Worldcoin's identity verification processes and overall operations.

"""

openai.api_key = "sk-proj-mIIdnKwC9MS960O6VrqOT3BlbkFJTkuB1VOpYB6Gz0BilVes"
response = openai.Image.create(
    prompt=PROMPT,
    n=1,
    size="256x256",
    response_format="url")

print(response)
print(response["data"][0]["url"])