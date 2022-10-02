import discord
import youtube_dl

from discord.ext import commands
from discord import app_commands
from colorama import init, Fore
import asyncio


init(autoreset=True)


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'cookiefile': 'cookies.txt',
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, volume=100):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Модуль музыки был успешно подключен и успешно работает!')


    @commands.hybrid_group(fallback='play', description='Играет любую введённую вами музыку')
    @app_commands.describe(query='Ваш поисковой запрос')
    @app_commands.describe(channel='Канал, в котором нужно будет проигрывать музыку')
    @commands.guild_only()
    async def music(self, ctx, channel: discord.VoiceChannel, *, query: str):
        embed = discord.Embed(title='Загрузка...', description=f'Идёт поиск музыки!\n\nЗапросил: <@{ctx.author.id}>\nЗапрос пользователя: {query}\n\n**Внимание!**\nЕсли бот не ответит в течении 15 секунд, вероятно произошла ошибка, возможные причины её возникновения:\n1) Видео с ограниченным доступом\n2) Требуется вход в YouTube-аккаунт для подтверждения возраста\n3) Видео заблокировано\n4) Бот просто не нашёл того, что вы запросили\n5) Неизвестная системная ошибка', color=discord.Color.blurple())
        await ctx.send(embed=embed)
        message = await ctx.channel.fetch_message(int(ctx.channel.last_message_id))
        player = await YTDLSource.from_url(query, stream=True)
        try:
            ctx.guild.voice_client.stop()
        except:
            try:
                await channel.connect()
            except:
                ctx.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title='Готово', description=f"Я нашёл то, что Вы и попросили!\nСейчас играет: ``{player.title}``\nДлительность: ``{player.duration}`` секунд(-а, -ы)\n\nПриятного прослушивания! :slight_smile: ", color=discord.Color.green())
                await ctx.channel.send(embed=embed)
            else:
                ctx.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title='Готово', description=f"Я нашёл то, что Вы и попросили!\nСейчас играет: ``{player.title}``\nДлительность: ``{player.duration}`` секунд(-а, -ы)\n\nПриятного прослушивания! :slight_smile: ", color=discord.Color.green())
                await ctx.channel.send(embed=embed)
        else:
            try:
                await channel.connect()
            except:
                ctx.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title='Готово', description=f"Я нашёл то, что Вы и попросили!\nСейчас играет: ``{player.title}``\nДлительность: ``{player.duration}`` секунд(-а, -ы)\n\nПриятного прослушивания! :slight_smile: ", color=discord.Color.green())
                await ctx.channel.send(embed=embed)
            else:
                ctx.guild.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                embed = discord.Embed(title='Готово', description=f"Я нашёл то, что Вы и попросили!\nСейчас играет: ``{player.title}``\nДлительность: ``{player.duration}`` секунд(-а, -ы)\n\nПриятного прослушивания! :slight_smile: ", color=discord.Color.green())
                await ctx.channel.send(embed=embed)


    @music.command(description='Установить громкость музыки')
    @app_commands.describe(volume='Громкость музыки')
    @commands.guild_only()
    async def volume(self, ctx, volume: int):
        if ctx.guild.voice_client is None:
            embed = discord.Embed(title='Ошибка', description=f'В данный момент, музыка не воспроизводится!', color=discord.Color.red())
        else:
            ctx.guild.voice_client.source.volume = volume / 100
            embed = discord.Embed(title='Готово', description=f'Я успешно выставил громкость музыку на {volume}% !', color=discord.Color.green())
            await ctx.send(embed=embed)


    @music.command(description='Остановить воспроизведение музыки')
    @commands.guild_only()
    async def stop(self, ctx):
        try:
            ctx.guild.voice_client.stop()
        except:
            embed = discord.Embed(title='Ошибка', description='В данный момент, музыка не воспроизводится!', color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Готово', description='Я успешно остановил воспроизведение музыки!', color=discord.Color.blurple())
            await ctx.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Music(client))