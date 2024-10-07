from config.chroma_config import collection
import json

def get_similar_articles(article, date):
    
    docs = collection.query(
        query_texts=article, 
        where= {'Date': date},
        n_results = 10
        )
    return docs

def get_all_articles(date):
    docs = collection.get(where={'Date': date})
    return docs

date = "03-09-2024"
docs =  get_all_articles(date)
# print(docs)

result = {}
for doc in docs['metadatas']:
    title = doc['Title']
    content = doc['Content']


    articles = get_similar_articles(content, date)

    # print(articles)
    for article, article_score in zip(articles['metadatas'][0], articles['distances'][0]):
        print(article)
        print(article["Title"], article_score)
        if title not in result:
            result[ title ] = {}

        result[title][article["Title"]] = article_score

print(result)
json.dump(result, indent=4, fp=open('comparison.json', 'w'))
