import ssl
from bs4 import BeautifulSoup
import feedparser
import requests
from typing import List
from datetime import datetime
from models.Article import Article


# Ignore SSL certificate verification (not recommended)
ssl._create_default_https_context = ssl._create_unverified_context

def web_crawler(rss_feed_urls: list[str]) -> list[Article]:
    """
    Web crawler to scrape the latest articles from the given RSS feeds.

    Args:
        rss_feed_url (str): The URL of the RSS feed.

    Returns:
        list: A list of dictionaries containing the scrapped articles.
            Each dictionary contains the following fields:
            - Date: The published date of the article.
            - Website: The URL of the website the article was published on.
            - Title: The title of the article.
            - Summary: The summary of the article.
            - Link: The URL of the article.
            - Content: The content of the article.
    """
    scrapped_articles: list[Article] = []
    
    for rss in rss_feed_urls:
        
        # Parse the RSS feed
        feed = feedparser.parse(rss)
        # Scrape articles from the feed
        for entry in feed.entries:
            date = entry.published

            try:
                date = datetime.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
            except ValueError:
                continue

            if str(date.date()) != str(datetime.now().date()):
                print(f"Skipping article: {entry.title} as it was published on {date.date()}")
                # This article is not the latest article so cannot be processed.
                # Skip to the next article.
                continue
            

            title = entry.title
            
            # Fetch and extract article content
            try:
                response = requests.get(entry.link)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    paragraphs = soup.find_all('p')
                    article = ' '.join([p.get_text().strip() for p in paragraphs])
                else:
                    article = ''
                    print(f"Failed to fetch article content: {response.status_code}")
            except Exception as e:
                article = ''
                print(f"Exception occurred while fetching article content: {e}")
            
            # Parse the HTML content of the summary
            soup = BeautifulSoup(entry.summary, 'html.parser')
            summary_text = soup.get_text(strip=True)
            
            # Add article to the list of scraped articles
            
            scrapped_articles.append(
                Article(
                    Date = date,
                    Title = title,
                    Summary = summary_text,
                    Content = article
                )
            )


    return scrapped_articles


