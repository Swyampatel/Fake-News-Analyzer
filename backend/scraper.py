import requests
from bs4 import BeautifulSoup

def scrape_news():
    # Target the BBC News homepage
    url = "https://www.bbc.com/news"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    # Scrape news articles from the BBC News homepage
    for article in soup.find_all('div', class_='gs-c-promo', limit=20):  # Limit to 20 articles for demo
        try:
            # Extract title
            title = article.find('h3').text.strip() if article.find('h3') else "No title available."
            # Extract link
            link = article.find('a', href=True)['href']
            if not link.startswith("https"):
                link = "https://www.bbc.com" + link
            # Extract summary/content
            content = article.find('p').text.strip() if article.find('p') else "Content not available."
            # Append extracted data
            articles.append({
                'title': title,
                'link': link,
                'content': content,
            })
        except Exception as e:
            # Skip malformed articles
            print(f"Error processing article: {e}")
            continue

    return articles
