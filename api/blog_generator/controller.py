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
def generate_blogs(articles: list[Article]) -> list[Article]:

    header = f"""
You are an AI assistant who will generate multiple blogs related to the given list of articles.
"""

    examples = "Below are the list of "
    for ndx, article in enumerate(articles):
        examples += "Article " + str(ndx + 1) + ": " + str(article.Content) + "\n\n"


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
        Tags: [<tag1>, <tag2>, <tag3>],
    },
    {
        Title: <blog-Heading>,
        Content: <ganerated-blog>,
        Summary: <ganerated-blog-summary>,
        Tags: [<tag1>, <tag2>, <tag3>],
    }
]

do not assign tags as a part of generated blog, provide them as an different field in the final response, 
and only provide json object in the response with no extra spaces and content or any other characters.
"""

    query = header + examples + footer

    response = get_completion(query)
    # print("Response:", response)
    generated_blogs = json.loads(response)
    # print("Generated Blogs:", generated_blogs)

    api_response: list[Article] = []
    for blog in generated_blogs:
        print(blog)
        article = Article(
            Date = str(datetime.now().date().strftime("%d-%m-%Y")),
            Title = blog['Title'],
            Summary = blog['Summary'],
            Content = blog['Content'],
            Tags = json.dumps(blog['Tags']),
            Image_url= generate_image(blog['Title'])
        )

        upload_article(article)
        api_response.append(article)

    return api_response