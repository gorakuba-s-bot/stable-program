# -*- coding: utf-8 -*- #

from typing import Union
import discord
from discord.ext import commands

import sqlite3
import json

import datetime

import config as cf

from cogs import m10s_remainder
from cogs import takumi_jyanken

bot = commands.Bot(command_prefix="g!", status=discord.Status.invisible,
                   allowed_mentions=discord.AllowedMentions(everyone=False),
                   intents=discord.Intents.all())
bot.remaind=[]


sqlite3.register_converter('json', json.loads)
sqlite3.register_adapter(dict, json.dumps)
"""sqlite3.register_converter('datetime', datetime.datetime.fromtimestamp)
sqlite3.register_adapter(datetime.datetime, get_timestamp)"""

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
    print(f"logined as {bot.user.name}(id:{bot.user.id})")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="g!help"))

bot.run(cf.token)