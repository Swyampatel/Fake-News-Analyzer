from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

app = Flask(__name__)
CORS(app)

# Load the pre-trained fake news classifier
model = joblib.load("fake_news_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")  # Load the text vectorizer

def scrape_bbc_news():
    url = "https://www.bbc.com/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch BBC News. HTTP Status: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")

    headlines = []
    for item in soup.find_all("h2", attrs={"data-testid": "card-headline"}):
        title = item.get_text(strip=True)
        if title:
            headlines.append(title)

    if not headlines:
        raise ValueError("No headlines scraped. Check the scraper logic or the BBC website structure.")
    return headlines

def classify_news(headlines):
    predictions = model.predict(vectorizer.transform(headlines))
    results = {"Fake": [], "Real": []}
    for headline, prediction in zip(headlines, predictions):
        if prediction == 1:
            results["Fake"].append(headline)
        else:
            results["Real"].append(headline)
    return results

@app.route("/scrape", methods=["GET"])
def scrape():
    try:
        print("Starting scraping process...")
        headlines = scrape_bbc_news()
        print(f"Scraped Headlines: {headlines}")
        print("Classifying headlines...")
        classified_news = classify_news(headlines)
        print(f"Classified News: {classified_news}")

        months = ["Jan", "Feb", "Mar", "Apr", "May"]
        fake_articles_by_month = [len(classified_news["Fake"]) // len(months)] * len(months)
        true_articles_by_month = [len(classified_news["Real"]) // len(months)] * len(months)

        fake_word_cloud = [{"text": word, "value": len(word) * 2} for word in ["fake", "lies", "news", "hoax"]]
        true_word_cloud = [{"text": word, "value": len(word) * 2} for word in ["truth", "real", "verified", "accurate"]]

        data = {
            "months": months,
            "fake_articles_by_month": fake_articles_by_month,
            "true_articles_by_month": true_articles_by_month,
            "fake_word_cloud": fake_word_cloud,
            "true_word_cloud": true_word_cloud,
            "fake_headlines": classified_news["Fake"],
            "real_headlines": classified_news["Real"],
        }
        return jsonify(data)
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
