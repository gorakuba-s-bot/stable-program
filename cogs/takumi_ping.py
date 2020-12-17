# -*- coding: utf-8 -*- #

import json
import datetime
import discord
from discord.ext import commands, tasks


class takumi_ping(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ping(self, ctx):
        message_time = ctx.message.created_at.timestamp()
        time_before_send = datetime.datetime.utcnow().timestamp()
        msg = await ctx.send("...")
        time_after_send = datetime.datetime.utcnow().timestamp()
        latency = self.bot.latency
        tb = abs(time_before_send - message_time)
        ba = abs(time_after_send - time_before_send)
        content = f"LA: {latency:.3}\nTB: {tb:.3}\nBA: {ba:.3}\n"
        if hasattr(ctx, "context_at") and isinstance(ctx.context_at, float):
            context_at = ctx.context_at
            tc = abs(context_at - message_time)
            cb = abs(time_before_send - context_at)
            content += f"TC: {tc:.3}\nCB: {cb:.3}\n"
        await msg.edit(content=content)

def setup(bot):
    bot.add_cog(takumi_ping(bot))