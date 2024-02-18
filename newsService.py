from NewsBaak import NewsBaak 
from NewsStudentsite import NewsStudentsite 
from models.NewsModel import NewsModel
from dotenv import load_dotenv
import os
import discord
import datetime

class newsService:
    studentSite = NewsStudentsite()
    baak = NewsBaak()

    def __init__(self,bot) -> None:
        self.bot = bot

    def get_unique_news_baak(self):
        unique_news = []
        read_file = open("./uploaded/id_baak_uploaded.txt", "r")
        data_added = []
        news_list = self.baak.get_data_all()
        for line in read_file:
            data_added.append(line.split("\n")[0])
        for i, news in enumerate(news_list):
            if news.id not in data_added:
                unique_news.append(news)
        
        return unique_news
    
    def get_unique_news_studentsite(self):
        unique_news = []
        read_file = open("./uploaded/id_studentsite_uploaded.txt", "r")
        data_added = []
        news_list = self.studentSite.get_data_all()
        # print(news_list)
        for line in read_file:
            data_added.append(line.split("\n")[0])
        for i, news in enumerate(news_list):
            if i == 20: #limit to 20
                break
            if news.id not in data_added:
                unique_news.append(news)
        
        return unique_news
    
    def get_unique_news(self):
        unique_news = []

        for i, news in enumerate(self.get_unique_news_baak()):
            unique_news.append(news)
        
        for i, news in enumerate(self.get_unique_news_studentsite()):
            unique_news.append(news)
        return unique_news
    
    def add_news_to_list(self, news_list):
        x=0
        fileBaak = open("./uploaded/id_baak_uploaded.txt", "a")
        fileStudentSite = open("./uploaded/id_studentsite_uploaded.txt", "a")
        for i,news in enumerate(news_list):
            if news.source == "BAAK":
                fileBaak.write(f"{news.id}\n")
                x+=1
            elif news.source == "STUDENT SITE":
                fileStudentSite.write(f"{news.id}\n")
                x+=1
        fileBaak.close()
        fileStudentSite.close()
        
        return x
    
    def add_news_id_to_list(self,message : NewsModel):
        fileBaak = open("./uploaded/id_baak_uploaded.txt", "a")
        fileStudentSite = open("./uploaded/id_studentsite_uploaded.txt", "a")
        if message.source == "BAAK":
            fileBaak.write(f"{message.id}\n")
        elif message.source == "STUDENT SITE":
            fileStudentSite.write(f"{message.id}\n")
        fileBaak.close()
        fileStudentSite.close()
    
    def get_message(self):
        news_list = self.get_unique_news()
        message = ""
        if news_list == []:
            message = "Tidak ada berita terbaru"
            return
        for i,news in enumerate(news_list):
            message += "```"
            message += f"------- BERITA {news.source} ------\n"
            message += f"Judul: {str(news.title).strip()}\n"
            message += f"ID: {str(news.id)}\n"
            message += f"Tanggal: {news.date}\n"
            message += f"\n{news.body}\n\n"
            message += f"Lihat selengkapnya: {news.url}"
            message += "```"
        return message
    
    def format_message(self,content : NewsModel):
        message = ""
        message += "```"
        message += f"------- BERITA {content.source} ------\n"
        message += f"Judul: {str(content.title).strip()}\n"
        message += f"ID: {str(content.id)}\n"
        message += f"Tanggal: {content.date}\n"
        message += f"\n{content.body}\n\n"
        message += f"Lihat selengkapnya: {content.url}"
        message += "```"
        return message
    
    async def send_repeated_message(self):
        message = self.get_message()
        if message != "":
            target_channel_name = os.getenv("CHANNEL_NAME")

            for guild in self.bot.guilds:
                target_channel = discord.utils.get(guild.channels, name=target_channel_name)
                if target_channel == None:
                    target_channel = await self.create_new_channel(guild,target_channel_name)

                if target_channel:
                    for i,message in enumerate(self.get_unique_news()):
                        if await target_channel.send(self.format_message(message)) != None:
                            print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m News with id {message.id} Send\033[0m")
                            self.add_news_id_to_list(message)
                        else :
                            print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m News Not found\033[0m")
                    print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Service News Repeated Message Complete \033[0m")

        else :
            return

