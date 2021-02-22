# -*- coding: utf-8 -*- #

from typing import Union
import discord
from discord.ext import commands
import logging

import asyncio

import sqlite3
import json

import datetime

# tokens
import config as cf
# cog
from cogs import m10s_remainder
from cogs import takumi_jyanken
from cogs import m10s_announce
from cogs import m10s_userinfo
from cogs import takumi_music
from cogs import takumi_ping
from cogs import takumi_suiso
from cogs import takumi_other
from cogs import m10s_vote_system
bot = commands.Bot(command_prefix="g.", status=discord.Status.invisible,
                   allowed_mentions=discord.AllowedMentions(everyone=False),
                   intents=discord.Intents.all())
bot.color = 0xe8da1c
bot.developers = cf.bot_developers
bot.GAPI_TOKEN = cf.google_api_key

bot.StartTime = datetime.datetime.now()

bot.version = "1.5.0"


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

bot.cursor.execute("create table if not exists vote(\
    name integer primary key not null,\
    panel integer not null,\
    targets json not null\
    )")


@bot.event
async def on_ready():
    bot.load_extension("jishaku")
    m10s_remainder.setup(bot)
    takumi_jyanken.setup(bot)
    m10s_announce.setup(bot)
    m10s_userinfo.setup(bot)
    takumi_music.setup(bot)
    takumi_ping.setup(bot)
    takumi_suiso.setup(bot)
    takumi_other.setup(bot)
    m10s_vote_system.setup(bot)
    logging.basicConfig(level=logging.WARNING)
    print('------------------')
    print('ログインしました。')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    
    files = ["m10s_remainder", "takumi_jyanken", "m10s_announce", "m10s_userinfo", "takumi_music", "takumi_ping",
             "takumi_suiso", "takumi_other", "m10s_vote_system"
            ]
      
    print(f"Extension {files} Load.")
    print('------------------')
      
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"g.help | Ver{bot.version}"))


@bot.event
async def on_voice_state_update(m, b, a):
    if m.guild.id == 592199606323118081:
        role = m.guild.get_role(795600507103215637)
        if (b.channel is None) and (not a.channel is None):
            # 参加時処理
            await m.add_roles(role)
        elif (not b.channel is None) and (a.channel is None):
            # 退出時処理
            await m.remove_roles(role)

@bot.command()
async def credit(ctx):
    e=discord.Embed(title="クレジット",description="SP thanks",color=bot.color)
    e.add_field(name="takumi0213#0213",value="Botのソースコード制作/実行サーバー契約者")
    e.add_field(name="mii-10#3110",value="Botのソースコード制作/早期認証Botデベロッパー")
    e.add_field(name="結衣花❀.*･ﾟ#0217",value="Embedのカラー選定")
    e.add_field(name="葵 -あおい-#0782",value="ユーザー情報コマンド等での評価値の提供")
    await ctx.send(embed=e)

@bot.command(name="set_status")
async def status_set(ctx,*,text):
    if ctx.author.id in bot.developers:
        await bot.change_presence(activity=discord.Game(name=text))
        await ctx.send("変更しました。")

@bot.command(name="debug_on")
async def debug_on(ctx):
    if ctx.author.id in bot.developers:
       await bot.change_presence(status=discord.Status.invisible)
       await ctx.send("デバックモードを有効にしました。")

@bot.command(name="debug_off")
async def debug_off(ctx):
    if ctx.author.id in bot.developers:
       await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"g.help | Ver{bot.version}"))
       await ctx.send("デバックモードを無効にしました。")

@bot.command(name="check")
async def user_check(ctx):
    if ctx.author.id in bot.developers:
        await ctx.send("ようこそ！ゴラクバ！クラフターズ(ゴラクラ)へ！\n ユーザー認証の際に問題が発生したためお知らせしています。\n 安全のため「あなたがこのサーバーに入ってきた理由」の確認を行っています。\n お手数をおかけしますが、ご協力をお願いします。\n (このメッセージは運営チームが定めるリストの中にあなたのアカウントがある際に自動送信されます。)")

bot.remove_command("help")

@bot.command(name="help")
async def help_(ctx):
    with open("help.json",mode="r") as j:
        helps = json.load(j)

    page = 0
    pmax = len(helps)-1
    
    def get_help(page):
        e = discord.Embed(title=helps[page]["title"],description=helps[page]["description"],color = bot.color)
        e.set_footer(text=f"{page + 1}/{pmax + 1}")
        return e

    msg = await ctx.send(embed=get_help(page))
    await msg.add_reaction("⬅")
    await msg.add_reaction("➡")

    while True:
        try:
            r, u = await bot.wait_for("reaction_add", check=lambda r, u: r.message.id == msg.id and u.id == ctx.message.author.id, timeout=30)
        except asyncio.TimeoutError:
            break
        try:
            await msg.remove_reaction(r, u)
        except discord.Forbidden:
            pass
        if str(r) == "➡":
            if page == pmax:
                page = 0
            else:
                page = page + 1
        elif str(r) == "⬅":
            if page == 0:
                page = pmax
            else:
                page = page - 1
        await msg.edit(embed=get_help(page))


@bot.event
async def on_command_error(ctx,error):
    """
    コマンド実行中に起きたエラーへの対応
    エラーの種類を確かめて適切な表示を行うのは後で
    """
    await ctx.send(f"> コマンド実行時エラー\n　{ctx.command.name}コマンドの実行時に次のエラーが発生しました。\n```{error}```")

@bot.event
async def on_command(ctx):
    e = discord.Embed(title="コマンド実行ログ",description=f"実行分:`{ctx.message.clean_content}`",color=bot.color)
    e.set_author(name=f"{ctx.author}({ctx.author.id})",icon_url=ctx.author.avatar_url_as(static_format="png"))
    e.timestamp = ctx.message.created_at
    ch = bot.get_channel(772111846374506516)

    await ch.send(embed=e)


bot.run(cf.token)
