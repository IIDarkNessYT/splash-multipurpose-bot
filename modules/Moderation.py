import discord
import os
import shutil

from func import *
from discord.ext import commands
from discord import app_commands
from colorama import init, Fore

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.hybrid_group(fallback='chat-filter', description='Управление фильтрацией чата')
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def moder(self, ctx):
        cfg = load_json(f"guilds/{ctx.guild.id}/config.json")
        try:
            stat = cfg["chat-filter"]
        except KeyError:
            cfg["chat-filter"] = "on"
            write_json(f"guilds/{ctx.guild.id}/config.json", cfg)
            embed = discord.Embed(
                title='Готово',
                description=
                'Вы успешно включили фильтрацию чата!\nТеперь бот будет удалять плохие слова и оскорбления по мере возможности.',
                color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            if cfg["chat-filter"] == "off":
                cfg["chat-filter"] = "on"
                write_json(f"guilds/{ctx.guild.id}/config.json", cfg)
                embed = discord.Embed(
                    title='Готово',
                    description=
                    'Вы успешно включили фильтрацию чата!\nТеперь бот будет удалять плохие слова и оскорбления по мере возможности.',
                    color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                cfg["chat-filter"] = "off"
                write_json(f"guilds/{ctx.guild.id}/config.json", cfg)
                embed = discord.Embed(
                    title='Готово',
                    description=
                    'Вы успешно выключили фильтрацию чата!\nТеперь бот будет игнорировать плохие слова и оскорбления.',
                    color=discord.Color.orange())
                await ctx.send(embed=embed)


    @moder.command(description='Выдать предупреждение участнику')
    @app_commands.describe(member='Пользователь, которому вы хотите выдать предупрежение')
    @app_commands.describe(reason='Причина, по которой вы выдадите предупрежение')
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, reason: str):
        warns = load_json(f"guilds/{ctx.guild.id}/warns.json")
        if member and member.top_role.position >= ctx.author.top_role.position:
            embed = discord.Embed(
                title="Ошибка",
                description=
                "У вас нет прав на использование данной команды над данным пользователем.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            try:
                test = warns[f'{member.id}']
            except KeyError:
                warns[f'{member.id}'] = 0
                write_json(f"guilds/{ctx.guild.id}/warns.json", warns)
            warns[f'{member.id}'] = warns[f'{member.id}'] + 1
            write_json(f"guilds/{ctx.guild.id}/warns.json", warns)
            if warns[f'{member.id}'] == 3:
                try:
                    embed = discord.Embed(
                        title='Уважаемый пользователь!',
                        description=
                        f'Вы получили предупреждение на сервере **{ctx.guild.name}** администратором **{ctx.author.name}** с наказанием: Мут на 5 минут. Причина: ``{reason}``\n\nУ вас предупреждений: ``{warns[f"{member.id}"]} / 3``\n',
                        color=discord.Color.red())
                    await member.send(embed=embed)
                except:
                    test = 'test'
                await member.timeout(
                    datetime.timedelta(days=1),
                    reason=
                    f'Выдано предупреждение администратором {ctx.author.name} (3/3)'
                )
                embed = discord.Embed(
                    title='Готово',
                    description=
                    f'Предупреждение было успешно выдано пользователю {member.mention} по причине: "{reason}" ( 3/3, мут на 1 день )',
                    color=discord.Color.purple())
                await ctx.send(embed=embed)
                warns[f'{member.id}'] = 0
                write_json(f"guilds/{ctx.guild.id}/warns.json", warns)
            else:
                try:
                    embed = discord.Embed(
                        title='Уважаемый пользователь!',
                        description=
                        f'Вы получили предупреждение на сервере **{ctx.guild.name}** администратором **{ctx.author.name}** без наказания. Причина: ``{reason}``\n\nУ вас предупреждений: ``{warns[f"{member.id}"]} / 3``',
                        color=discord.Color.red())
                    await member.send(embed=embed)
                except:
                    test = 'test'
                embed = discord.Embed(
                    title='Готово',
                    description=
                    f'Предупреждение было успешно выдано пользователю {member.mention} по причине: "{reason}" ( {warns[f"{member.id}"]}/3 )\nБез наказания',
                    color=discord.Color.green())
                await ctx.send(embed=embed)


    @moder.command(description='Снять предупрежение с пользователя')
    @app_commands.describe(member='Пользователь, с которого нужно снять предупрежение')
    @commands.has_permissions(moderate_members=True)
    @commands.guild_only()
    async def unwarn(self, ctx, member: discord.Member):
        warns = load_json(f"guilds/{ctx.guild.id}/warns.json")
        if member and member.top_role.position >= ctx.author.top_role.position:
            embed = discord.Embed(
                title="Ошибка",
                description=
                "У вас нет прав на использование данной команды над данным пользователем.",
                color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            try:
                test = warns[f'{member.id}']
            except KeyError:
                warns[f'{member.id}'] = 0
                write_json(f"guilds/{ctx.guild.id}/warns.json", warns)
            else:
                if warns[f'{member.id}'] == 0:
                    embed = discord.Embed(
                        title='Ошибка',
                        description=
                        'У данного пользователя нет выданных предупреждений!',
                        color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    warns[f'{member.id}'] = warns[f'{member.id}'] - 1
                    write_json(f"guilds/{ctx.guild.id}/warns.json", warns)
                    embed = discord.Embed(
                        title='Готово',
                        description=
                        f'Вы успешно сняли одно предупреждение с пользователя {member.mention} ! ( {warns[f"{member.id}"]}/3 )',
                        color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(
                        title='Уважаемый пользователь!',
                        description=
                        f'На сервере {ctx.guild.name} администратор {ctx.user.name} снял с вас одно предупреждение! ( {warns[f"{member.id}"]}/3 )',
                        color=discord.Color.green())
                    await member.send(embed=embed)


    @moder.command(description="Выгнать пользователя с сервера")
    @app_commands.describe(member='Пользователь, которого вы хотите кикнуть')
    @app_commands.describe(reason='Причина кика пользователя')
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, reason: str = None):
        if member and member.top_role.position >= ctx.author.top_role.position:
            if check_bot_owner(ctx.author.id) is True:
                guild = ctx.guild
                if reason is None:
                    embed = discord.Embed(title=f"Пользователь {member.name} был кикнут", description=f'Пользователь {member.name} кикнут администратором {ctx.author.name} по причине: "Не указана"', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Вы были кикнуты!", description=f"Увы, но Вы были выгнаны с сервера ``{ctx.guild.name}`` администратором {ctx.author.mention} без указаной причины.")
                    try:
                        await member.send(embed=embed)
                    except:
                        pass
                    finally:
                        await guild.kick(user=member, reason=f'Пользователь кикнут администратором {ctx.author.name} без указанной причины.')
                else:
                    if len(reason) > 150:
                        embed = discord.Embed(title="Ошибка", description=f"Указанная вами причина не может превышать более 150 символов!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title=f"Пользователь {member.name} был кикнут", description=f'Пользователь {member.name} кикнут администратором {ctx.author.name} по причине: "{reason}"', color=discord.Color.green())
                        await ctx.send(embed=embed)
                        embed = discord.Embed(title="Вы были кикнуты!", description=f"Увы, но Вы были выгнаны с сервера ``{ctx.guild.name}`` администратором {ctx.author.mention} по причине: ``{reason}``")
                        try:
                            await member.send(embed=embed)
                        except:
                            pass
                        finally:
                            await guild.kick(user=member, reason=f'Пользователь кикнут администратором {ctx.author.name} по причине: {reason}')
            else:
                embed = discord.Embed(title="Ошибка", description="У вас нет прав на использование данной команды над данным пользователем.", color=discord.Color.red())
        else:
            guild = ctx.guild
            if reason is None:
                embed = discord.Embed(title=f"Пользователь {member.name} был кикнут", description=f'Пользователь {member.name} кикнут администратором {ctx.author.name} по причине: "Не указана"', color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Вы были кикнуты!", description=f"Увы, но Вы были выгнаны с сервера ``{ctx.guild.name}`` администратором {ctx.author.mention} без указаной причины.")
                try:
                    await member.send(embed=embed)
                except:
                    pass
                finally:
                    await guild.kick(user=member, reason=f'Пользователь кикнут администратором {ctx.author.name} без указанной причины.')
            else:
                if len(reason) > 150:
                    embed = discord.Embed(title="Ошибка", description=f"Указанная вами причина не может превышать более 150 символов!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Пользователь {member.name} был кикнут", description=f'Пользователь {member.name} кикнут администратором {ctx.author.name} по причине: "{reason}"', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Вы были кикнуты!", description=f"Увы, но Вы были выгнаны с сервера ``{ctx.guild.name}`` администратором {ctx.author.mention} по причине: ``{reason}``")
                    try:
                        await member.send(embed=embed)
                    except:
                        pass
                    finally:
                        await guild.kick(user=member, reason=f'Пользователь кикнут администратором {ctx.author.name} по причине: {reason}')


    @moder.command(description="Блокировка пользователя на данном сервере")
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(member='Пользователь, которого вы хотите кикнуть')
    @app_commands.describe(reason='Причина бана пользователя')
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, reason: str = None):
        if member and member.top_role.position >= ctx.author.top_role.position:
            if check_bot_owner(int(ctx.author.id)) is True:
                guild = ctx.guild
                if reason is None:
                    embed = discord.Embed(title=f"Пользователь {member.name} был забанен", description=f'Пользователь {member.name} забанен администратором {ctx.author.name} по причине: "Не указана"', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Вы были забанены!", description=f"Увы, но Вы были забанены на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} без указаной причины.")
                    try:
                        await member.send(embed=embed)
                    except:
                        pass
                    finally:
                        await guild.ban(user=member, reason=f'Пользователь забанен администратором {ctx.author.name} без указанной причины.')
                else:
                    if len(reason) > 150:
                        embed = discord.Embed(title="Ошибка", description=f"Указанная вами причина не может превышать более 150 символов!", color=discord.Color.red())
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(title=f"Пользователь {member.name} был забанен", description=f'Пользователь {member.name} забанен администратором {ctx.author.name} по причине: "{reason}"', color=discord.Color.green())
                        await ctx.send(embed=embed)
                        embed = discord.Embed(
                        title="Вы были забанены!",
                        description=
                        f"Увы, но Вы были забанены на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} по причине: ``{reason}``")
                        try:
                            await member.send(embed=embed)
                        except:
                            pass
                        finally:
                            await guild.ban(user=member, reason=f'Пользователь забанен администратором {ctx.author.name} по причине: {reason}')
            else:
                embed = discord.Embed(title="Ошибка", description="У вас нет прав на использование данной команды над данным пользователем.", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            guild = ctx.guild
            if reason is None:
                embed = discord.Embed(title=f"Пользователь {member.name} был забанен", description=f'Пользователь {member.name} забанен администратором {ctx.author.name} по причине: "Не указана"', color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Вы были забанены!", description=f"Увы, но Вы были забанены на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} без указаной причины.")
                try:
                    await member.send(embed=embed)
                except:
                    pass
                finally:
                    await guild.ban(user=member, reason=f'Пользователь забанен администратором {ctx.author.name} без указанной причины.')
            else:
                if len(reason) > 150:
                    embed = discord.Embed(title="Ошибка", description=f"Указанная вами причина не может превышать более 150 символов!",color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Пользователь {member.name} был забанен", description=f'Пользователь {member.name} забанен администратором {ctx.author.name} по причине: "{reason}"', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Вы были забанены!", description=f"Увы, но Вы были забанены на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} по причине: ``{reason}``")
                    try:
                        await member.send(embed=embed)
                    except:
                        pass
                    finally:
                        await guild.ban(user=member, reason=f'Пользователь забанен администратором {ctx.author.name} по причине: {reason}')


    @moder.command(description='Разбанить пользователя')
    @commands.has_permissions(ban_members=True)
    @app_commands.describe(user='Пользователь, которого нужно разбанить')
    @commands.guild_only()
    async def unban(self, ctx, user: str):
        try:
            await ctx.guild.unban(user=user, reason=f'Разбанен администратором {ctx.author.name}')
            embed = discord.Embed(title='Готово', description=f'Пользователь {user.name} был успешно разбанен администратором {ctx.author.name}', color=discord.Color.green())
            await ctx.send(embed=embed)
            try:
                embed = discord.Embed(title='Внимание!', description=f'Вы были успешно разбанены на сервере ``{ctx.guild.name}`` администратором {ctx.author.name}')
                await user.send(embed=embed)
            except:
                pass
        except:
            embed = discord.Embed(title='Ошибка', description=f'Произошла ошибка! Возможно, данный пользователь не находится в блокировке, либо вы указали неверный ID.', color=discord.Color.red())
            await ctx.send(embed=embed)


    @moder.command(description='Изменить никнейм пользователю')
    @commands.has_permissions(manage_nicknames=True)
    @app_commands.describe(member='Пользователь которому вы хотите изменить нинкейм')
    @app_commands.describe(nickname='Новый никнейм, который вы хотите поставить пользователю')
    @commands.guild_only()
    async def nickname(self, ctx, member: discord.Member, nickname: str):
        if member and member.top_role.position >= ctx.author.top_role.position:
            embed = discord.Embed(title="Ошибка", description="У вас нет прав на использование данной команды над данным пользователем.", color=discord.Color.red())
            await ctx.send(embed=embed)
        else:
            if len(nickname) > 32:
                embed = discord.Embed(title="Ошибка", description="Максимальная длинна никнейма не может превышать 32-ух символов!", color=discord.Color.red())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Готово', description=f"Теперь у пользователя **{member.name}#{member.discriminator}** новый никнейм: **{nickname}**",color=discord.Color.red())
                await ctx.send(embed=embed)
                await member.edit(nick=nickname)


    @moder.command(description='Очистить сообщения в канале')
    @commands.has_permissions(manage_messages=True)
    @app_commands.describe(amount='Кол-во сообщений для удаления')
    @commands.guild_only()
    async def clear(self, ctx, amount: int):
        if amount > 200:
            if await check_premium(ctx.guild.id, ctx.guild.owner_id):
                if amount > 400:
                    embed = discord.Embed(title=f'Ошибка', description='Вы не можете удалить более четырёхсот сообщений разом!\nВам даже не поможет подписка Splash! PREMIUM, так как установленный лимит удаления сообщений: 500', color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title='Идёт удаление...', description=f'Идёт удаление {amount} сообщений(-я, -e)! Подождите пожалуйста чуть-чуть...', color=discord.Color.orange())
                    await ctx.send(embed=embed)
                    await ctx.channel.purge(limit=amount + 1)
                    embed = discord.Embed(title='Готово', description=f'Я успешно смог очистить в этом канале {amount} сообщений(-я, -е)! :white_check_mark: ', color=discord.Color.green())
                    await ctx.channel.send(embed=embed, delete_after=3)
            else:
                embed = discord.Embed(title=f'Ошибка', description='Вы не можете удалить более двухсот сообщений разом!\n**Т-с-с...**\nКупите подписку Splash! PREMIUM всего-лишь за 50₽ в честь открытия Splash! v2.0, чтобы снять ограничения с команд!', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Идёт удаление...', description=f'Идёт удаление {amount} сообщений(-я, -e)! Подождите пожалуйста чуть-чуть...', color=discord.Color.orange())
            await ctx.send(embed=embed)
            await ctx.channel.purge(limit=amount + 1)
            embed = discord.Embed(title='Готово', description=f'Я успешно смог очистить в этом канале {amount} сообщений(-я, -е)! :white_check_mark: ', color=discord.Color.green())
            await ctx.channel.send(embed=embed, delete_after=3)


    @moder.group(fallback='give', description='Изменение ролей участника')
    @app_commands.describe(member='Пользователь, с которым будет выполнена операция')
    @app_commands.describe(role='Роль, с которой будет выполнена операция')
    @commands.guild_only()
    async def role(self, ctx, member: discord.Member, role: discord.Role):
        if role.position >= ctx.author.top_role.position:
            if int(ctx.author.id) in bot['owners']:
                try:
                    await member.add_roles(role)
                    embed = discord.Embed(title='Готово', description=f'Роль <@&{role.id}> была успешно выдана пользователю {member.mention}!', color=discord.Color.green())
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title='Ошибка', description='Возможно, у меня нет прав либо заданная вами роль расположена выше моей!', color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title='Ошибка', description='Данная роль расположена выше вашей!', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            try:
                await member.add_roles(role)
                embed = discord.Embed(title='Готово', description=f'Роль <@&{role.id}> была успешно выдана пользователю {member.mention}!', color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title='Ошибка', description='Возможно, у меня нет прав либо заданная вами роль расположена выше моей!',color=discord.Color.red())
                await ctx.send(embed=embed)


    @role.command(description='Изменение ролей участника')
    @app_commands.describe(member='Пользователь, с которым будет выполнена операция')
    @app_commands.describe(role='Роль, с которой будет выполнена операция')
    @commands.guild_only()
    async def remove(self, ctx, member: discord.Member, role: discord.Role):
        if role.position >= ctx.author.top_role.position:
            if int(ctx.author.id) in bot['owners']:
                try:
                    await member.remove_roles(role)
                    embed = discord.Embed(title='Готово', description=f'Роль <@&{role.id}> была успешно изъята у пользователя {member.mention}!', color=discord.Color.green())
                    await ctx.send(embed=embed)
                except:
                    embed = discord.Embed(title='Ошибка', description='Возможно, у меня нет прав либо заданная вами роль расположена выше моей!', color=discord.Color.red())
                    await interaction.response.send_message(embed=embed)
            else:
                embed = discord.Embed(title='Ошибка', description='Данная роль расположена выше вашей!', color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            try:
                await member.add_roles(role)
                embed = discord.Embed(title='Готово', description=f'Роль <@&{role.id}> была успешно изъята у пользователя {member.mention}!', color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title='Ошибка', description='Возможно, у меня нет прав либо заданная вами роль расположена выше моей!',color=discord.Color.red())
                await ctx.send(embed=embed)


    @moder.command(description='Размьютить пользователя')
    @app_commands.describe(member='Пользователь, которого вы хотите заткнуть')
    @commands.guild_only()
    async def unmute(self, ctx, member: discord.Member):
        if member and member.top_role.position >= ctx.author.top_role.position:
            if check_bot_owner(ctx.user.id):
                await member.timeout(datetime.timedelta(seconds=0), reason=f"Пользователь размьючен администратором {ctx.author.name}")
                embed = discord.Embed(title='Готово', description=f"Пользователь {member.name} был успешно размьючен администратором {ctx.author.name}!", color=discord.Color.green())
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Ошибка", description="У вас нет прав на использование данной команды над данным пользователем.", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            await member.timeout(datetime.timedelta(seconds=0), reason=f"Пользователь размьючен администратором {ctx.author.name}")
            embed = discord.Embed(title='Готово', description=f"Пользователь {member.name} был успешно размьючен администратором {ctx.author.name}!", color=discord.Color.green())
            await ctx.send(embed=embed)


    @moder.command(description='Выдаёт запрет на общение на сервере пользователю')
    @commands.has_permissions(moderate_members=True)
    @app_commands.describe(member='Пользователь, которого вы хотите заткнуть')
    @app_commands.describe(time='Время наказания')
    @app_commands.describe(reason='Причина мьюта пользователя')
    @commands.guild_only()
    async def mute(self, ctx, member: discord.Member, time: str, reason: str = None):
        if member and member.top_role.position >= ctx.author.top_role.position:
            embed = discord.Embed(title="Ошибка", description="У вас нет прав на использование данной команды над данным пользователем.", color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
        else:
            try:
                seconds = int(time[:-1])
                duration = time[-1]
                if duration == "s":
                    test = 'test'
                if duration == "m":
                    seconds *= 60
                if duration == "h":
                    seconds *= 3600
                if duration == "d":
                    seconds *= 86400
            except:
                embed = discord.Embed(title=f"Ошибка", description=f"Вы указали неверное время. Примеры указания времени: 1s, 1m, 1d (s - секунды, m - минуты, d - дни)", color=discord.Color.red())
                return await ctx.send(embed=embed)
            if reason is None:
                embed = discord.Embed(title=f"Пользователь {member.name} был заткнут", description=f'Пользователь {member.name} заткнут администратором {ctx.author.name} по причине: "Не указана"', color=discord.Color.green())
                await ctx.send(embed=embed)
                embed = discord.Embed(title="Вы были замьючены!", description=f"Увы, но Вы не можете теперь говорить на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} без указаной причины.")
                await member.send(embed=embed)
                await member.timeout(datetime.timedelta(seconds=seconds), reason=f'Пользователь замьючен администратором {ctx.author.name} без указанной причины.')
            else:
                if len(reason) > 150:
                    embed = discord.Embed(title="Ошибка", description=f"Указанная вами причина не может превышать более 150 символов!", color=discord.Color.red())
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Пользователь {member.name} был заткнут", description=f'Пользователь {member.name} заткнут администратором {ctx.author.name} по причине: "{reason}"', color=discord.Color.green())
                    await ctx.send(embed=embed)
                    embed = discord.Embed(title="Вы были замьючены!", description=f"Увы, но Вы не можете теперь говорить на сервере ``{ctx.guild.name}`` администратором {ctx.author.mention} по причине: ``{reason}``")
                    await member.send(embed=embed)
                    await member.timeout(datetime.timedelta(seconds=seconds), reason=f"Пользователь заткнут администратором {ctx.author.name} по причине: {reason}")


async def setup(client: commands.Bot):
    await client.add_cog(Moderation(client))