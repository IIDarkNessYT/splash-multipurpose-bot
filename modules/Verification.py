import discord

from func import *
from colorama import init, Fore
from discord.ext import commands
from discord import app_commands
import random
import asyncio
import os
import shutil


init(autoreset=True)


class Verification(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Модуль верификации был успешно подключен и успешно работает!')


    @commands.hybrid_group(fallback='info', description='Информация о конфигурации сервера')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def config(self, ctx):
        config = load_json(f"guilds/{ctx.guild.id}/config.json")
        embed = discord.Embed(title=f"Конфигурация сервера {ctx.guild.name}", description=f"Прежде чем посмотреть конфигурацию, изучите знаки обозначения:\n``true`` - правда (включено)\n``false`` - ложь (выключено)\n``none`` - не настроено\n\n\n``Роль для выдачи`` - {config['role']}\n\n``Канал для логов`` - {config['logchannel']}\n\n``Канал для верификации`` - {config['channelcaptcha']}\n\n``Игнорировать ботов от блокировки сервера?`` - {config['ignorebots']}\n\n``Заблокирован ли сервер?`` - {config['lockserver']}\n\n``Канал, в которой присылаются оповещения о пришедших/ушедших пользователей с сервера`` - {config['comernoticechannel']}", color=discord.Color.green())
        await ctx.send(embed=embed)


    @config.command(name='send-msg', description='Отправить сообщение о проверке')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def send(self, ctx):
        guild_id = ctx.guild.id
        config = load_json(f"guilds/{guild_id}/config.json")
        if config['ignorebots'] == "none":
            embed = discord.Embed(title=f"Ошибка", description=f"Вы не указали, стоит ли мне игнорировать ботов от блокировки сервера, либо же нет!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if config['lockserver'] == "none":
                embed = discord.Embed(title=f"Ошибка", description=f"Вы ещё не активировали команду переключения блокировки сервера!", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                if config['channelcaptcha'] == "none":
                    embed = discord.Embed(title=f"Ошибка", description=f"Вы ещё не указали канал, в который будет отправлено сообщение о проверке!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    if config['logchannel'] == "none":
                        embed = discord.Embed(title=f"Ошибка", description=f"Вы ещё не указали канал, в который будут отсылаться логи (отчёты)!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                    else:
                        if config['role'] == "none":
                            embed = discord.Embed(title=f"Ошибка", description=f"Вы ещё не указали роль, которая будет выдана пользователю если он пройдёт проверку!", color=discord.Color.red())
                            await ctx.send(embed=embed)
                        else:
                            if config['text'] == "none":
                                embed = discord.Embed(title=f"Ошибка", description=f"Вы ещё не установили текст, который будет в сообщении о проверке!", color=discord.Color.red())
                                await ctx.send(embed=embed)
                            else:
                                embed = discord.Embed(title=f"Верификация", description=f"{config['text']}", color=discord.Colour.blue())
                                channel = ctx.guild.get_channel(int(config['channelcaptcha']))
                                await channel.send(embed=embed, view=create_captcha_code())
                                await ctx.send(f"Готово! Вы успешно настроили сообщение о проверке.")


    @config.command(description='Настроить конфигурацию сервера')
    @commands.has_permissions(manage_guild=True)
    @app_commands.describe(text='Текст, который будет отображён в сообщении верификации')
    @app_commands.describe(role='Роль, которая будет выдана после успешной проверки')
    @app_commands.describe(logchannel='Канал, в который будут отправляться логи')
    @app_commands.describe(verifychannel='Канал, в котором будет проходить верификация и отослано сообщение и проверке')
    @app_commands.describe(welcomechannel='Канал, в который будут присылаться сообщения о новых/ушедших с сервера участников')
    @commands.guild_only()
    async def setup(self, ctx, text: str, role: discord.Role, logchannel: discord.TextChannel, verifychannel: discord.TextChannel, welcomechannel: discord.TextChannel = None):
        config = load_json(f"guilds/{ctx.guild.id}/config.json")
        if await check_premium(ctx.guild.id, ctx.guild.owner_id):
            if len(text) > 300:
                await ctx.send(f"Вы не можете ставить текст сообщения более 300 символов! Купите подписку Splash! PREMIUM для того, чтобы увеличить кол-во символов в 2 раза (600 символов).")
            else:
                config['text'] = str(text)
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
        else:
            if len(text) > 600:
                await ctx.send(f"Вы не можете ставить текст сообщения более 600 символов!")
            else:
                config['text'] = str(text)
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
        config['role'] = str(role.id)
        write_json(f"guilds/{ctx.guild.id}/config.json", config)
        config['logchannel'] = str(logchannel.id)
        write_json(f"guilds/{ctx.guild.id}/config.json", config)
        config['channelcaptcha'] = str(verifychannel.id)
        write_json(f"guilds/{ctx.guild.id}/config.json", config)
        if welcomechannel is None:
            config['comernoticechannel'] = "false"
            write_json(f"guilds/{ctx.guild.id}/config.json", config)
            embed = discord.Embed(title='Готово', description=f"Вы настроили текст сообщения о проверке как:\n``{text}``\nРоль после успешной проверки: {role.mention}\nКанал для логов: <#{logchannel.id}>\nКанал где будет сообщение о проверке: <#{verifychannel.id}>\nКанал оповещений о пришедших/ушедших с сервера участниках: **ОТКЛЮЧЕН**\n\n**Не забудьте сохранить конфигурацию сервера, а так же отправить сообщение о верификации (используя команды)**", color=discord.Color.green())
        else:
            config['comernoticechannel'] = str(ncchannel.id)
            write_json(f"guilds/{ctx.guild.id}/config.json", config)
            embed = discord.Embed(title='Готово', description=f"Вы настроили текст сообщения о проверке как:\n``{text}``\nРоль после успешной проверки: {role.mention}\nКанал для логов: <#{logchannel.id}>\nКанал где будет сообщение о проверке: <#{verifychannel.id}>\nКанал оповещений о пришедших/ушедших с сервера участниках: <#{ncchannel.id}>\n\n**Не забудьте сохранить конфигурацию сервера, а так же отправить сообщение о верификации (используя команды)**", color=discord.Color.green())
        await ctx.send(embed=embed)
        role = ctx.guild.get_role(int(config['role']))
        for channel in ctx.guild.channels:
            await channel.set_permissions(ctx.guild.default_role, view_channel=False)
            await channel.set_permissions(role, view_channel=True)
        for member in ctx.guild.members:
            await member.add_roles(role)


    @config.command(description='Переключить игнорирование ботов при заблокированом сервере')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def ignorebots(self, ctx):
        config = load_json(f"guilds/{ctx.guild.id}/config.json")
        if config['ignorebots'] == "none":
            config['ignorebots'] = "true"
            write_json(f"guilds/{ctx.guild.id}/config.json", config)
            embed = discord.Embed(title='Готово', description=f"Теперь я буду игнорировать входящих на сервер ботов, пока сервер будет в блокировке!", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            if config['ignorebots'] == "true":
                config['ignorebots'] = "false"
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
                embed = discord.Embed(title='Готово', description=f"Теперь, я пока не буду игнорировать входящих на сервер ботов, пока сервер будет в блокировке!", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                config['ignorebots'] = "true"
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
                embed = discord.Embed(title='Готово', description="Теперь, я буду игнорировать входящих на сервер ботов, пока сервер будет в блокировке!", color=discord.Color.green())
                await ctx.send(embed=embed)


    @config.command(description='Переключить блокирование сервера от входящих на сервер участников')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def lockserver(self, ctx):
        config = load_json(f"guilds/{ctx.guild.id}/config.json")
        if config['lockserver'] == "none":
            config['lockserver'] = "false"
            write_json(f"guilds/{ctx.guild.id}/config.json", config)
            embed = discord.Embed(title='Готово', description="Команда активирована. Сервер сейчас разблокирован!", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            if config['lockserver'] == "true":
                config['lockserver'] = "false"
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
                embed = discord.Embed(title='Готово', description="Вы успешно разблокировали сервер. Теперь новые участники вновь смогут заходить на сервер!", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                config['lockserver'] = "true"
                write_json(f"guilds/{ctx.guild.id}/config.json", config)
                embed = discord.Embed(title='Готово', description="Вы успешно заблокировали сервер. Теперь новые участники не смогут сюда входить, пока Вы сами не разблокируете сервер!")
                await ctx.send(embed=embed)


    @config.command(description='Верифицировать пользователя вручную')
    @commands.has_permissions(kick_members=True)
    @app_commands.describe(member='Пользователь, которого вы хотите верифицировать')
    @commands.guild_only()
    async def verify(self, ctx, member: discord.Member):
        users = load_json(f"guilds/{ctx.guild.id}/users.json")
        config = load_json(f"guilds/{ctx.guild.id}/config.json")
        role = ctx.guild.get_role(int(config['role']))
        try:
            userstat = users[f'{member.id}']
        except:
            users[f'{member.id}'] = '123456789'
        else:
            pass
        if users[f'{member.id}'] == 'verified':
            embed = discord.Embed(title="Ошибка", description=f"Пользователь {member.mention} уже верифицирован!", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if users[f'{member.id}'] == 'notverified':
                users[f'{member.id}'] = 'verified'
                write_json(f"guilds/{ctx.guild.id}/users.json", users)
                await member.add_roles(role)
                embed = discord.Embed(title='Готово', description=f"Пользователь {member.mention} был успешно верифицирован!", color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Верификация вручную", description=f"Пользователь {ctx.author.mention} верифицировал пользователя {member.mention}!", color=discord.Color.green())
                channel = ctx.guild.get_channel(int(config['logchannel']))
                await channel.send(embed=embed)
            else:
                users[f'{member.id}'] = 'verified'
                write_json(f"guilds/{ctx.guild.id}/users.json", users)
                await member.add_roles(role)
                embed = discord.Embed(title='Готово', description=f"Пользователь {member.mention} был успешно верифицирован!", color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Верификация вручную", description=f"Пользователь {ctx.author.mention} верифицировал пользователя {member.mention}!", color=discord.Color.green())
                channel = ctx.guild.get_channel(int(config['logchannel']))
                await channel.send(embed=embed)


    @config.command(description='Создаёт резервную копию конфигурации сервера')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def save(self, ctx):
        try:
            os.mkdir(f"saves/{ctx.guild.id}")
            shutil.copy(f'guilds/{ctx.guild.id}/config.json', f'saves/{ctx.guild.id}/config.json')
            embed = discord.Embed(title='Готово', description="Конфигурация данного сервера успешно сохранена! :white_check_mark: ", color=discord.Color.green())
            await ctx.send(embed=embed)
        except:
            shutil.rmtree(f"saves/{ctx.guild.id}")
            os.mkdir(f"saves/{ctx.guild.id}")
            shutil.copy(f'guilds/{ctx.guild.id}/config.json', f'saves/{ctx.guild.id}/config.json')
            embed = discord.Embed(title='Готово', description="Конфигурация данного сервера успешно сохранена! :white_check_mark: ", color=discord.Color.green())
            await ctx.send(embed=embed)


    @config.command(description='Загрузить резервную копию конфигурации сервера')
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def load(self, ctx):
        try:
            shutil.copy(f'saves/{ctx.guild.id}/config.json', f'guilds/{ctx.guild.id}/config.json')
            embed = discord.Embed(title='Готово', description="Резервная копия данного сервера была успешно загружена!", color=discord.Color.green())
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title="Ошибка", description="Вы не создавали резервную копию данного сервера!", color=discord.Color.red())
            await ctx.send(embed=embed)



class verification_start(discord.ui.Modal, title='Верификация'):

    name = discord.ui.TextInput(label='Введите свой капча-код:', placeholder='123456789',max_length=9, min_length=9)

    async def on_submit(self, interaction: discord.Interaction):
        config = load_json(f"guilds/{interaction.guild.id}/config.json")
        role = interaction.guild.get_role(int(config['role']))
        inputcode = self.children[0].value
        codes = load_json(f"guilds/{interaction.guild.id}/users.json")
        try:
            userdata = codes[str(interaction.user.id)]
        except KeyError:
            codes[f'{interaction.user.id}'] = 'notverified'
            write_json(f'guilds/{interaction.guild.id}/users.json', codes)
            userdata = codes[str(interaction.user.id)]
        if inputcode == userdata:
            embed = discord.Embed(title=f"Уважаемый пользователь!", description=f"Спасибо, Вы успешно прошли проверку. Добро пожаловать, {interaction.user.name}!", color=discord.Color.green())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            codes = load_json(f"guilds/{interaction.guild.id}/users.json")
            status = 'verified'
            codes[str(interaction.user.id)] = str(status)
            write_json(f"guilds/{interaction.guild.id}/users.json", codes)
            await interaction.user.add_roles(role)
            embed = discord.Embed(title=f"{interaction.user.name} успешно прошёл прошёл проверку!", description=f"Пользователь успешно прошёл капчу и был допущен к серверу!", color=discord.Color.green())
            channel = interaction.guild.get_channel(int(config['logchannel']))
            await channel.send(embed=embed)
        else:
            try:
                embed = discord.Embed(title=f"Уважаемый пользователь!", description=f"Вы были кикнуты с сервера **{interaction.guild.name}**,\nтак как Вы неверно ввели свой капча-код!")
                await interaction.user.send(embed=embed)
            except:
                pass
            embed = discord.Embed(title=f"{interaction.user.name} был кикнут.", description=f"Пользователь был кикнут, так как не прошёл проверку на робота (индивидуальный капча-код бл введён не верно!)", color=discord.Color.red())
            channel = interaction.guild.get_channel(int(config['logchannel']))
            await channel.send(embed=embed)
            await interaction.user.kick(reason='Неверно введён индивидуальный капча-код')

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(title="Ошибка", description=f"Во время какой-то операции на сервере пользователя <@{interaction.guild.owner_id}> произошла ошибка!\n``{error}``", color=discord.Color.red())
        guild = client.get_guild(995048257447280770)
        channel = guild.get_channel(999356269137764383)
        await channel.send(embed=embed)


# Создание капча-кода
class create_captcha_code(discord.ui.View):

    def __init__(self) -> None:
        super().__init__(timeout=None)

    @discord.ui.button(label="Начать проверку", style=discord.ButtonStyle.primary, custom_id="verify", emoji="🤖")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            guild_id = interaction.guild.id
            codes = load_json(f"guilds/{guild_id}/users.json")
            config = load_json(f"guilds/{guild_id}/config.json")
            try:
                role = interaction.guild.get_role(int(config['role']))
                rname = role.name
            except:
                await interaction.response.send_message(f"Извините, но я не могу вас верифицировать. Настроенная роль либо отсутствуют, либо у меня недостаточно прав. Сообщите об этом владельцу сервера!", ephemeral=True)
            else:
                try:
                    test = codes[f'{interaction.user.id}']
                except KeyError:
                    codes[f'{interaction.user.id}'] = 'notverified'
                    write_json(f'guilds/{interaction.guild.id}/users.json', codes)
                if codes[f'{interaction.user.id}'] == 'leaved':
                    codes[f'{interaction.user.id}'] = 'notverified'
                    write_json(f'guilds/{interaction.guild.id}/users.json', codes)
                if codes[f'{interaction.user.id}'] == 'notverified':
                    status = random.randint(100000000, 999999999)
                    codes[str(interaction.user.id)] = str(status)
                    write_json(f"guilds/{guild_id}/users.json", codes)
                    embed = discord.Embed(title=f"Уважаемый пользователь!",description=f"Вы получили свой капча-код: ||{status}||\nВы должны его ввести прямо сейчас, нажав на кнопку ещё раз.\n\n**У вас всего 15 минут после присоединения к серверу!**", color=discord.Color.blurple())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    channel = interaction.guild.get_channel(int(config['logchannel']))
                    embed = discord.Embed(title=f"{interaction.user.name} получил свой капча-код", description="Данный пользователь получил свой индивидуальный капча-код!", color=discord.Color.purple())
                    await channel.send(embed=embed)
                else:
                    userdata = load_json(f"guilds/{guild_id}/users.json")
                    if userdata[f'{interaction.user.id}'] == "verified":
                        await interaction.response.send_message(f"Извините, но Вы уже верифицированны!", ephemeral=True)
                        await interaction.user.add_roles(role)
                    else:
                        await interaction.response.send_modal(verification_start())
                        channel = interaction.guild.get_channel(int(config['logchannel']))
                        embed = discord.Embed(title=f"{interaction.user.name} начал прохождение проверки", description="Данный пользователь начал прохождение проверки на робота!", color=discord.Color.blue())
                        await channel.send(embed=embed)
        except Exception as e:
            print(e)
            embed = discord.Embed(title='Ошибка', description='Возможно, у меня нет прав, либо вас нет в списке записанных пользователей! Перезайдите на сервер.', color=discord.Color.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(client: commands.Bot):
    await client.add_cog(Verification(client))