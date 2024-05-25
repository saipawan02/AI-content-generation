import json

from fastapi import APIRouter

from config.gemini_config import get_completion

router = APIRouter(
    prefix= '/blog-generator',
    tags= ['blog-generator']
)

@router.get('/article')
async def generate_blog(article: str) -> dict:
    header = f"""
Generate a Blog to the article below:
{article}

make sure the article is in the correct format and free from plagarism.
"""

    footer = """
return the blog in plain text format with proper heading and sub-heading.

Note:
# blog content should be a string and render it in .md format and put \n instad of new line in the blog.

return the resoponse in the folloing JSON format:
{
    <blog-Heading>: <ganerated-blog>,
    tags: [<tag1>, <tag2>, <tag3>],
}

do not assign tags as a part of generated blog, provide them as an different field in the final response, 
and only provide json object in the response with no extra spaces and content or any other characters.
"""

    query = header + footer
    return json.loads(get_completion(query))


@router.post('/articles')
async def generate_blogs(articles_json: dict):
    for article in articles_json:
        article["generated-content"] = generate_blog(article["content"])
    return articles_json