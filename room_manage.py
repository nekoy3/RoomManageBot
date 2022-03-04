# coding: utf_8
import discord
import time
from discord.commands import Option
import configparser

bot = discord.Bot()
config = configparser.ConfigParser()
config.read('config.ini', encoding="utf-8_sig")

first_server_name = str(config['SERVER']['first_server_name'])
second_server_name = str(config['SERVER']['second_server_name'])

TOKEN = str(config['TOKEN']['token'])

type_dict = {'one': config['CHANNEL']['first_channel_color'], 'two': config['CHANNEL']['second_channel_color'], 'er': config['OTHER']['error_message_color']}
id_dict = {'one': [config['SERVER']['first_server_id'], config['CHANNEL']['first_channel_id']], 'two': [config['SERVER']['second_server_id'], config['CHANNEL']['second_channel_id']]}
max_count = int(config['OTHER']['max_roomcount'])

print('Starting...')
count = 0
def count_manage(n):
    global count
    count += n

def add_embed(title, descrip, type):
    embed = discord.Embed(title=title, description=descrip, color=type_dict[type])
    embed.set_footer(text="部屋人数管理システム")
    return embed

def write_logfile(username, c, io_type, server_name):
    f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} {server_name} {username} {io_type}:{c} sum:{count}\n")

#ログファイル生成
filename = time.strftime("room-%Y-%m-%d-%H-%M-%S") + ".log"
f = open(filename, "a")

#初期設定
@bot.listen()
async def on_ready():
    print('Logged in as\n' + bot.user.name + "\n" + str(bot.user.id) + "\n------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/enter, /exit'))
    await bot.user.edit(username='部屋人数管理システム')

@bot.slash_command(guild_ids=[id_dict['one'][0], id_dict['two'][0]])
async def enter(
    ctx,
    num: Option(int, '利用人数を入力してください'),
):
    global filename
    one_ch, two_ch = bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['one'][1])
    count_manage(num)
    if count > max_count:
        count_manage(-num)
        await ctx.respond("エラー")
        embed = add_embed("満員", f"同時利用人数は{max_count}人以下にして下さい。", "er")
        await one_ch.send(embed=embed)
        await two_ch.send(embed=embed)
        return

    if str(ctx.channel.id) == id_dict['one'][1]:
        embed = add_embed("利用通知", f'{first_server_name}で{num}人入室しました。現在の利用人数は{count}人です。', "one")
        await ctx.respond(embed=embed)
        await two_ch.send(embed=embed)
        write_logfile(ctx.author, num, "in", first_server_name)

    elif str(ctx.channel.id) == id_dict['two'][1]:
        embed = add_embed("利用通知", f'{second_server_name}で{num}人入室しました。現在の利用人数は{count}人です。', "two")
        await ctx.respond(embed=embed)
        await one_ch.send(embed=embed)
        write_logfile(ctx.author, num, "in", second_server_name)

@bot.slash_command(guild_ids=[id_dict['one'][0], id_dict['two'][0]])
async def exit(
    ctx,
    num: Option(int, '退出人数を入力してください'),
):
    global filename
    one_ch, two_ch = bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['two'][1])
    count_manage(-num)
    if count < 0:
        count_manage(num)
        await ctx.respond("エラー")
        embed = add_embed("エラー", "0人を下回らないで下さい。", "er")
        await one_ch.send(embed=embed)
        await two_ch.send(embed=embed)
        return

    if str(ctx.channel.id) == id_dict['one'][1]:
        embed = add_embed("利用通知", f'{first_server_name}で{num}人退室しました。現在の利用人数は{count}人です。', "one")
        await ctx.respond(embed=embed)
        await two_ch.send(embed=embed)
        write_logfile(ctx.author, num, "out", first_server_name)

    elif str(ctx.channel.id) == id_dict['two'][1]:
        embed = add_embed("利用通知", f'{second_server_name}で{num}人退室しました。現在の利用人数は{count}人です。', "two")
        await ctx.respond(embed=embed)
        await one_ch.send(embed=embed)
        write_logfile(ctx.author, num, "out", second_server_name)

@bot.slash_command() #botをログファイルを閉じて停止させる
async def stop(ctx):
    f.close()
    await ctx.respond("botを停止しました。")
    await exit()

bot.run(TOKEN)