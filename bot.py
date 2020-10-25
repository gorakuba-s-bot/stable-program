# -*- coding: utf-8 -*- #

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
                   allowed_mentions=discord.AllowedMentions(everyone=False,users=False,roles=False),
                   intents=discord.Intents.all())
bot.remaind=[]
bot.color = 0xe8da1c
bot.ydk_token = cf.ydk_token
bot.developers = cf.bot_developers


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


@bot.command()
async def credit(ctx):
    e=discord.Embed(title="クレジット",description="SP thanks",color=bot.color)
    e.add_field(name="takumi0213#0213",value="Botのソースコード制作/実行サーバー契約者")
    e.add_field(name="mii-10#3110",value="Botのソースコード制作/早期認証Botデベロッパー")
    e.add_field(name="結衣華❁⃘❀✩*⋆#1632",value="Embedのカラー選定")
    e.add_field(name="葵 -あおい-#0782",value="ユーザー情報コマンド等での評価値の提供")
    await ctx.send(embed=e)

@bot.event
async def on_command_error(ctx,error):
    """
    コマンド実行中に起きたエラーへの対応
    エラーの種類を確かめて適切な表示を行うのは後で
    """
    await ctx.send(f"> コマンド実行時エラー\n　{ctx.command.name}コマンドの実行時に次のエラーが発生しました。\n```{error}```")


bot.run(cf.token)