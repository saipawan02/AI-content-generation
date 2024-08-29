import uuid
from datetime import datetime
from config.chroma_config import collection, client
from models.Article import Article

def upload_article(article: Article):
    article = dict(article)

    content = article['Content']

    collection.add(
        documents=content,
        metadatas = article,
        ids = str(uuid.uuid4())
    )

def update_article(id:str, article: Article):
    article = dict(article)

    collection.update(
        ids=id,
        metadatas = article
    )

def get_similar_articles(article):
    docs_score = collection.query(
        query_texts=article, 
        include=['distances']
        )
    return docs_score

def get_article_by_date(date: str, to_publish: bool):
    # date = datetime.strptime(date, '%d-%m-%Y')
    if to_publish == True:
        docs = collection.get(where={'$and':[{'Date': date}, {'is_published': False}]})
    else:
        docs = collection.get(where={'Date': date})
    return [docs["ids"], docs["metadatas"]]

def get_all_articles():
    docs = collection.get()
    print(docs['documents'])
    return docs["metadatas"]

def clear_collection():
    client.delete_collection(name="chroma_collection")
    
def clear_collection_by_date(date: datetime):
    # date = datetime.strptime(date, '%d-%m-%Y')
    collection.delete(where={'Date': date})