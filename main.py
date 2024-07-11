import uvicorn
from datetime import datetime
from fastapi import FastAPI

import services.chroma_services as chroma_services
from api.blog_generator.controller import router as blog_router
from api.scrape_articles.controller import router as scrape_router

_app =  FastAPI(
    title='Rag Fusion API',
    description='Retrieval augmented generation (RAG) is a natural language processing (NLP) technique that combines \
    the strengths of both retrieval- and generative-based artificial intelligence (AI) models.'
)

"""
routers are excluded as bolg generator and scrape articles are executed as corn job
"""

# Adding router to different API groups.
# _app.include_router(blog_router)
# _app.include_router(scrape_router)

@_app.get('/')
def check():
    return "Hey dev! This API endpoints are up and running."

@_app.get('/articles/{date}')
async def get_articles_by_date(date: str):
    """
    Args:
        date (str, optional): The date for which the articles are to be fetched. Defaults to today's date.
    
    Returns:
        list: A list of dictionaries containing the fetched articles. Each dictionary contains the following fields:
            - Date: The published date of the article.
            - Website: The URL of the website the article was published on.
            - Title: The title of the article.
            - Summary: The summary of the article.
            - Link: The URL of the article.
            - Content: The content of the article.
    """
    return chroma_services.get_article_by_date(date)


@_app.get('/articles')
async def get_all_articles():
    """
    Returns:
        list: A list of dictionaries containing the fetched articles. Each dictionary contains the following fields:
            - Date: The published date of the article.
            - Website: The URL of the website the article was published on.
            - Title: The title of the article.
            - Summary: The summary of the article.
            - Link: The URL of the article.
            - Content: The content of the article.
    """
    return chroma_services.get_all_articles()


if __name__ == "__main__":
    uvicorn.run(app='main:_app', host='0.0.0.0', port=3000)