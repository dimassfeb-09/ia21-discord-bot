from discord.ext import commands
import discord
from Vclass import Vclass
from dotenv import load_dotenv
import os

# Create an instance of the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)


@bot.command(name='tugas', help='Responds with a greeting.')
async def tugas(ctx):
    
    vc = Vclass()
    courses = vc.getAssigmentAreNotYetDue()
    message = "============== DAFTAR TUGAS =============="
    for i, course in enumerate(courses):
        detail_course = course.detail_course()
        text = f"[{i+1}]\n"
        text += f"Kursus: {detail_course.course_title}\n"
        text += f"Deskripsi: {detail_course.description}\n"
        text += f"Tenggat: {detail_course.deadline}\n"
        text += f"Pengumpulan: {detail_course.assign_url}\n"
        text += f"===========================================\n"
        message += f"\n{text}"
    await ctx.send(message)

@bot.command(name='helpme', help='Responds with a greeting.')
async def helpme(ctx):
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

