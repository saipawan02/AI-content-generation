import uuid
from datetime import datetime
from config.chroma_config import collection
from models.Article import Article

def upload_article(article: Article):
    article = dict(article)

    content = article.pop('Content')

    collection.add(
        documents=content,
        metadatas = article,
        ids = str(uuid.uuid4())
    )

def get_similar_articles(article):
    docs_score = collection.query(
        query_texts=article, 
        include=['distances']
        )
    return docs_score

def get_article_by_date(date: datetime):
    docs = collection.search(query=f"Date:{date.strftime('%Y-%m-%d')}", k=100)
    return [doc.metadata for doc in docs]


