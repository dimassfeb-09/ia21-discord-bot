from discord.ext import commands, tasks
import discord
from Vclass import Vclass
from dotenv import load_dotenv
import os
import datetime
import asyncio
from newsService import newsService

from discordBotService import discordBotService

# Create an instance of the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

botService = discordBotService(bot)
serviceNews = newsService(bot)

@bot.event
async def on_guild_join(guild):
    channel_name = os.getenv("CHANNEL_NAME")
    channel_exists = any(channel.name == channel_name for channel in guild.channels)

    if not channel_exists:
        create_channel = await botService.create_new_channel(guild,channel_name)
        create_channel.send("Hello From Bot!")

@bot.event
async def on_ready():
    print(f'\033[96mLogged in as {bot.user.name} ({bot.user.id}) \033[0m')

    now = datetime.datetime.now()
    current_hour = datetime.datetime.now().hour
    next_hour = datetime.datetime(year=datetime.datetime.now().year,month=datetime.datetime.now().month,day=datetime.datetime.now().day,hour=current_hour+1,minute=00,second=00,microsecond=00)
    
    time_difference =   next_hour - now

    minutes_to_wait = time_difference.total_seconds()

    await asyncio.sleep(minutes_to_wait)
    send_message.start()


@tasks.loop(hours=1,reconnect=True) 
async def send_message():
    print(f"\033[85m{datetime.datetime.now()} \033[0m \033[32m Send Repeated Task For Hourly Reminder \033[0m")
    await botService.send_repeated_message()
    await serviceNews.send_repeated_message()

@bot.command(name='tugas', help='Responds with a assignment list.')
async def tugas(ctx):
    print(f"\033[85m{datetime.datetime.now()} \033[0m \033[32m Command /tugas Raise in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.message.channel} by {ctx.message.author}\033[0m")
    vc = Vclass()
    courses = vc.getAssigmentAreNotYetDue()
    # courses = vc.getAssignmentByTimeStamp('1701450000') #for testing purpose
    # print(courses)
    if courses == []:
        await ctx.send("Tidak Ada tugas dalam Waktu Dekat, Selamat Beristirahat :person_in_bed:")
        return
    message = "============== DAFTAR TUGAS V-Class =============="
    for i, course in enumerate(courses):
        # print(course)
        detail_course = course.detail_course()
        text = "\n"
        # text += f"[{i+1}]\n"
        text += f"[***{course.title}***]\n"
        text += f"Kursus: {detail_course.course_title}\n"
        text += f"Deskripsi: {detail_course.description}\n"
        text += f"Tenggat: {detail_course.deadline}\n"
        text += f"Pengumpulan: {detail_course.assign_url}\n"
        text += f"===========================================\n"
        message += f"\n{text}"
    await ctx.send(message)

@bot.command(name='helpme', help='Responds with a greeting.')
async def helpme(ctx):
    print(f"\033[85m{datetime.datetime.now()} \033[0m \033[32m Command /helpme Raise in {ctx.guild.name} ({ctx.guild.id}) in channel {ctx.message.channel} by {ctx.message.author}\033[0m")
    menus = """
    Keyword List
    **/bantu**: Menampilkan command yang tersedia.
    **/tugas**: Menampilkan tugas masa mendatang.
    **/jadwal**: Menampilkan jadwal kelas (Comming soon).
    """
    await ctx.send(menus)



# Load file .env
load_dotenv()
BOT_TOKEN = os.getenv("TOKEN_DISCORD")
bot.run(BOT_TOKEN)

