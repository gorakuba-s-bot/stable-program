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
        embed.add_field(name="プロセッサ", value=platform.processor())
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}({platform.version()})")
        embed.add_field(
            name="メモリ", value=f"全てのメモリ容量:{allmem}GB\n使用量:{used}GB({memparcent}%)\n空き容量{ava}GB({100-memparcent}%)")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(other(bot))