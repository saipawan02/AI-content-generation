import random
from datetime import datetime
from api.blog_generator.controller import generate_blogs
from api.scrape_articles.controller import scrape_article_url

print(f"Executing the pipeline at {datetime.now()}")

url = ['https://Blockchain.News/RSS/', 'https://cryptoslate.com/feed/', 'https://www.the-blockchain.com/feed/']

scraped_blogs = scrape_article_url(url)
print(f"Total of {len(scraped_blogs)} articles are genenrated.")

# Sending max 4 articles as context restriction.
no_of_articles = min(len(scraped_blogs), 4)

scraped_blogs = random.sample(scraped_blogs, no_of_articles)

print("____________GENERATED BLOGS____________")

print(generate_blogs(scraped_blogs))