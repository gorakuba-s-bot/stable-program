# -*- coding: utf-8 -*- #

from cogs.m10s_userinfo import m10s_userinfo
from typing import Union
import discord
from discord.ext import commands

import sqlite3
import json


import config as cf

from cogs import m10s_remainder
from cogs import takumi_jyanken
from cogs import m10s_announce
from cogs import m10s_userinfo

bot = commands.Bot(command_prefix="g!", status=discord.Status.invisible,
                   allowed_mentions=discord.AllowedMentions(everyone=False,users=False,roles=None),
                   intents=discord.Intents.all())
bot.remaind=[]
bot.color = 0x000000
bot.ydk_token = cf.ydk_token


sqlite3.register_converter('json', json.loads)
sqlite3.register_adapter(dict, json.dumps)

db = sqlite3.connect(
    "main.db", detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
db.row_factory = sqlite3.Row
bot.cursor = db.cursor()

bot.cursor.execute("create table if not exists remaind(\
    id integer primary key not null,\
    stext text not null,\
    mention_role integer,\
    time real not null,\
    chid integer not null)")


@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    m10s_remainder.setup(bot)
    takumi_jyanken.setup(bot)
    m10s_announce.setup(bot)
    m10s_userinfo.setup(bot)
    print(f"logined as {bot.user.name}(id:{bot.user.id})")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="g!help"))


@bot.event
async def on_command_error(ctx,error):
    """
    コマンド実行中に起きたエラーへの対応
    エラーの種類を確かめて適切な表示を行うのは後で
    """
    await ctx.send(f"> コマンド実行時エラー\n　{ctx.command.name}コマンドの実行時に次のエラーが発生しました。\n```{error}```")


bot.run(cf.token)