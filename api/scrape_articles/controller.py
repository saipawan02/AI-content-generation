import json

from fastapi import APIRouter

from .web_crawler import web_crawler
from services.chroma_services import get_similar_articles, upload_article
from models.Article import Article

router = APIRouter(
    prefix= '/scrape-articles',
    tags= ['scrape-articles']
)

@router.post("/urls")
def scrape_article_url(urls: list[str]) -> list[Article]:
    """
    The Function will use the URL and fetch the articles from the Website.
    The Fetched articles will be then check in the vector database is similar set 
    of article is already published and then store the new articles in the vector database.
    """

    # Fetching the aricles from the website
    scraped_articles:list[Article] = web_crawler(urls)

    unique_new_articles:list[Article] = []

    for article in scraped_articles:
        similarity_scores = dict(get_similar_articles(article.Content))['distances'][0]
        
        if len(similarity_scores) == 0:
            similarity_scores = [0]

        to_publish = True
        for score in similarity_scores:
            if score < 0.3:
                print(f"Skipping article: {article.Title} as similar article is already present in the database.")
                to_publish = False
                break

        if to_publish == True:
            unique_new_articles.append(article)

    return unique_new_articles