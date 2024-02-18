import datetime
from typing import Optional
from bs4 import BeautifulSoup
import requests as r
from helpers.Text import Text
from models.NewsModel import NewsModel

class NewsStudentsite(NewsModel):

    def get_data_all(self) -> list['NewsModel'] | None:
        response = r.get("https://studentsite.gunadarma.ac.id/index.php/site/news")
        if response.status_code == 200:
            article_lists = []
            sp = BeautifulSoup(response.content, 'html.parser')
            content_boxes = sp.find_all('div', class_='content-box')
            for content_box in content_boxes:
                article = {}
                article['title'] = content_box.find('h3', class_='content-box-header').get_text().strip()
                # article['url'] = f"https://studentsite.gunadarma.ac.id{content_box.find('a')['href']}"
                article['url'] = f"https://studentsite.gunadarma.ac.id{content_box.find('a', class_='btn btn-info')['href']}"
                article['id'] =  str(article['url']).split("/")[-1]
                article['body'] = content_box.find('div', class_='content-box-wrapper').text.strip()
                # article['date'] = content_box.find('div', class_='font-gray').text.strip()
                article['date'] = content_box.find('div', class_='font-gray').text.split("  ")[-1]
                article['source'] = "STUDENT SITE"
                article_lists.append(NewsModel(article))
            return article_lists
        else:
            return None
