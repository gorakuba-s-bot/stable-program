# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands
import asyncio
import re

class takumi_suiso(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @bot.event
    async def on message(message):
        if re.search "プシュ" in message.content:
            await message.channel.send("プシュー")

    @bot.event
    async def on message(message):
        if re.search "水素の音" in message.content:
            await message.channel.send("あ～あぁぁぁぁぁぁ～～水素の音ぉ～")
    
    @bot.event
    async def on message(message):
        if re.fullmatch "水素" in message.content:
            await message.channel.send("水素はすごいんだよ！！！")

    @bot.event
    async def on message(message):
        if re.fullmatch "suiso" in message.content:
            await message.channel.send("Suiso is amazing!!!")

    @bot.event
    async def on message(message):
        if re.fullmatch "水槽" in message.content:
            await message.channel.send("水槽？ちがうちがう！**水素**だからね？")

    @bot.event
    async def on message(message):
        if re.fullmatch "suisou" in message.content:
            await message.channel.send("Suisou? No different! Because it’s Suiso, right?")

    @bot.event
    async def on message(message):
        if re.fullmatch "彗星" in message.content:
            await message.channel.send("彗星？ちゃんと聞いてた？す・い・そ　だってば！")

    @bot.event
    async def on message(message):
        if re.fullmatch "suisei" in message.content:
            await message.channel.send("Suisei? Did you hear properly? Su I So!")

def setup(bot):
    bot.add_cog(takumi_suiso(bot))