from api.blog_generator.controller import generate_blogs
from api.scrape_articles.controller import scrape_article_url


from config.openai_config import get_completion

# print(get_completion("which model of the GPT are you?"))

url = ['https://Blockchain.News/RSS/', 'https://cryptoslate.com/feed/', 'https://www.the-blockchain.com/feed/']

scraped_blogs = scrape_article_url(url)


# Sending max 5 articles as context restriction.
no_of_articles = 1
if len(scraped_blogs) > no_of_articles:
    scraped_blogs = scraped_blogs[:no_of_articles]

print("____________GENERATED BLOGS____________")

print(generate_blogs(scraped_blogs))