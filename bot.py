# -*- coding: utf-8 -*- #

from typing import Union
import discord
from discord.ext import commands

import sqlite3
import json

# tokens
import config as cf
# cog
from cogs import m10s_remainder
from cogs import takumi_jyanken
from cogs import m10s_announce
from cogs import m10s_userinfo
from cogs import takumi_music

bot = commands.Bot(command_prefix="g/", status=discord.Status.invisible,
                   allowed_mentions=discord.AllowedMentions(everyone=False),
                   intents=discord.Intents.all())
bot.color = 0xe8da1c
bot.ydk_token = cf.ydk_token
bot.developers = cf.bot_developers
bot.GAPI_TOKEN = cf.google_api_key


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
    takumi_music.setup(bot)
    print(f"logined as {bot.user.name}(id:{bot.user.id})")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="g/help | Ver1.2"))


@bot.command()
async def credit(ctx):
    e=discord.Embed(title="クレジット",description="SP thanks",color=bot.color)
    e.add_field(name="takumi0213#0213",value="Botのソースコード制作/実行サーバー契約者")
    e.add_field(name="mii-10#3110",value="Botのソースコード制作/早期認証Botデベロッパー")
    e.add_field(name="結衣華❁⃘❀✩*⋆#1632",value="Embedのカラー選定")
    e.add_field(name="葵 -あおい-#0782",value="ユーザー情報コマンド等での評価値の提供")
    await ctx.send(embed=e)

@bot.command(name="set_status")
async def change_status(ctx,*,text):
    if ctx.author.id in bot.developers:
        await bot.change_presence(activity=discord.Game(name=text))
        await ctx.send("変更しました。")

@bot.command(name="debug_on")
async def debug_on(ctx):
    if ctx.author.id in bot.developers:
       await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="デバックモード中 | g/help"))
       await ctx.send("デバックモードを有効にしました。")

@bot.command(name="debug_off")
async def debug_off(ctx):
    if ctx.author.id in bot.developers:
       await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="g/help | Ver1.2"))
       await ctx.send("デバックモードを無効にしました。")

@bot.command()
    async def ping(ctx):
        latency = bot.latency
        await ctx.send(latency)

bot.remove_command("help")

@bot.command(name="help")
async def help_(ctx,into=None):
    if into:
        help_content=cf.helps.get(into,None)
        if help_content:
            e = discord.Embed(title="gorakuba's bot コマンドメニュー",description=f"> {into}のヘルプ\n　{help_content}",color=bot.color)
        else:
            e = discord.Embed(title="gorakuba's bot コマンドメニュー",description="> 該当のコマンドは見つかりませんでした！",color=bot.color)
    else:
        e = discord.Embed(title="gorakuba's bot コマンドメニュー",color=bot.color)
        e.add_field(name="✨一般ユーザー向け",value="`userinfo`,`jyanken`,`remainder`,`help`,`music'`(これは必ず引数に入れて詳細をご確認ください。)",inline=False)
        e.add_field(name="🔐管理ユーザー向け",value="`jishaku`,`announce`,`set_status`",inline=False)
    await ctx.send(embed=e)


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