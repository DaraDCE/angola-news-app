## Notícias Angolanas :flag-ao: :newspaper: :bulb:

Fetch and display news articles from different news sources covering Angola. Filter articles by keyword or by news source.

### Features

- Fetches articles from various Angolan news sources using RSS feeds
- Filter articles by fuzzy keyword search
- Filter articles by news source
- Display 10 articles initially, while the "Carrega mais" button loads an additional 10 articles, up to a maximum of 20

### Usage

To run the app, navigate to the directory containing the Python script and run the following command in your terminal:

streamlit run rss_news_app.py

### Dependencies

This app uses the following packages:

feedparser
streamlit
fuzzywuzzy
unidecode
Pillow