# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands
import asyncio

class takumi_suiso(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener
    async def on_message(self,message):
        if "プシュ" in message.content:
            await message.channel.send("プシュー")
        if "水素の音" in message.content:
            await message.channel.send("あ～あぁぁぁぁぁぁ～～水素の音ぉ～")

        if message.content == "g.kasi":
            e = discord.Embed(title="水素の音 歌詞",description="ｻｲｷﾝ ﾃﾞｷﾔｽ… \nなんか健康のために 気遣ってなんかやってることあります？\nあっ！水素水飲んでます 水素水！\nこっち見て。ジャジャン！\nえ！\nほらこれ！\nえ！ \nすごいでしょ！ \nなんですかこれ！\nパンパンでしょ！パンパン \nすごい全然違うほら！\n開けてみたいでしょ～？ \nうん、みたーい！\n行きますよー！ \nせーのっ！ \nあぁ～！水素の音ォ～！！",color=0x66ffff)
            e.set_footer(text=f"水素は命！")
            e.timestamp = message.created_at

            await message.channel.send(embed=e)

        
        if "水素" == message.content:
            await message.channel.send("水素はすごいんだよ！！！")
        if "suiso" == message.content:
            await message.channel.send("Suiso is amazing!!!")
        if "水槽" == message.content:
            await message.channel.send("水槽？ちがうちがう！**水素**だからね？")
        if "suisou" == message.content:
            await message.channel.send("Suisou? No different! Because it’s Suiso, right?")
        if "彗星" == message.content:
            await message.channel.send("彗星？ちゃんと聞いてた？す・い・そ　だってば！")
        if "suisei" == message.content:
            await message.channel.send("Suisei? Did you hear properly? Su I So!")

def setup(bot):
    bot.add_cog(takumi_suiso(bot))