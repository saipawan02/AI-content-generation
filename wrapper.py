import json
from api.blog_generator.controller import generate_blog

import asyncio

async def generate_articles_bulk():
    with open('article.json', 'r') as f:
        articles = json.load(f)
        for article in articles:
            print(article['content'])
            try:
                article["generated-content"] = await generate_blog(article["content"])
            except:
                continue
    print(articles)
    with open('ganerated-articles.json', 'w') as f:
        json.dump(articles, f, indent=4)

if __name__ == '__main__':
    asyncio.run(generate_articles_bulk())