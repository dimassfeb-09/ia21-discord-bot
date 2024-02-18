import discord
from repeatedMsgService import repeatedMsgService
import datetime
import os

class discordBotService:
    def __init__(self,bot) -> None:
        self.bot = bot

    async def create_new_channel(self,guild,channel_name):
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        new_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m New Text Channel Created in {guild.name}\033[0m")

        return new_channel
    
    async def send_repeated_message(self):
        message_automation = repeatedMsgService()
        message = message_automation.get_message()
        if message != "":
            target_channel_name = os.getenv("CHANNEL_NAME")

            for guild in self.bot.guilds:
                target_channel = discord.utils.get(guild.channels, name=target_channel_name)
                if target_channel == None:
                    target_channel = await self.create_new_channel(guild,target_channel_name)

                if target_channel:
                    await target_channel.send(message)
        print(f"\033[85m{datetime.datetime.now()} \033[0m  \033[96m[LOG]\033[0m \033[32m Service Assignment Repeated Message Complete \033[0m")