# coding: utf_8 
import discord

import start

bot, cfg = start.main()

@bot.listen()
async def on_ready():
    print('Logged in as\n' + bot.user.name + "\n" + str(bot.user.id) + "\n------")

bot.run(cfg.TOKEN)