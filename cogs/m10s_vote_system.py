# coding:utf-8

import discord
from discord.ext import commands

import json

"""
bot.cursor.execute("create table if not exists vote(\
    name integer primary key not null,\
    panel integer not null,\
    targets json not null\
    )")
"""


class m10s_vote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.vt = bot.get_emoji(800296846181793822)

    @commands.group
    async def vote(self, ctx:commands.Context):
        if not ctx.invoked_subcommand:
            await ctx.reply("> 投票システム\n　`create [name] *[targets]`")

    @vote.command()
    async def create(self, ctx:commands.Context, name:str, *targets):
        if self.bot.cursor.execute("SELECT * FROM vote WHERE name = ?",(name,)).fetchone():
            await ctx.reply("> 投票システム\n　すでにその名前の投票が存在します。")
        else:
            rt = "\n"
            msg = await ctx.send(embed=discord.Embed(title=f"投票:'{name}'",description=f"立候補者:```{rt.join(targets)}```"))
            await msg.add_reaction(self.vt)
            self.bot.cursor.execute("INSERT INTO vote (name,panel,targets) VALUES (?,?,?)", (name, msg.id, json.dumps(list(targets))))
            with open(f"{name}.json",mode="w") as f:
                json.dump({
                    "name":name,
                    "votes":[]
                }, f)
            await ctx.reply("> 投票システム\n　投票の作成が完了しました。")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,pr):
        
        self.bot.cursor.execute("select * from vote where panel = ?",(pr.message_id,))
        rs = self.bot.cursor.fetchone()
        if rs and pr.emoji.id == self.vt.id:
            dm = pr.member.dm_channel or await pr.member.create_dm()
            with open(f"{rs['name']}.json",mode="r") as f:
                j = json.load(f)
            if pr.member.id in [v["user"][1] for v in j["votes"]]:
                await dm.send("あなたは投票済みです。")
                return
            result = []
            for t in rs["targets"]:
                m = await dm.send(f"> {t}を信任するかどうかをリアクションしてください。")
                await m.add_reaction("✅")
                await m.add_reaction("❌")
                r,u = await self.bot.wait_for("reaction_add",check=lambda r,u:u.id == pr.user_id and r.message.id == m.id and str(r.emoji) in "✅❌")
                result.append([t,str(r.emoji)])
            with open(f"{rs['name']}.json",mode="r") as f:
                j = json.load(f)
            j["votes"].append({
                "user":[str(pr.member),pr.member.id],
                "result":result
            })
            with open(f"{rs['name']}.json",mode="w") as f:
                json.dump(j,f)
            await dm.send("投票ありがとうございました。")



def setup(bot):
    bot.add_cog(m10s_vote(bot))