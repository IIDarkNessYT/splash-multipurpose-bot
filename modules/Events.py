import os
import shutil
import discord

from discord.ext import commands
from colorama import init, Fore
from func import *
import random
import asyncio

init(autoreset=True)


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_shard_connect(self, shard):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Шард с ID {shard} был успешно подключен!')


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Модуль событий был успешно подключен и успешно работает!')


    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        try:
            cfg = load_json(f"guilds/{msg.guild.id}/config.json")
        except:
            pass
        else:
            try:
                stat = cfg["chat-filter"]
            except KeyError:
                cfg["chat-filter"] = "off"
                write_json(f"guilds/{msg.guild.id}/config.json", cfg)
            else:
                if cfg["chat-filter"] == "on":
                    if msg.author.bot is False:
                        mess = msg.content.lower()
                        for mats in mess.split(' '):
                            if mats in bot["matlist"]:
                                try:
                                    await msg.delete()
                                except:
                                    t = 't'
                                finally:
                                    try:
                                        await msg.author.timeout(datetime.timedelta(minutes=2), reason=f'Наказание выдано за использование плохого слова! (фильтрация чата)', color=discord.Color.red())
                                    except:
                                        embed = discord.Embed(title='Сообщение удалено', description=f'{msg.author.mention}, в вашем сообщении было использовано плохое слово и сообщение было удалено!', color=discord.Color.red())
                                        await msg.channel.send(embed=embed, delete_after=5)
                                    else:
                                        embed = discord.Embed(title=f'Участнику {msg.author} вынесено наказание за плохое слово.', description=f'Наказание: Тайм-аут (мут) на одну минуту.')
                                        await msg.channel.send(embed=embed, delete_after=5)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            guild_id = member.guild.id
            config = load_json(f"guilds/{guild_id}/config.json")
            if config['channelcaptcha'] != "none":
                if member.bot is True:
                    if config['ignorebots'] != "false":
                        if config['lockserver'] == "true":
                            await member.kick(reason="Сервер заблокирован владельцем")
                else:
                    if config['lockserver'] == "true":
                        embed = discord.Embed(title=f"Упс...", description=f"Простите, но Вы не можете заходить на сервер **{member.guild.name}**, так как он заблокирован владельцем.", color=discord.Color.red())
                        await member.send(embed=embed)
                        await member.kick(reason="Сервер заблокирован владельцем")
                        embed = discord.Embed(title=f"{member.name} был кикнут.", description=f"Пользователь был кикнут, так как сервер был заблокирован администратором.", color=discord.Color.red())
                        channel = member.guild.get_channel(int(config['logchannel']))
                        await channel.send(embed=embed)
                    else:
                        guild = member.guild
                        if config['comernoticechannel'] != "false":
                            channel = guild.get_channel(int(config['comernoticechannel']))
                            embed = discord.Embed(title=f"{member.name} присоединился к серверу", description=f"Поприветствуем нового пользователя {member.mention} на нашем сервере!", color=discord.Color.green())
                        await channel.send(embed=embed)
                        users = load_json(f"guilds/{guild_id}/users.json")
                        users[f'{member.id}'] = 'notverified'
                        write_json(f"guilds/{guild_id}/users.json", users)
                        await asyncio.sleep(900)
                        users = load_json(f"guilds/{guild_id}/users.json")
                        if users[str(member.id)] != "leaved":
                            codes = load_json(f"guilds/{guild_id}/users.json")
                            userdata = codes[str(member.id)]
                            if userdata != 'verified':
                                embed = discord.Embed(title=f"{member.name} был кикнут.", description=f"Пользователь был кикнут, так как не прошёл проверку на робота в течении заданного времени (15 минут)", color=discord.Color.red())
                                channel = member.guild.get_channel(int(config['logchannel']))
                                await channel.send(embed=embed)
                                await member.kick(reason='Индивидуальный капча-код не был введён в течении 15 минут')
                        else:
                            codes = load_json(f"guilds/{guild_id}/users.json")
                            codes.pop(str(member.id))
                            write_json(f"guilds/{guild_id}/users.json", codes)
        except:
            try:
                await member.guild.owner.send('Произошла ошибка, когда пользователь присоединился к вашему серверу. Возможно, у меня нет прав на получение данных сервера, либо отсутствуют файлы конфигурации. Пожалуйста, настройте меня для стабильной работы!')
            except:
                guild = self.client.get_guild(995048257447280770)
                channel = guild.get_channel(999356269137764383)
                await channel.send(f'Произошла ошибка, когда пользователь присоединился к серверу. Возможно, у меня нет прав на получение данных сервера, либо отсутствуют файлы конфигурации.')


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            guild_id = member.guild.id
            guild = member.guild
            status = "leaved"
            users = load_json(f"guilds/{guild_id}/users.json")
            users[str(member.id)] = str(status)
            write_json(f"guilds/{guild_id}/users.json", users)
            config = load_json(f"guilds/{guild_id}/config.json")
            if config['lockserver'] != "true":
                if config['comernoticechannel'] != "false":
                    channel = guild.get_channel(int(config['comernoticechannel']))
                    embed = discord.Embed(title=f"{member.name} покинул сервер", description=f"Будем ждать тебя здесь снова, **{member.name}**!", color=discord.Color.orange())
                    await channel.send(embed=embed)
                else:
                    pass
            else:
                pass
        except:
            pass


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_id = guild.id
        try:
            channel = await guild.create_text_channel("splash-bot-информация")
            await channel.set_permissions(guild.default_role, send_messages=False)
            await channel.set_permissions(guild.default_role, view_channel=False)
            await channel.send(f"{guild.owner.mention}")
            embed = discord.Embed(title=f"Внимание!", description=f"К Вам пригласили бота верификации **Splash!**, он же сплэшик :D\nИдёт настройка вашего сервера для правильной работы верификации. Пройдёт 2 этапа:\n``Создание файлов на сервере`` - создание конфигурационного файла, а так же файла со всеми участниками сервера\n``Обработка пользователей`` - занесение пользователей в наш сервер для получения их списка\n\nНастройка сервера начнётся через 15 секунд...", color=discord.Color.blue())
            await channel.send(embed=embed)
            message = await channel.fetch_message(channel.last_message_id)
            os.mkdir(f"guilds/{guild_id}")
            await asyncio.sleep(15)
            shutil.copy('samples/guild_configuration.json', f'guilds/{guild.id}/config.json')
            shutil.copy('samples/guild_users.json', f'guilds/{guild.id}/users.json')
            shutil.copy('samples/guild_warns.json', f'guilds/{guild.id}/warns.json')
            pr = load_json("premium.json")
            try:
                prg = pr[f"{guild.id}"]
            except KeyError:
                pr[f"{guild.id}"] = "false"
                write_json("premium.json", pr)
            members_int = 0
            members = len(list(guild.members))
            for member in guild.members:
                members_int = members_int + 1
                users = load_json(f"guilds/{guild_id}/users.json")
                status = "verified"
                users[str(member.id)] = str(status)
                write_json(f"guilds/{guild_id}/users.json", users)
                embed = discord.Embed(title=f"Идёт настройка...", description=f"Статус обработки участников: ``{members_int} / {members}``. Как только цифры перестанут меняться - бот окончит настройку", color=discord.Color.blue())
                await message.edit(embed=embed)
                if members_int == members:
                    embed = discord.Embed(title=f"Настройка завершена!", description=f"Вам осталось настроить до конца бота через слэш-команды и начать им пользоваться!", color=discord.Color.green())
                    await message.edit(embed=embed)
        except:
            try:
                owner = await self.client.fetch_user(guild.owner_id)
                await owner.send("К вам пригласили бота Splash! Вы видите данное сообщение потому, что произошла ошибка, и возможно у бота недостаточно прав. Пожалуйста, переавторизуйте бота (кикните бота и перейдите по ссылке OAuth2 Discord(-а)) с правами администратора, иначе бот не сможет работать стабильно без прав.")
            except:
                pass


    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            shutil.rmtree(f'guilds/{guild.id}')
        except:
            pass


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        try:
            config = load_json(f"guilds/{channel.guild.id}/config.json")
            if config['role'] != "none":
                role = channel.guild.get_role(int(config['role']))
                await channel.set_permissions(channel.guild.default_role, view_channel=False)
                await channel.set_permissions(role, view_channel=True)
        except:
            embed = discord.Embed(title="Ошибка", description=f"Либо бот был приглашён, либо произошла ошибка при создании канала на сервере с ID ``{channel.guild.id}``\n``{channel.guild.owner_id}``\n<@{channel.guild.owner_id}>", color=discord.Color.red())
            guild = self.client.get_guild(995048257447280770)
            channel = guild.get_channel(999356269137764383)
            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error: discord.ext.commands.CommandError) -> None:
        if isinstance(error, discord.ext.commands.MissingPermissions):
            embed = discord.Embed(title=f"Произошла критическая ошибка", description=f"У вас нет прав на использование данной команды.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)
        else:
            if isinstance(error, discord.errors.Forbidden):
                try:
                    embed = discord.Embed(title="Произошла критическая ошибка", description=f"У меня нет прав на данное действие.", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Произошла критическая ошибка", description=f"Во время какой-то операции на сервере пользователя <@{ctx.guild.owner_id}> произошла ошибка! У меня недостаточно прав на изменение прав участника или каналов.", color=discord.Color.red())
                    guild = self.client.get_guild(995048257447280770)
                    channel = guild.get_channel(999356269137764383)
                    await channel.send(embed=embed)
                except:
                    embed = discord.Embed(title="Произошла критическая ошибка", description=f"Во время какой-то операции на сервере пользователя <@{ctx.guild.owner_id}> произошла ошибка! У меня недостаточно прав на изменение прав участника или каналов.", color=discord.Color.red())
                    guild = self.client.get_guild(995048257447280770)
                    channel = guild.get_channel(999356269137764383)
                    await channel.send(embed=embed)
            else:
                try:
                    embed = discord.Embed(title=f"Произошла критическая ошибка", description=f"Произошла неизвестная ошибка! Сообщите о ней разработчику <@553960665581355009> !\nЛог ошибки:\n\n``{error}``", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Ошибка", description=f"Во время какой-то операции на сервере пользователя <@{ctx.guild.owner_id}> произошла ошибка!\n``{error}``", color=discord.Color.red())
                    guild = self.client.get_guild(995048257447280770)
                    channel = guild.get_channel(999356269137764383)
                    await channel.send(embed=embed)
                except:
                    embed = discord.Embed(title="Ошибка", description=f"Во время какой-то операции на сервере пользователя <@{ctx.guild.owner_id}> произошла ошибка!\n``{error}``", color=discord.Color.red())
                    guild = self.client.get_guild(995048257447280770)
                    channel = guild.get_channel(999356269137764383)
                    await channel.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Events(client))