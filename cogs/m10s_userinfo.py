# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands
import aiohttp

from typing import Union

import datetime
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
            "Authorization":f"Bearer {self.bot.ydk_token}"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.aoichaan0513.jp/v1/users/{target.id}',headers=headers) as rs:
                if rs.status == 200:
                    rtn = await rs.json()
                    ydk_ev = rtn["settings"]["evaluate_value"]
                else:
                    ydk_ev = -1
        
        badges = ""
        role_ids = [i.id for i in target.roles]
        if 770996612503175258 in role_ids: #開発者チーム
            badges+="💠"
        if 770996609533607958 in role_ids: #認証アカウント
            badges+="✅"
        if 599804873118187520 in role_ids: #Bot
            badges+="⚙"
        if 601052213435039745 in role_ids: #運営@サポート
            badges+="🛠"
        if 611730459402960907 in role_ids: #サーバーブースター
            badges+="✨"
        if 676051183923757108 in role_ids: #SP-Vip
            badges+="🎗"

        e=discord.Embed(color=self.bot.color)
        e.set_author(name=badges+str(target),icon_url=target.avatar_url_as(static_format="png"))
        e.add_field(name="オンライン状況",value=target.status)
        e.add_field(name="Discord Bot:結月による評価値",value=ydk_ev if ydk_ev != -1 else "評価値が取得できませんでした")
        e.add_field(name="役職リスト",value="\n".join([i.mention for i in target.roles]))
        if admin_role in ctx.author.roles:
            e.set_footer(text=f"{(target.created_at + rdelta(hours=9)).strftime('%Y年%m月%d日%H時%M分%S秒')}({(datetime.datetime.now()-(target.created_at+ rdelta(hours=9))).days}日前にアカウント作成)")
        if ctx.author.id == 525658651713601536:
            e.add_field(name="サーバー内権限",value=f"```{','.join([i[0] for i in iter(target.guild_permissions) if i[1]])}```")
        await ctx.send(embed=e)
        

def setup(bot):
    bot.add_cog(m10s_userinfo(bot))