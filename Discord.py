import requests as r
from models.DiscordUser import DiscordUserModel
from models.NewsModel import NewsModel
from dotenv import load_dotenv
import os


class Discord:
    def __init__(self):
        load_dotenv()
        TOKEN_BOT = os.getenv("TOKEN_DISCORD")
        
        self.headers = {
            "Authorization": f"Bot {TOKEN_BOT}",
            "Content-Type": "application/json",
        }

        res = r.get(
            "https://discord.com/api/v10/users/@me",
            headers=self.headers,
        )

        if res.status_code == 200:
            user_info = DiscordUserModel(res.json())
            print(f"Success connect to Discord! {user_info.username}")
            # self.send_message(os.getenv("CHANNEL_COMMAND"), f"Success connect to Discord! {user_info.username}")
        else:
            print("Failed to connect Discord!")
            print(res.json())

    def send_message(self, channel_id: int, content: str, news: NewsModel) -> bool:
        
        read_file = open("./uploaded/id_baak_uploaded.txt", "r")
        data_added = []
        for line in read_file:
            data_added.append(line.split("\n")[0])
        
        if news.id not in data_added:
            res = r.post(f"https://discord.com/api/v10/channels/{channel_id}/messages",
                headers=self.headers,
                json={"content": content})
            if res.status_code == 200:
                write_file = open("./uploaded/id_baak_uploaded.txt", "a")
                write_file.write(f"{news.id}\n")
                write_file.close()
                return True
            else:
                return False
        
        
        
        

        
