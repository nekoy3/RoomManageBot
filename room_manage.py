import discord
import time
from discord.commands import Option

sk_serverid = '略' #シス研サーバーid
sk_channelid = '略' #シス研チャンネルid
gl_serverid = '略' #ゲームラボサーバーid
gl_channelid = '略' #ゲームラボチャンネルid
TOKEN = '略' #botトークン
bot = discord.Bot()

print('Starting...')
count = 0
def count_manage(n):
    global count
    count += n

def add_embed(title, descrip, type):
    #ckシス研 水色 glゲームラボ 紫 erエラー通知 赤 dict型
    type_dict = {'ck': 0x66A6FF, 'gl': 0xCA80FF, 'er': 0xFF0000}
    embed = discord.Embed(title=title, description=descrip, color=type_dict[type])
    embed.set_footer(text="部屋人数管理システム")
    return embed

def write_logfile(username, c, io_type):
    with open(filename, "a") as f:
        f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} シス研 {username} {io_type}:{c} sum:{count}\n")

#ログファイル生成
filename = time.strftime("room-%Y-%m-%d-%H-%M-%S") + ".log"
open(filename, "w").close()

#初期設定
@bot.listen()
async def on_ready():
    print('Logged in as\n' + bot.user.name + "\n" + str(bot.user.id) + "\n------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/enter, /exit'))
    await bot.user.edit(username='部屋人数管理システム')

@bot.slash_command(guild_ids=[sk_serverid, gl_serverid])
async def enter(
    ctx,
    num: Option(int, '利用人数を入力してください'),
):
    global filename
    skch, glch = bot.get_partial_messageable(sk_channelid), bot.get_partial_messageable(gl_channelid)
    count_manage(num)
    if count > 10:
        count_manage(-num)
        await ctx.respond("エラー")
        embed = add_embed("満員", "同時利用人数は10人以下にして下さい。", "er")
        await skch.send(embed=embed)
        await glch.send(embed=embed)
        return

    if str(ctx.channel.id) == sk_channelid:
        embed = add_embed("利用通知", f'シス研で{num}人入室しました。現在の利用人数は{count}人です。', "ck")
        await ctx.respond(embed=embed)
        await glch.send(embed=embed)
        write_logfile(ctx.author, num, "in")

    elif str(ctx.channel.id) == gl_channelid:
        embed = add_embed("利用通知", f'ゲームラボで{num}人入室しました。現在の利用人数は{count}人です。', "gl")
        await ctx.respond(embed=embed)
        await skch.send(embed=embed)
        write_logfile(ctx.author, num, "in")

@bot.slash_command(guild_ids=[sk_serverid, gl_serverid])
async def exit(
    ctx,
    num: Option(int, '退出人数を入力してください'),
):
    global filename
    skch, glch = bot.get_partial_messageable(sk_channelid), bot.get_partial_messageable(gl_channelid)
    count_manage(-num)
    if count < 0:
        count_manage(num)
        await ctx.respond("エラー")
        embed = add_embed("エラー", "0人を下回らないで下さい。", "er")
        await skch.send(embed=embed)
        await glch.send(embed=embed)
        return

    if str(ctx.channel.id) == sk_channelid:
        embed = add_embed("利用通知", f'シス研で{num}人退室しました。現在の利用人数は{count}人です。', "ck")
        await ctx.respond(embed=embed)
        await glch.send(embed=embed)
        write_logfile(ctx.author, num, "out")

    elif str(ctx.channel.id) == gl_channelid:
        embed = add_embed("利用通知", f'ゲームラボで{num}人退室しました。現在の利用人数は{count}人です。', "gl")
        await ctx.respond(embed=embed)
        await skch.send(embed=embed)
        write_logfile(ctx.author, num, "out")

bot.run(TOKEN)