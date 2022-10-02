
import discord
from discord import app_commands
from discord.ext import tasks, commands
from func import *
import traceback
import random
import asyncio
import os
from itertools import cycle
import datetime, time
from datetime import timezone
from modules.Verification import create_captcha_code
import sys
from colorama import init, Fore


init(autoreset=True)
intents = discord.Intents().all()
client = commands.AutoShardedBot(command_prefix=['sp.', 'sp?', 'sp!'], intents=intents, shard_count=5)


config = load_json("configs/config.json")


@client.event
async def on_ready():
    tree = client.tree
    await tree.sync()
    change_status.start()
    client.add_view(create_captcha_code())
    use_commands = True
    print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.WHITE + f' Все модули загружены. Бот готов к работе!')


@client.event
async def on_connect():
    global startTime
    startTime = time.time()


@tasks.loop(seconds=15)
async def change_status():
    url = "https://www.youtube.com/watch?v=Khe3jIWqN0c"
    guilds = len(list(client.guilds))
    status = f"Количество серверов: {guilds}"
    await client.change_presence(
        activity=discord.Game(name=status, type="watching"))
    await asyncio.sleep(5)
    status = f"Количество шардов: {client.shard_count}"
    await client.change_presence(
        activity=discord.Game(name=status, type="watching"))
    await asyncio.sleep(5)
    status = f"Пинг бота: {round(client.latency * 1000)}ms"
    await client.change_presence(
        activity=discord.Game(name=status, type="watching"))


@tasks.loop(seconds=3)
async def check_blacklist():
    blacklist = load_json("configs/blacklist.json")
    for guild in client.guilds:
        if guild.id in blacklist['list']:
            gguild = await client.fetch_guild(int(guild.id))
            embed = discord.Embed(
                title='Вы в чёрном списке!',
                description=
                f'Ваш сервер {gguild.name} находится в чёрном списке бота! Я покидаю вас и ваш сервер.',
                color=discord.Color.red())
            user = await client.fetch_user(int(gguild.owner_id))
            try:
                await user.send(embed=embed)
                await gguild.leave()
            except:
                await gguild.leave()


@client.command(name='unload-module')
async def unloadm(ctx, name: str):
    if check_bot_owner(ctx.author.id):
        try:
            await client.unload_extension(f"modules.{name}")
        except Exception as e:
            embed = discord.Embed(title='Ошибка', description=f'{e}', color=discord.Color.red())
        else:
            embed = discord.Embed(title='Готово', description=f'Модуль {name} был успешно отключен.', color=discord.Color.green())
        await ctx.send(embed=embed)


@client.command(name='load-module')
async def loadm(ctx, name: str):
    if check_bot_owner(ctx.author.id):
        try:
            await client.load_extension(f"modules.{name}")
        except Exception as e:
            embed = discord.Embed(title='Ошибка', description=f'{e}', color=discord.Color.red())
        else:
            embed = discord.Embed(title='Готово', description=f'Модуль {name} был успешно подключен.', color=discord.Color.green())
        await ctx.send(embed=embed)


@client.command(name='restart-module')
async def restartm(ctx, name: str):
    if check_bot_owner(ctx.author.id):
        try:
            await client.reload_extension(f"modules.{name}")
        except Exception as e:
            embed = discord.Embed(title='Ошибка', description=f'{e}', color=discord.Color.red())
        else:
            embed = discord.Embed(title='Готово', description=f'Модуль {name} был успешно перезапущен.', color=discord.Color.green())
        await ctx.send(embed=embed)


@client.hybrid_command(description='Информация о боте')
async def bot(ctx):
    embed = discord.Embed(title='Информация о боте', color=discord.Color.blue())
    embed.add_field(name='🌎 Пинг', value=f'{round(client.latency * 1000)}ms', inline=False)
    shard = client.get_shard(ctx.guild.shard_id)
    embed.add_field(name='🖥 Шарды', value=f'Всего шардов: {client.shard_count}\nID шарда данного сервера: {ctx.guild.shard_id}\nПинг шарда данного сервера: {round(shard.latency * 1000)}ms', inline=False)
    embed.add_field(name='🤖 Имя бота', value='Конечно же **Splash!**', inline=False)
    embed.add_field(name='🐍 Версия Python', value=f'Python {sys.version}', inline=False)
    embed.add_field(name='👑 Количество гильдий, на которых находится бот', value=f'{len(client.guilds)} сервер (-а, -ов)', inline=False)
    embed.add_field(name='🕓 Аптайм бота', value=f'{str(datetime.timedelta(seconds=int(round(time.time()-startTime))))}', inline=False)
    embed.add_field(name='👨‍💻 Разработчики бота', value='Самый единственный и неповторимый <@553960665581355009>', inline=False)
    embed.add_field(name='🔗 Полезные ссылки', value='🔮 [Пригласить бота к себе на сервер](https://discord.com/api/oauth2/authorize?client_id=995064500610932747&permissions=8&scope=bot%20applications.commands)\n❓ [Сервер поддержки и место обитания бота](https://discord.gg/f8N5uzJvgx)\n:cat: [GitHub](https://github.com/IIDarkNessYT/splash-discord-verify-bot)')
    await ctx.send(embed=embed)


async def start():
    client.remove_command('help')
    for filename in os.listdir("./modules"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await client.load_extension(f"modules.{filename[:-3]}")


asyncio.run(start())
client.run(config['token'])