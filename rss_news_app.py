import feedparser
import streamlit as st
from datetime import datetime, date, timedelta, timezone
from fuzzywuzzy import fuzz
from unidecode import unidecode
import re
import urllib.parse
from PIL import Image

# List of RSS feeds
rss_feeds = {
    "Club-K": "https://www.club-k.net/index.php?option=com_obrss&task=feed&id=2:rss-noticias-do-club-k&format=feed&lang=pt",
    "O País": "https://opais.co.ao/feed/",
    "Africa Intelligence": "http://feeds.feedburner.com/AfricaIntelligence",
    "Correio da Kianda": "https://correiokianda.info/feed/",
    "Notícias de Angola": "https://noticiasdeangola.co.ao/feed/",
    "Folha 8": "https://jornalf8.net/feed/",
    "Imparcial Press": "https://imparcialpress.net/feed/"
}

# List of allowed domains for RSS feeds
allowed_domains = ["club-k.net/", "opais.co.ao", "feeds.feedburner.com",
"correiokianda.info", "noticiasdeangola.co.ao", "jornalf8.net", "imparcialpress.net"]

# Create two columns with different widths, for logo and app name
col1, col2 = st.columns([3.3, 0.7], gap="medium")
with col1:
    col1.write(f'## Notícias de Angola, Africa e o mundo ##')
with col2:
    image = Image.open("https://raw.githubusercontent.com/DaraDCE/angola-news-app/master/dce_logo_extrasmall_jpeg.jpg")
    col2.image(image, use_column_width=True)

# Widgets for searching by date range and keywords, displayed in column with app (as opposed to 'sidebar')
end_date = st.date_input("Filtrar por data: mais recente", value=date.today())
start_date = st.date_input("Filtrar por data: mais antiga", value=(date.today() - timedelta(days=7)))
keyword = st.text_input("Procurar palavra-chave", value='')

# Fetch and parse the RSS feed
filtered_articles = []

# Validate and sanitize the URL for each RSS feed (security)
for source, url in rss_feeds.items():
    try:
        # Validate the URL format
        if not re.match(r"^https?://", url):
            raise ValueError("URL não está em um formato válido")
        
        # Parse the URL to check the domain
        parsed_url = urllib.parse.urlparse(url)
        if parsed_url.netloc not in allowed_domains:
            raise ValueError("O domínio não é permitido")

        # Sanitize the URL parameters
        sanitized_url = urllib.parse.urlunparse(parsed_url._replace(query=""))
        
        # Use HTTPS
        if parsed_url.scheme == "http":
            sanitized_url = "https://" + parsed_url.netloc + parsed_url.path
        
        feed = feedparser.parse(sanitized_url)
    except Exception as e:
        print(f"Houve um erro ao interpretar a fonte {source}: {e}")
        continue

    for item in feed["entries"]:
        # Filter by date
        if start_date and end_date:
            if datetime(*item.published_parsed[:6]).date() < start_date or datetime(*item.published_parsed[:6]).date() > end_date:
                continue
        elif start_date:
            if datetime(*item.published_parsed[:6]).date() < start_date:
                continue
        elif end_date:
            if datetime(*item.published_parsed[:6]).date() > end_date:
                continue

        # Filter by keyword with fuzzy search
        if keyword:
            title_score = fuzz.token_set_ratio(unidecode(keyword.lower()), unidecode(item.title.lower()))
            summary_score = fuzz.token_set_ratio(unidecode(keyword.lower()), unidecode(item.summary.lower()))
            if title_score < 80 and summary_score < 80:
                continue

        filtered_articles.append((source, item))

# Sort the filtered news articles by date
filtered_articles = sorted(filtered_articles, key=lambda x: datetime(*x[1].published_parsed[:6]), reverse=True)

# Display the filtered news articles with buttons to increment upto max 20 and reset
if filtered_articles:
    articles_displayed = 10
    for i, (source, item) in enumerate(filtered_articles[:articles_displayed]):
        st.write(f"## {item['title']}")
        st.write(f"**Fonte:** {source},  " + f"**Publicado:** {item['published']}")
        #st.write(f"**Publicado:** {item['published']}")
        #st.markdown(item["summary"]) # exclude markdown summary
        st.write(f"Leia mais: {item['link']}")
    
    if len(filtered_articles) > 10:
        load_more = st.button('Carrega mais')
        if load_more:
            articles_displayed += 10
            if articles_displayed > 20:
                articles_displayed = 20
                st.write("_Não há mais notícias para carregar._")
            else:
                for i, (source, item) in enumerate(filtered_articles[10:articles_displayed], start=10):
                    st.write(f"## {item['title']}")
                    st.write(f"**Fonte:** {source},  " + f"**Publicado:** {item['published']}")
                    #st.write(f"**Publicado:** {item['published']}")
                    #st.markdown(item["summary"]) # exclude markdown summary
                    st.write(f"Leia mais: {item['link']}")

            st.write(f"{articles_displayed} notícias exibidas.")
            if articles_displayed == 20:
                st.write("_Não há mais notícias para carregar._")
        else:
            st.write(f"{articles_displayed} notícias exibidas.")
    else:
        st.write("_Não foram encontradas mais notícias relacionadas às palavras-chave ou no período definido._")

    if articles_displayed > 10:
        reset = st.button('Reiniciar')
        if reset:
            articles_displayed = 10
            st.experimental_rerun()
else:
    st.write("_Não foram encontradas mais notícias relacionadas às palavras-chave ou no período definido._")
