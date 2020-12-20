# -*- coding: utf-8 -*-

from os import cpu_count
import discord
from discord.ext import commands,tasks
from discord.mentions import AllowedMentions

import config as cf
import twitter




class takumi_twinotif_camp(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.twi = twitter.Twitter(auth=twitter.OAuth(cf.T_Acs_Token, cf.T_Acs_SToken, cf.T_API_key, cf.T_API_SKey))
        self.target = ["tsukasa_yt","Nadeshiko_gogo"]
        self.last_id = [self.gtwi_fu(i)[0] for i in self.target]
        self.ch = self.bot.get_channel(790217848370888714)
        self.loop_task.start()


    def gtwi_fu(self,uname):
        ret = self.twi.statuses.user_timeline(screen_name=uname,count=1)
        return (int(ret[0]["id"]),ret[0])

    @tasks.loop(seconds=10)
    async def loop_task(self):
        ret = [self.gtwi_fu(i) for i in self.target]
        for i in range(len(ret)):
            if not self.last_id[i] == ret[i][0]:
                self.last_id[i] = ret[i][0]
                tweet = ret[i][1]
                embed = discord.Embed(description=tweet["text"], color=int(
                    tweet["user"]["profile_background_color"], 16))
                embed.set_author(name=f'{tweet["user"]["name"]}(@{tweet["user"]["screen_name"]})',
                                    url=f'https://twitter.com/{tweet["user"]["screen_name"]}', icon_url=tweet["user"]["profile_image_url_https"])
                try:
                    embed.set_image(
                        url=tweet["entities"]["media"][0]["media_url_https"])
                except:
                    pass
                embed.add_field(name="Twitterで見る", value=f'https://twitter.com/{tweet["user"]["screen_name"]}/status/{tweet["id"]}')
                await self.ch.send(embed=embed)

def setup(bot):
    bot.add_cog(takumi_twinotif_camp(bot))