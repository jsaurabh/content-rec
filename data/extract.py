"""
Data extraction scripts for scraping content from blogs, Wikipedia and MOOC platforms
"""

from utils import day2month

import requests
from calendar import isleap
from bs4 import BeautifulSoup

urls = {
    'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
}

def extract_medium(urls: dict, year: int) -> list:
    results = []
    days = list(range(1, 10 if isleap(year) else 11))
    idx, article_id = 0, 0

    for day in days:
        idx += 1
        month, day = day2month(day)

        for pub, url in urls.items():
            formatted_url = url.format(year, month, day)
            response = requests.get(formatted_url, allow_redirects=True)
            if not response.url.startswith(url.format(year, month, day)):
                continue
            
            page = response.content

            soup = BeautifulSoup(page, 'html.parser')

            articles = soup.find_all("div", class_="postArticle postArticle--short js-postArticle js-trackPostPresentation js-trackPostScrolls")
            for article in articles:
                title = article.find("h3", class_="graf--title")
                if title is None:
                    continue

                title = title.contents[0]
                article_id += 1
                sub = article.find("h4", class_="graf--subtitle")
                if sub:
                    sub = sub.contents[0]
                else:
                    sub = ""
                
                link = article.find_all("a")[3]['href'].split("?")[0]
                time = article.find("span", class_="readingTime")
                time = 0 if time is None else int(time['title'].split(" ")[0])

                print(article_id, link, title, sub, time)
                info = {
                    "id": article_id,
                    "url": link,
                    "title": title,
                    "subtitle": sub,
                    "readTime": time
                }
                results.append(info)

    return results