import os
import shutil
import discord
import datetime, time

from discord.ext import commands
from discord import app_commands
from func import load_json, write_json
from func import request, check_premium, check_bot_owner
from colorama import init, Fore


init(autoreset=True)


class create_announcement(discord.ui.Modal, title='Создание объявления/новости'):

    mtsend = discord.ui.TextInput(
        label='Ваша новость или объявление',
        style=discord.TextStyle.long,
        placeholder='Пишите здесь!',
        required=True,
        max_length=2000,
    )

    urltsend = discord.ui.TextInput(
        label='Ссылка на фото или GIF, если требуется',
        style=discord.TextStyle.short,
        placeholder='Пишите здесь!',
        required=False,
        max_length=1000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if '.png' in self.children[1].value or '.gif' in self.children[
            1].value or '.jpg' in self.children[1].value or '.jpeg' in self.children[
                1].value or '.bmp' in self.children[
                    1].value or 'http://' in self.children[
                        1].value or 'https://' in self.children[
                            1].value or '.mp4' in self.children[
                                1].value or '.avi' in self.children[
                                    1].value or '.mpeg' in self.children[
                                        1].value or '.webp' in self.children[
                                            1].value or '.webm' in self.children[
                                                1].value:
            if len(self.children[0].value) < 20:
                embed = discord.Embed(
                    title='Ошибка',
                    description=
                    'Ваша новость не может содержать менее 20-ти символов!',
                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed)
            else:
                config = load_json(
                    f"guilds/{interaction.guild.id}/config.json")
                if config['ancolor'] == '1':
                    embed = discord.Embed(
                        title='Объявление | Новость',
                        description=f'{self.children[0].value}',
                        color=discord.Color.blue())
                else:
                    if config['ancolor'] == '2':
                        embed = discord.Embed(
                            title='Объявление | Новость',
                            description=f'{self.children[0].value}',
                            color=discord.Color.purple())
                    else:
                        if config['ancolor'] == '3':
                            embed = discord.Embed(
                                title='Объявление | Новость',
                                description=f'{self.children[0].value}',
                                color=discord.Color.green())
                        else:
                            embed = discord.Embed(
                                title='Объявление | Новость',
                                description=f'{self.children[0].value}',
                                color=discord.Color.red())
            embed.set_image(url=self.children[1].value)
        else:
            if len(self.children[0].value) < 20:
                embed = discord.Embed(
                    title='Ошибка',
                    description=
                    'Ваша новость не может содержать менее 20-ти символов!',
                    color=discord.Color.red())
                await interaction.response.send_message(embed=embed)
            else:
                config = load_json(
                    f"guilds/{interaction.guild.id}/config.json")
                if config['ancolor'] == '1':
                    embed = discord.Embed(
                        title='Объявление | Новость',
                        description=f'{self.children[0].value}',
                        color=discord.Color.blue())
                else:
                    if config['ancolor'] == '2':
                        embed = discord.Embed(
                            title='Объявление | Новость',
                            description=f'{self.children[0].value}',
                            color=discord.Color.purple())
                    else:
                        if config['ancolor'] == '3':
                            embed = discord.Embed(
                                title='Объявление | Новость',
                                description=f'{self.children[0].value}',
                                color=discord.Color.green())
                        else:
                            embed = discord.Embed(
                                title='Объявление | Новость',
                                description=f'{self.children[0].value}',
                                color=discord.Color.red())
                channel = interaction.guild.get_channel(int(config['anchannel']))
                await channel.send(embed=embed)
                embed = discord.Embed(
                    title='Готово',
                    description=
                    f"Ваша новость/объявление было успешно отправлено на канал <#{config['anchannel']}>!",
                    color=discord.Color.green())
                await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        embed = discord.Embed(
            title="Ошибка",
            description=
            f"Во время какой-то операции на сервере пользователя <@{interaction.guild.owner_id}> произошла ошибка!\n``{error}``",
            color=discord.Color.red())
        guild = self.client.get_guild(995048257447280770)
        channel = guild.get_channel(999356269137764383)
        await channel.send(embed=embed)


class help_cmd(discord.ui.Select):

    def __init__(self):
        options = [
            discord.SelectOption(
                label='Верификация',
                description='Настройка конфигурации, проверка людей на робота',
                emoji='🔐'),
            discord.SelectOption(
                label='Модерация',
                description='Изменение никнеймов, блокировка, мут и т.д.',
                emoji='👮'),
            discord.SelectOption(label='Развлечения',
                                description='Куча весёлостей и развлечений',
                                emoji='😀'),
            discord.SelectOption(
                label='Конкурсы/раздачи',
                description='Команды для создания конкурсов или раздач',
                emoji='🎉'),
            discord.SelectOption(
                label='Музыка',
                description='Теперь, вы сможете слушать музыку в боте!',
                emoji='🎧'),
            discord.SelectOption(label='Полезное',
                                description='Просто полезные команды',
                                emoji='♻'),
            discord.SelectOption(label='Запретная зона',
                                description='Команды разработчика',
                                emoji='🛠️'),
        ]
        super().__init__(placeholder='Выберите раздел',
                        min_values=1,
                        max_values=1,
                        options=options)

    async def callback(self, interaction: discord.Interaction):
        if "Верификация" in self.values:
            embed = discord.Embed(color=discord.Color.yellow())
            embed.add_field(name='Командный справочник | Верификация', value=f'``/config verify`` - верифицировать пользователя вручную\n``/config send-msg`` - отправить сообщение о верификации в предназначенный для этого канал (его ID указан в файле конфигурации)\n``/config setup`` - настраивает конфигурацию сервера для верификации\n``/config save`` - сохраняет файл конфигурации сервера\n``/config load`` - загружает файл конфигурации сервера\n``/config`` - выдаёт информацию о конфигурации сервера для верификации\n``/config ignorebots`` - игнорировать ботов которые входят на сервер во время включенной блокировки сервера\n``/config lockserver`` - блокирует сервер от нововходящих пользователей на сервер')
            await interaction.response.edit_message(embed=embed)
        if "Модерация" in self.values:
            embed = discord.Embed(color=discord.Color.blurple())
            embed.add_field(name='Командный справочник | Модерация', value=f'``/moder chat-filtration`` - включает фильтрацию чата с наказанием\n``/moder ban`` - банит пользователя\n``/moder unban`` - разбанивает пользователя\n``/moder kick`` - выгоняет пользователя с сервера\n``/moder mute`` - отправляет в мьют пользователя\n``/moder unmute`` - размьючивает пользователя\n``/moder nickname`` - изменяет никнейм пользователю\n``/moder role`` - изменяет роли участнику\n``/moder clear`` - чистит определённое кол-во сообщений в канале\n``/moder warn`` - выдать предупреждение пользователю\n``/moder unwarn`` - убрать варны пользователю')
            await interaction.response.edit_message(embed=embed)
        if "Развлечения" in self.values:
            embed = discord.Embed(color=discord.Color.purple())
            embed.add_field(name='Командный справочник | Развлечения', value=f'~~``/activity`` - создать активность в определённый голосовой канал (доступно только с ПК-версии)~~\n``/ben`` - задайте вопрос Бену!')
            await interaction.response.edit_message(embed=embed)
        if "Конкурсы/раздачи" in self.values:
            embed = discord.Embed(color=discord.Color.blue())
            embed.add_field(name='Командный справочник | Конкурсы/раздачи', value=f'~~``/gcreate`` - создать новую раздачу/конкурс~~')
            await interaction.response.edit_message(embed=embed)
        if "Музыка" in self.values:
            embed = discord.Embed(color=discord.Color.orange())
            embed.add_field(name='Командный справочник | Музыка', value=f'``/music play`` - играет музыку по вашему запросу или по ссылке на YouTube-видео\n``/music stop`` - останавливает музыку\n``/music volume`` - изменяет громкость проигрываемой музыки')
            await interaction.response.edit_message(embed=embed)
        if "Полезное" in self.values:
            embed = discord.Embed(color=discord.Color.green())
            embed.add_field(name='Командный справочник | Полезное', value=f'``/help`` - выводит справку по всем командам с разделами\n``/create invite`` - создаёт ссылку-приглашение на сервер в определённый канал с определённым количеством использований\n``/bot`` - показывает всю информацию о боте\n``/server`` - показывает информацию о сервере\n``/premium`` - показывает информацию о подписке **Splash! PREMIUM**\n~~``/create announcement`` - создать новость либо объявление в определённый канал~~\n``/create password`` - генерирует пароль и отправляет его вам в личные сообщения\n``/create forum`` - создать канал-форум на сервере\n``/create qr-code`` - создать QR-код, в котором будет находится ваш текст')
            await interaction.response.edit_message(embed=embed)
        if "Команды разработчика (обычно отключены)" in self.values:
            embed = discord.Embed(color=discord.Color.red())
            embed.add_field(name='Командный справочник | Команды разработчика',value=f'~~``/dev get-user`` - поиск пользователя по его ID~~\n~~``/dev blacklist`` - настройка чёрного списка гильдий~~\n~~``/dev guilds`` - список всех гильдий, на который присутствует бот~~\n~~``/dev pm`` - управление премиумом~~')
            await interaction.response.edit_message(embed=embed)


class design_help_cmd(discord.ui.View):

    def __init__(self):
        super().__init__()
        self.add_item(help_cmd())


class Basic(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Базовый модуль (полезных и прочих команд) был успешно подключен и успешно работает!')


    @commands.hybrid_command(name='help', description='Справочник по всем командам')
    @commands.guild_only()
    async def help(self, ctx):
        view = design_help_cmd()
        embed = discord.Embed(title=f'Командный справочник', description='Пожалуйста, выберите раздел помощи, который вам подойдёт больше всего\n\n**ВНИМАНИЕ!!!**\nВсе команды начинаются с префиксов sp!, sp. и sp?,  но так же действуют slash-команды!', color=discord.Color.blue())
        await ctx.send(embed=embed, view=view)


#    @commands.hybrid_group(fallback='announcement', description='Создать объявление или новость')
#    @commands.has_permissions(manage_guild=True)
#    @commands.guild_only()
#    @app_commands.describe(channel='Канал, в который будет прислано объявление')
#    async def create(self, ctx, channel: discord.TextChannel):
#        embed = discord.Embed(title='Выберите пожалуйста цвет для вашей новости/объявления', color=discord.Color.blurple())
#        await ctx.send(embed=embed)
#        config = load_json(f"guilds/{ctx.guild.id}/config.json")
#        config['anchannel'] = str(channel.id)
#        write_json(f"guilds/{ctx.guild.id}/config.json", config)


    @commands.hybrid_group(fallback='password', description='Генерирует пароль определённой длинной (указанной вами) и отправляет его в личные сообщения')
    @app_commands.describe(length='Длинная пароль (до 72 символов)')
    async def create(self, ctx, length: int):
        if length > 72:
            if await check_premium(ctx.guild.id, ctx.guild.owner_id):
                embed = discord.Embed(title='Готово', description='Пароль сгенерирован! Я отправляю вам его в личные сообщения...\n\nПредупреждение: Если бот не прислал код, значит возможно у вас закрыты личные сообщения!', color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title='Сгенерированный код', description=f'Я сгенерировал пароль длинной в {length} символ(-ов, -а)!\nПароль: || {generate_password(length)} ||', color=discord.Color.blue())
                await ctx.author.send(embed=embed)
            else:
                embed = discord.Embed(title='Ошибка',description='Указанная длинна пароля не может превышать 72-ух символов!\n**Т-с-с...**\nКупите подписку Splash! PREMIUM всего-лишь за 50₽ в честь открытия Splash! v2.0, чтобы снять ограничения с команд!', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            if length < 8:
                if await check_premium(ctx.guild.id, ctx.guild.owner_id):
                    embed = discord.Embed(title='Готово', description='Пароль сгенерирован! Я отправляю вам его в личные сообщения...\n\nПредупреждение: Если бот не прислал код, значит возможно у вас закрыты личные сообщения!', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title='Сгенерированный код', description=f'Я сгенерировал пароль длинной в {length} символ(-ов, -а)!\nПароль: || {generate_password(length)} ||', color=discord.Color.blue())
                    await ctx.author.send(embed=embed)
                else:
                    embed = discord.Embed(title='Ошибка', description=f'Указанная длинна пароля не может быть менее 8-ми символов!\n**Т-с-с...**\nКупите подписку Splash! PREMIUM всего-лишь за 50₽ в честь открытия Splash! v2.0, чтобы снять ограничения с команд!', color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title='Готово', description='Пароль сгенерирован! Я отправляю вам его в личные сообщения...\n\nПредупреждение: Если бот не прислал код, значит возможно у вас закрыты личные сообщения!', color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title='Сгенерированный код', description=f'Я сгенерировал пароль длинной в {length} символ(-ов, -а)!\nПароль: || {generate_password(length)} ||', color=discord.Color.blue())
                await ctx.author.send(embed=embed)


    @commands.hybrid_command(description='Полная информация о сервере')
    @commands.guild_only()
    async def server(self, ctx):
        if await check_premium(ctx.guild.id, ctx.guild.owner_id):
            premium = "Подписка Splash! PREMIUM преобретена на данном сервере :white_check_mark: "
        else:
            premium = "Подписка Splash! PREMIUM не преобретена на данном сервере :x: "
        members = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))), len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        embed = discord.Embed(title=f"{ctx.guild.name} Справка по серверу", description="Информация о сервере", color=discord.Colour.blue())
        embed.add_field(name='🆔 ID сервера', value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name='🖥 ID шарда данного сервера', value=f"Шард №{ctx.guild.shard_id + 1}", inline=False)
        embed.add_field(name="💡 Статусы пользователей", value=f"В сети: {statuses[0]}\nНеактивны: {statuses[1]}\nНе беспокоить: {statuses[2]}\nОффлайн: {statuses[3]}", inline=False)
        embed.add_field(name="👥 Участники", value=f"Всех: {len(ctx.guild.members)} | Людей: {members} | Ботов: {bots}", inline=False)
        embed.add_field(name='📆 Дата создания сервера', value=ctx.guild.created_at.strftime("%b %d %Y"), inline=False)
        embed.add_field(name='👑 Владелец', value=f"<@{ctx.guild.owner_id}>", inline=False)
        embed.add_field(name='💬 Каналы', value=f'{len(ctx.guild.text_channels)} Текстовый(-ых) | {len(ctx.guild.voice_channels)} Голосовой(-ых)', inline=False)
        embed.add_field(name='🌎 Регион', value=f'{ctx.guild.preferred_locale}', inline=False)
        embed.add_field(name='💸 Подписка Splash! PREMIUM', value=f'{premium}', inline=False)
        embed.set_thumbnail(url=ctx.guild.icon)
        await ctx.send(embed=embed)


    @create.command(name='qr-code', description='Создать свой собственный QR-код')
    @app_commands.describe(data='Данные, которые будут в QR-коде')
    @commands.guild_only()
    async def qrcode(self, ctx, data: str):
        id = random.randint(00000000000, 99999999999)
        myqrcode = qrcode.make(data)
        myqrcode.save(f"tmp/{idi}.png")
        embed = discord.Embed(title='Готово', description=f'Ваш QR-код был успешно создан и сгенерирован по данным: {data}', color=discord.Color.green())
        await ctx.send(embed=embed)
        await ctx.channel.send(file=discord.File(f"tmp/{idi}.png", filename=f"tmp/{idi}.png"))
        os.remove(f"tmp/{idi}.png")


    @create.command(description='Создать ссылку-приглашение на сервер')
    @app_commands.describe(channel='Канал, в который будет направлен пользователь после использования приглашения')
    @app_commands.describe(max_uses='Кол-во максимальных использований пригласительной ссылки')
    async def invite(self, ctx, channel: discord.TextChannel, max_uses: int = 0):
        if check_bot_owner(int(ctx.author.id)):
            channel = await ctx.guild.fetch_channel(int(993059800353095770))
            inv = await channel.create_invite(max_uses=max_uses, max_age=0)
            embed = discord.Embed(title='Готово', description=f'Ваша ссылку-приглашение на данный сервер в канал <#{channel.id}> успешно создана!\n{inv.url}', color=discord.Color.green())
            await ctx.send(embed=embed)


    @create.command(description='Создать форум на сервере')
    @commands.has_permissions(manage_channels=True)
    @app_commands.describe(name='Название форума')
    @app_commands.describe(category='Категория, в которой будет размещён форум')
    @app_commands.describe(position='Номер позиции, на которой будет стоять форум')
    async def forum(self, ctx, name: str, category: discord.CategoryChannel = None, position: int = None):
        if category is None:
            if position is None:
                forum = await ctx.guild.create_forum(name=f'{name}')
            else:
                forum = await ctx.guild.create_forum(name=f'{name}', position=position)
        else:
            if position is None:
                forum = await ctx.guild.create_forum(name=f'{name}', category=category)
            else:
                forum = await ctx.guild.create_forum(name=f'{name}', category=category, position=position)
        inv = await forum.create_invite(max_uses=0, max_age=0)
        embed = discord.Embed(title='Готово', description=f'Форум под именем {name} успешно создан! Пригласительная ссылка:\n{inv.url}', color=discord.Color.green())
        await ctx.send(embed=embed)


    @commands.command()
    async def test(self, ctx):
        embed = discord.Embed(title='test')
        await ctx.send(embed=embed)


async def setup(client: commands.Bot):
    await client.add_cog(Basic(client))