import uuid
from datetime import datetime
from config.chroma_config import collection
from models.Article import Article

def upload_article(article: Article):
    article = dict(article)

    content = article['Content']

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

def get_article_by_date(date: str):
    # date = datetime.strptime(date, '%d-%m-%Y')
    docs = collection.get(where={'Date': date})
    return docs["metadatas"]

def get_all_articles():
    docs = collection.get()
    
    print(docs['documents'])

    return docs["metadatas"]

def clear_collection():
    collection.delete(where={})

def clear_collection_by_date(date: datetime):
    date = datetime.strptime(date, '%d-%m-%Y')
    collection.delete(where={'Date': date})