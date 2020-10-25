# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands


class m10s_announce(commands.Cog):
    def __init__(self,bot):
         self.bot = bot

    @commands.command(name="announce")
    async def send_other_ch(self, ctx, title, *, text):
        role = ctx.guild.get_role(769835497706881044)
        if role in ctx.author.roles:
            mrole = ctx.guild.get_role(698022495051055114)
            ch = self.bot.get_channel(592201270014640138)
            e = discord.Embed(title=title, description=text, color=ctx.author.color)
            e.timestamp = ctx.message.created_at
            e.set_author(name=f"{ctx.guild}からのお知らせ", icon_url=ctx.guild.icon_url_as(static_format="png"))
            e.set_footer(text=f"送信者:{ctx.author.display_name}", icon_url=ctx.author.avatar_url_as(static_format="png"))
            if ctx.message.attachments:
                e.set_image(url=ctx.message.attachments[0].url)
            try:
                await ch.send(f"{mrole.mention}",embed=e)
            except discord.Forbidden:
                await ctx.send("> 送信できません！\n　botに必要な権限が割り当てられているかどうかを確認してください。")
            except discord.HTTPException:
                await ctx.send("> 送信できません！\n　メッセージの送信に失敗しました。")    

def setup(bot):
    bot.add_cog(m10s_announce)