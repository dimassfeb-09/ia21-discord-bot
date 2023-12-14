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
                self.title = content_box.find('h3', class_='content-box-header').text.strip()
                self.url = f"https://studentsite.gunadarma.ac.id{content_box.find('a')['href']}"
                self.id = self.url.split("/")[-1]
                self.body = content_box.find('div', class_='content-box-wrapper').text.strip()
                self.date = content_box.find('div', class_='font-gray').text.strip()
                self.source = "STUDENT SITE"
                article_lists.append(NewsModel(
                    self.id,
                    self.title,
                    self.url,
                    self.body,
                    self.date,
                    self.source,
                ))
            return article_lists
        else:
            return None
