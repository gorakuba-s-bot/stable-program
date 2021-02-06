# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
import random
import time
import asyncio
import platform
import re
import psutil


class other(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botinfo(self, ctx):
        mem = psutil.virtual_memory()
        allmem = str(mem.total/1000000000)[0:3]
        used = str(mem.used/1000000000)[0:3]
        ava = str(mem.available/1000000000)[0:3]
        memparcent = mem.percent
        embed = discord.Embed(title="所属サーバー数", description=f"{len(self.bot.guilds)}", color=self.bot.color)
        embed.add_field(name="最終起動時間", value=self.bot.StartTime.strftime(
            '%Y{0}%m{1}%d{2} %H{3}%M{4}%S{5}').format(*'年月日時分秒'))
        embed.add_field(name="Pythonバージョン",
                        value=platform.python_version())
        embed.add_field(name="プロセッサ", value="Intel(R) Xeon(R) CPU E5-2660 v3 @ 2.60GHz")
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}({platform.version()})")
        embed.add_field(
            name="メモリ", value=f"全てのメモリ容量:{allmem}GB\n使用量:{used}GB({memparcent}%)\n空き容量{ava}GB({100-memparcent}%)")
        await ctx.send(embed=embed)

    
    @commands.group()
    @commands.is_owner()
    async def manage_features(self, ctx):
        pass

    @manage_features.command(name="view")
    async def view_(self,ctx,uid:int):
        await ctx.reply(f"```py\n{self.bot.features.get(uid,[])}```")

    @manage_features.command(name="del")
    async def del_(self,ctx,uid:int,feature):
        uf = self.bot.features.get(uid,None)
        if uf and feature in uf:
            self.bot.features[uid].remove(feature)
        await ctx.message.add_reaction(self.bot.get_emoji(790552892838248448))

    @manage_features.command(name="add")
    async def add_(self,ctx,uid:int,feature):
        uf = self.bot.features.get(uid,None)
        if uf:
            self.bot.features[uid].append(feature)
        else:
            self.bot.features[uid] = [feature]
        await ctx.message.add_reaction(self.bot.get_emoji(790552892838248448))

    @manage_features.command(name="reload")
    async def reload_(self,ctx):
        import importlib
        import config
        importlib.reload(config)
        self.bot.features = config.sp_features
        await ctx.message.add_reaction(self.bot.get_emoji(790552892838248448))

    @commands.command()
    async def emojiinfo(self, ctx, *, emj: commands.EmojiConverter=None):

        if emj is None:
            await ctx.send(ctx._("einfo-needarg"))
        else:
            embed = discord.Embed(
                title=emj.name, description=f"id:{emj.id}", color=self.bot.ec)
            embed.add_field(name=ctx._("einfo-animated"), value=emj.animated)
            embed.add_field(name=ctx._("einfo-manageout"), value=emj.managed)
            if emj.user:
                embed.add_field(name=ctx._("einfo-adduser"),
                                value=str(emj.user))
            embed.add_field(name="url", value=emj.url)
            embed.set_footer(text=ctx._("einfo-addday"))
            embed.set_thumbnail(url=emj.url)
            embed.timestamp = emj.created_at
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(other(bot))