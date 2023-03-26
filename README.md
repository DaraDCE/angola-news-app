# angola-news-app
Source and display articles from Angolan RSS news feeds, with optional date and keyword selector

This Python code is an RSS news app built with the feedparser and streamlit packages to fetch and parse news articles from Angolan RSS feeds. The author is responding to the scarcity of Angolan news aggregators. The app allows the user to filter articles by date range and keyword search, and displays the results in reverse chronological order, with an option to load more articles up to a maximum of 20. The app was developed with the assitance of GPT-3.

Prerequisites
This code has the following Python package dependnecies:

feedparser
streamlit
datetime
fuzzywuzzy
unidecode
re
urllib.parse
Pillow

Usage
To run the app, navigate to the directory containing the Python script and run the following command in your terminal:

streamlit run rss_news_app.py

Once the app is running, you can use the date range and keyword search widgets to filter the articles displayed. Clicking on the "Carrega mais" button will load an additional 10 articles, up to a maximum of 20. The app displays the title, source, publication date, and link to each article.
