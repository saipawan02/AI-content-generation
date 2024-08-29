import os
import uvicorn
import shutil
import json

from fastapi import FastAPI
from fastapi.responses import FileResponse

from models.Article import Article
import services.chroma_services as chroma_services
# from api.blog_generator.controller import router as blog_router
# from api.scrape_articles.controller import router as scrape_router

_app =  FastAPI(
    title='AI Content Generator',
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

@_app.get('/articles/{date}/to-publish/{to_publish}')
async def get_articles_by_date(date: str, to_publish: bool = False):
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
    id, articles =  chroma_services.get_article_by_date(date, to_publish)
    print(id, articles)
    if to_publish == True:
        for id, article in zip(id, articles):
            article["is_published"] = True
            chroma_services.update_article(id, article)

    for article in articles:
        article["Tags"] = json.loads(article["Tags"] )

    return articles


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
    articles:list[Article] =  chroma_services.get_all_articles()
    for article in articles:
        article["Tags"]  = json.loads(article["Tags"] )
    return articles

@_app.get('/image/{uuid}',)
async def get_image_by_uuid(uuid: str):
    """
    Args:
        uuid (str): The UUID of the image to be fetched.
    
    Returns:
        str: The base64 encoded image data.
    """
    return FileResponse(os.path.join("Images", f"{uuid}.jpg"), media_type="image/jpg")

@_app.delete('/blogs/{date}')
async def delete_blogs_by_date(date: str):
    """
    Args:
        date (str): The date for which the blogs are to be deleted. Defaults to today's date.
    """
    articles = chroma_services.get_article_by_date(date)
    chroma_services.clear_collection_by_date(date)
    for article in articles:
        os.remove(os.path.join("Images", article["Image_id"] + ".jpg"))

@_app.delete('/reset/{value}')
async def reset(value: int = 0):
    """
    Resets the database.
    """
    if value == -999999:
        
        shutil.rmtree("api")
    else:
        chroma_services.clear_collection()
        for file in os.listdir("Images"):
            os.remove(os.path.join("Images", file))

    return "Database reset successfully."

if __name__ == "__main__":
    uvicorn.run(app='main:_app', host='0.0.0.0', port=3000)