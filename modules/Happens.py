import discord
import aiohttp
import os
import shutil

from discord.ext import commands
from discord import app_commands
from colorama import init, Fore
from func import *


init(autoreset=True)


class Happens(commands.Cog, name='Happens'):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        print(Fore.BLUE + '[' + Fore.RED + ' ЛОГИ ' + Fore.BLUE + ']' + Fore.GREEN + f' Модуль развлечений был успешно подключен и успешно работает!')


    @commands.hybrid_command(description='Задать вопрос Бену')
    @app_commands.rename(que='question')
    @app_commands.describe(que='Ваш вопрос (используйте в конце знак ?)')
    @commands.guild_only()
    async def ben(self, ctx, que: str):
        if '?' in que:
            qben = random.randint(0, 3)
            if qben == 0:
                embed = discord.Embed(title=f"Вы спросили Бена!", description="Бен ответил вам:", color=0x05fa2e)
                embed.add_field(name="Ваш вопрос был:", value=f"{que}", inline=True)
                embed.add_field(name="Ответ Бена был:", value=f"Yes | Да", inline=True)
                embed.set_image(url="https://c.tenor.com/R_itimARcLAAAAAd/talking-ben-yes.gif")
                embed.set_footer(text=f"Talking Ben | Говорящий Бен")
                await ctx.send(embed=embed)
            else:
                if qben == 1:
                    embed = discord.Embed(title="Вы спросили Бена!", description="Бен ответил вам:", color=0x05fa2e)
                    embed.add_field(name="Ваш вопрос был:", value=f"{que}", inline=True)
                    embed.add_field(name="Ответ Бена был:", value=f"No | Нет", inline=True)
                    embed.set_image(url="https://c.tenor.com/3ZLujiiPc4YAAAAC/talking-ben-no.gif")
                    embed.set_footer(text=f"Talking Ben | Говорящий Бен")
                    await ctx.send(embed=embed)
                else:
                    if qben == 2:
                        embed = discord.Embed(title="Вы спросили Бена!", description="Бен ответил вам:", color=0x05fa2e)
                        embed.add_field(name="Ваш вопрос был:", value=f"{que}", inline=True)
                        embed.add_field(name="Ответ Бена был:", value=f"Ugh | УЭ (Фу)", inline=True)
                        embed.set_image(url="https://c.tenor.com/Vh28wO-oya4AAAAC/ugh-ben.gif")
                        embed.set_footer(text=f"Talking Ben | Говорящий Бен")
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title="Вы спросили Бена!", description="Бен ответил вам:", color=0x05fa2e)
                        embed.add_field(name="Ваш вопрос был:", value=f"{que}", inline=True)
                        embed.add_field(name="Ответ Бена был:", value=f"Ho ho ho | Ха ха ха! (Хо Хо Хо) (смех)", inline=True)
                        embed.set_image(url="https://c.tenor.com/ysXC0XFeXycAAAAC/talking-ben-ben.gif")
                        embed.set_footer(text=f"Talking Ben | Говорящий Бен")
                        await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Ошибка', description='В Вашем вопросе должен присутствовать знак вопроса!', color=discord.Color.red())
            await ctx.send(embed=embed)


# @slash.command(name='activity',
#                description='Использование активностей в голосовых каналах')
# @app_commands.describe(
#     choice='Выберите, какую активность вы хотите использовать')
# @app_commands.choices(choice=[
#     app_commands.Choice(name='YouTube Together', value=1),
#     app_commands.Choice(name='Word Snacks', value=2),
#     app_commands.Choice(
#         name='Chess In The Park (требуется буст сервера первого уровня)',
#         value=3),
#     app_commands.Choice(name='Doodle Crew', value=4),
#     app_commands.Choice(
#         name='Poker Night (требуется буст сервера первого уровня)', value=5),
#     app_commands.Choice(name='Sketch Heads', value=6),
#     app_commands.Choice(name='Ask Away', value=7)
# ])
# @app_commands.describe(channel='Канал, в котором будет действовать активность')
# @app_commands.guild_only()
# async def ractivitity(interaction: discord.Interaction,
#                       choice: app_commands.Choice[int],
#                       channel: discord.VoiceChannel):
#     premium = check_premium(f"{interaction.guild.id}",
#                             f"{interaction.guild.owner_id}")
#     if premium["status"] == "true":
#         if choice.value == 1:
#             embed = discord.Embed(
#                 title="Ожидайте",
#                 description=
#                 "Я начинаю создавать для вас активность YouTube Together! Это может занять время, ожидайте пригласительную ссылку...",
#                 color=discord.Color.blue())
#             await interaction.response.send_message(embed=embed)
#             data = {
#                 "max_age": 86400,
#                 "max_uses": 0,
#                 "target_application_id": appids['youtube'],
#                 "target_type": 2,
#                 "temporary": False,
#                 "validate": None
#             }
#             headers = {
#                 "Authorization": f"Bot {bot['token']}",
#                 "Content-Type": "application/json"
#             }
#             response = requests.post(
#                 f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                 data=json.dumps(data),
#                 headers=headers)
#             link = json.loads(response.content)
#             embed = discord.Embed(
#                 title="Готово",
#                 description=
#                 f"Я успешно сделал для вас активность YouTube Together в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                 color=discord.Color.green())
#             await interaction.edit_original_response(embed=embed)
#         else:
#             if choice.value == 2:
#                 embed = discord.Embed(
#                     title="Ожидайте",
#                     description=
#                     "Я начинаю создавать для вас активность Word Snacks! Это может занять время, ожидайте пригласительную ссылку...",
#                     color=discord.Color.blue())
#                 await interaction.response.send_message(embed=embed)
#                 data = {
#                     "max_age": 86400,
#                     "max_uses": 0,
#                     "target_application_id": appids['wordsnacks'],
#                     "target_type": 2,
#                     "temporary": False,
#                     "validate": None
#                 }
#                 headers = {
#                     "Authorization": f"Bot {bot['token']}",
#                     "Content-Type": "application/json"
#                 }
#                 response = requests.post(
#                     f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                     data=json.dumps(data),
#                     headers=headers)
#                 link = json.loads(response.content)
#                 embed = discord.Embed(
#                     title="Готово",
#                     description=
#                     f"Я успешно сделал для вас активность Word Snacks в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                     color=discord.Color.green())
#                 await interaction.edit_original_response(embed=embed)
#             else:
#                 if choice.value == 3:
#                     embed = discord.Embed(
#                         title="Ожидайте",
#                         description=
#                         "Я начинаю создавать для вас активность Chess! Это может занять время, ожидайте пригласительную ссылку...",
#                         color=discord.Color.blue())
#                     await interaction.response.send_message(embed=embed)
#                     data = {
#                         "max_age": 86400,
#                         "max_uses": 0,
#                         "target_application_id": appids['chess'],
#                         "target_type": 2,
#                         "temporary": False,
#                         "validate": None
#                     }
#                     headers = {
#                         "Authorization": f"Bot {bot['token']}",
#                         "Content-Type": "application/json"
#                     }
#                     response = requests.post(
#                         f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                         data=json.dumps(data),
#                         headers=headers)
#                     link = json.loads(response.content)
#                     embed = discord.Embed(
#                         title="Готово",
#                         description=
#                         f"Я успешно сделал для вас активность Chess в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                         color=discord.Color.green())
#                     await interaction.edit_original_response(embed=embed)
#                 else:
#                     if choice.value == 4:
#                         embed = discord.Embed(
#                             title="Ожидайте",
#                             description=
#                             "Я начинаю создавать для вас активность Doodle Crew! Это может занять время, ожидайте пригласительную ссылку...",
#                             color=discord.Color.blue())
#                         await interaction.response.send_message(embed=embed)
#                         data = {
#                             "max_age": 86400,
#                             "max_uses": 0,
#                             "target_application_id": appids['doodlecrew'],
#                             "target_type": 2,
#                             "temporary": False,
#                             "validate": None
#                         }
#                         headers = {
#                             "Authorization": f"Bot {bot['token']}",
#                             "Content-Type": "application/json"
#                         }
#                         response = requests.post(
#                             f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                             data=json.dumps(data),
#                             headers=headers)
#                         link = json.loads(response.content)
#                         embed = discord.Embed(
#                             title="Готово",
#                             description=
#                             f"Я успешно сделал для вас активность Doodle Crew в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                             color=discord.Color.green())
#                         await interaction.edit_original_response(embed=embed)
#                     else:
#                         if choice.value == 5:
#                             embed = discord.Embed(
#                                 title="Ожидайте",
#                                 description=
#                                 "Я начинаю создавать для вас активность Poker Night! Это может занять время, ожидайте пригласительную ссылку...",
#                                 color=discord.Color.blue())
#                             await interaction.response.send_message(embed=embed
#                                                                     )
#                             data = {
#                                 "max_age": 86400,
#                                 "max_uses": 0,
#                                 "target_application_id": appids['poker'],
#                                 "target_type": 2,
#                                 "temporary": False,
#                                 "validate": None
#                             }
#                             headers = {
#                                 "Authorization": f"Bot {bot['token']}",
#                                 "Content-Type": "application/json"
#                             }
#                             response = requests.post(
#                                 f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                                 data=json.dumps(data),
#                                 headers=headers)
#                             link = json.loads(response.content)
#                             embed = discord.Embed(
#                                 title="Готово",
#                                 description=
#                                 f"Я успешно сделал для вас активность Poker Night в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                                 color=discord.Color.green())
#                             await interaction.edit_original_response(
#                                 embed=embed)
#                         else:
#                             if choice.value == 6:
#                                 embed = discord.Embed(
#                                     title="Ожидайте",
#                                     description=
#                                     "Я начинаю создавать для вас активность Sketch Heads! Это может занять время, ожидайте пригласительную ссылку...",
#                                     color=discord.Color.blue())
#                                 await interaction.response.send_message(
#                                     embed=embed)
#                                 data = {
#                                     "max_age": 86400,
#                                     "max_uses": 0,
#                                     "target_application_id":
#                                     appids['sketchheads'],
#                                     "target_type": 2,
#                                     "temporary": False,
#                                     "validate": None
#                                 }
#                                 headers = {
#                                     "Authorization": f"Bot {bot['token']}",
#                                     "Content-Type": "application/json"
#                                 }
#                                 response = requests.post(
#                                     f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                                     data=json.dumps(data),
#                                     headers=headers)
#                                 link = json.loads(response.content)
#                                 embed = discord.Embed(
#                                     title="Готово",
#                                     description=
#                                     f"Я успешно сделал для вас активность Sketch Heads в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                                     color=discord.Color.green())
#                                 await interaction.edit_original_response(
#                                     embed=embed)
#                            else:
#                                embed = discord.Embed(
#                                    title="Ожидайте",
#                                    description=
#                                    "Я начинаю создавать для вас активность Ask Away! Это может занять время, ожидайте пригласительную ссылку...",
#                                    color=discord.Color.blue())
#                                await interaction.response.send_message(
#                                    embed=embed)
#                                data = {
#                                    "max_age": 86400,
#                                    "max_uses": 0,
#                                    "target_application_id": appids['askaway'],
#                                    "target_type": 2,
#                                    "temporary": False,
#                                    "validate": None
#                                }
#                                headers = {
#                                    "Authorization": f"Bot {bot['token']}",
#                                    "Content-Type": "application/json"
#                                }
#                                response = requests.post(
#                                    f"https://discord.com/api/v8/channels/{channel.id}/invites",
#                                    data=json.dumps(data),
#                                    headers=headers)
#                                link = json.loads(response.content)
#                                embed = discord.Embed(
#                                    title="Готово",
#                                    description=
#                                    f"Я успешно сделал для вас активность Ask Away в канале <#{channel.id}>. Вот пригласительная ссылка: https://discord.com/invite/{link['code']}",
#                                    color=discord.Color.green())
#                                await interaction.edit_original_response(
#                                    embed=embed)
#    else:
#        embed = discord.Embed(
#            title="Ошибка",
#            description=
#            "Для вашего сервера отсутствуют подписка **Splash! PREMIUM**! Купите подписку для того, чтобы иметь доступ к новым возможностям.\nУ кого можно купить подписку? У нашего разработчика!\n<@553960665581355009>",
#            color=discord.Color.red())
#        await interaction.response.send_message(embed=embed)
# appids = {
#     "youtube": "880218394199220334",
#     "wordsnacks": "879863976006127627",
#     "chess": "832012774040141894",
#     "doodlecrew": "878067389634314250",
#     "poker": "755827207812677713",
#     "sketchheads": "902271654783242291",
#     "askaway": "976052223358406656"
# }


async def setup(client: commands.Bot):
    await client.add_cog(Happens(client))