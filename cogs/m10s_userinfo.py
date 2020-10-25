# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands
import aiohttp

from typing import Union

from dateutil.relativedelta import relativedelta as rdelta

class m10s_userinfo(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(name="userinfo",aliases=["ui","user"])
    async def _info_of_user(self, ctx, target:Union[commands.MemberConverter,None]):
        admin_role = ctx.guild.get_role(601052213435039745)
        if target is None:
            target = ctx.author

        headers ={
            "Authorization":f"Authorization {self.bot.ydk_token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.yudzuki.pw/v1/users/{target.id}',headers=headers) as rs:
                if rs.status == 200:
                    rtn = rs.json()
                    if rtn["result"]:
                        ydk_ev = rs.json()["settings"]["evaluate_value"]
                    else:
                        ydk_ev = -1
                else:
                    ydk_ev = -1
        
        e=discord.Embed(color=self.bot.color)
        e.set_author(name=target,icon_url=target.avatar_url_as(static_format="png"))
        e.add_field(name="オンライン状況",value=target.status)
        e.add_field(name="Discord Bot:結月による評価値",value=ydk_ev if ydk_ev != -1 else "評価値が取得できませんでした")
        e.add_field(name="役職リスト",value="\n".join([i.mention for i in target.roles]))
        if admin_role in ctx.author.roles:
            e.set_footer(text=(target.created_at + rdelta(hours=9)).strftime('%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}').format(*'年月日時分秒'))
        if ctx.author.id == 525658651713601536:
            e.add_field(name="サーバー内権限",value=f"```{','.join(target.guild_permissions)}```")
        await ctx.send(embed=e)
        


def setup(bot):
    bot.add_cog(m10s_userinfo)