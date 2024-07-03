import json
from fastapi import APIRouter
from datetime import datetime

from config.openai_config import get_completion
from services.chroma_services import upload_article
from config.openai_config import generate_image
from models.Article import Article

router = APIRouter(
    prefix= '/blog-generator',
    tags= ['blog-generator']
)

@router.post('/article')
async def generate_blogs(articles: list[Article]) -> list[Article]:

    header = f"""
You are an AI assistant who will generate multiple blogs related to the given list of articles.
"""

    examples = "Below are the list of "
    for ndx, article in enumerate(articles):
        examples += "Article " + str(ndx + 1) + ": " + str(article) + "\n\n"


    footer = """
return the blog in plain text format with proper heading and sub-heading.

Note:
# Make sure the content is not repeated among the blogs and each blog that is generated should be unique.
# blog content should be a string and render it in .md format and put \n instad of new line in the blog.

return the resoponse in the folloing JSON format:
[
    {
        Title: <blog-Heading>,
        Content: <ganerated-blog>,
        Summary: <ganerated-blog-summary>,
        tags: [<tag1>, <tag2>, <tag3>],
    },
    {
        Title: <blog-Heading>,
        Content: <ganerated-blog>,
        Summary: <ganerated-blog-summary>,
        tags: [<tag1>, <tag2>, <tag3>],
    }
]

do not assign tags as a part of generated blog, provide them as an different field in the final response, 
and only provide json object in the response with no extra spaces and content or any other characters.
"""

    query = header + examples + footer
    print(query)
    generated_blogs = json.loads(get_completion(query))

    for blog in generate_blogs:
        upload_article(Article(
            Date = datetime.now(),
            Title = blog['Title'],
            Summary = blog['Summary'],
            Content = blog['Content'],
            Tags = blog['Tags'],
            Image_url= generate_image(blog['Title'])
        ))

    return generated_blogs
