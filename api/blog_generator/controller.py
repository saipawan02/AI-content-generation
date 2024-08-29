import os
import json
import traceback
from uuid import uuid4
import base64
from fastapi import APIRouter
from datetime import datetime

from config.openai_config import get_completion
from services.chroma_services import get_similar_articles, upload_article
from config.openai_config import generate_image
from models.Article import Article

router = APIRouter(
    prefix= '/blog-generator',
    tags= ['blog-generator']
)

if not os.path.exists("Images"):
    os.mkdir("Images")

@router.post('/article')
def generate_blogs(articles: list[Article]) -> list[Article]:

    header = f"""
You are an AI assistant who will generate a blog related to the given list of articles.
"""

    examples = "Below are the list of "
    for ndx, article in enumerate(articles):
        examples += "Article " + str(ndx + 1) + ": " + str(article.Content) + "\n\n"


    footer = """
return the blog in plain text format with proper heading and sub-heading.

### return the resoponse in the below JSON format:
{
    Title: <blog-Heading>,
    Content: <ganerated-blog>,
    Summary: <ganerated-blog-summary>,
    Tags: [<tag1>, <tag2>, <tag3>],
}

Note:
# Do not add any disclaimers and any other remarks in the blog.
# Make sure any information about the publisher of the original article is not mentioned.
# Blog content should be a string and render it in .md format and put '\n' instad of new line in the blog.
# Do not assign tags as a part of generated blog, provide them as an different field in the final response, 
# Only provide json object in the response with no extra spaces and content or any other characters.
# Format the complete content without any extra spaces, remove unsessary characters or special characters.
# Make sure the content is divided in proper heading and sub-heading with # and ## respectively.
"""

    query = header + examples + footer

    response = None
    counter = 0
    while True:
        try:
            response = get_completion(query)
            generated_blogs =  json.loads(response)
            break
        except:
            print(response)
            print(traceback.print_exc())
            counter += 1
            print(f"Invalid JSON response. Retrying... {counter}")


    api_response: list[Article] = []    
    
    if type(generated_blogs) != list:
        generated_blogs = [generated_blogs]
    
    for blog in generated_blogs:

        # Check if the article is already present in the database
        similarity_scores = dict(get_similar_articles(blog["Content"]))['distances'][0]
        if len(similarity_scores) == 0:
            similarity_scores = [0]

        skip_blog = False
        for score in similarity_scores:
            if score > 0.6:
                print(f"Skipping article: {blog['Title']} as similar article is already generated in the database with a score of {score}.")
                skip_blog = True
                break

        if skip_blog:
            continue

        # Gnenerate image
        image_base64 = generate_image(blog['Title'])

        # Store image
        uuid_id = str(uuid4())
        image_path = os.path.join('Images', uuid_id + '.jpg')
        with open(image_path, 'wb') as img_file:
            img_file.write(base64.b64decode(image_base64))

        article = Article(
            Date = str(datetime.now().date().strftime("%d-%m-%Y")),
            Title = blog['Title'],
            Summary = blog['Summary'],
            Content = blog['Content'],
            Tags = json.dumps(blog['Tags']),
            Image_id = uuid_id
        )

        upload_article(article)
        api_response.append(article)

    return api_response