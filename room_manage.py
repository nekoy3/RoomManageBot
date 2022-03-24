# coding: utf_8
import discord
import time
from discord.commands import Option
import configparser
import glob
import os
import sys
#import datetime
#import asyncio

bot = discord.Bot()
config = configparser.ConfigParser()
try:
    config.read('config.ini', encoding="utf-8_sig")

    first_server_name = str(config['SERVER']['first_server_name'])
    second_server_name = str(config['SERVER']['second_server_name'])

    TOKEN = str(config['TOKEN']['token'])

    type_dict = {'one': config['SERVER']['first_server_color'], 'two': config['SERVER']['second_server_color'], 'er': config['OTHER']['error_message_color']}
    id_dict = {'one': [config['SERVER']['first_server_id'], config['CHANNEL']['first_channel_id']], 'two': [config['SERVER']['second_server_id'], config['CHANNEL']['second_channel_id']]}
    max_count = int(config['OTHER']['max_roomcount'])

except:
    print("config.iniが存在しないか、設定が間違っています。")
    exit()

print('Starting...')

#ログファイル生成
os.mkdir('logs') if not os.path.exists('logs') else None

def tail(fn):
    with open(fn, 'r') as latest_file:
        lines = latest_file.readlines()
    print(str(lines))
    if len(lines) == 1:
        return lines[0]
    else:
        return lines[-1]

#最新ログを取得
try:
    if sys.argv[1] == 'continue':
        continue_flag = True
    else:
        continue_flag = False
except:
    continue_flag = False

#最新(latest)のログファイルを読み取り、最終行から最新の部屋人数を取得
def read_latest_log():
    try:
        list_of_files = glob.glob('./logs/*')
        fn = max(list_of_files, key = os.path.getctime)
        print("latest log -> " + fn)
        last_log = tail(fn)
        cnt = int(last_log.split('sum:')[1])
    except Exception as e:
        print(e)
        cnt = 0
    return cnt

if continue_flag:
    count = read_latest_log()
else:
    count = 0

print("count = " + str(count))

#ログファイル作成
def make_logfile():
    global f
    filename = time.strftime("room-%Y-%m-%d-%H-%M-%S") + ".log"
    f = open("./logs/" + filename, "a")

make_logfile()

def count_manage(n, set_boolean):
    global count
    if set_boolean:
        count = n
    else:
        count += n

def add_embed(title, descrip, type):
    embed = discord.Embed(title=title, description=descrip, color=int(type_dict[type], 16))
    return embed

def write_logfile(username, c, io_type, server_name):
    f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} {server_name} {username} {io_type}:{c} sum:{c}\n")

write_logfile('system', count, 'start', 'system')

#毎日午前二時にログファイルを作り直す
#asyncioの知識が浅すぎて挫折したので、他の方法も模索しながらいったん保留
#def remake_logfile():
#    global f
#    f.close()
#    make_logfile()
#    write_logfile('system', count, 'start', 'system')
#    print("remaked logfile")

#特定の時刻にメソッドを実行する
#参考　https://stackoverflow.com/questions/51292027/how-to-schedule-a-task-in-asyncio-so-it-runs-at-a-certain-date
#また、毎日午前二時にログファイルを作り直すのを実行するようにした
#async def wait_until(dt):
#    now = datetime.datetime.now()
#    await asyncio.sleep((dt - now).total_seconds())
#
#async def sleep_one_day():
#    await asyncio.sleep(30) #86400

#async def run_at(dt, coro):
#    await wait_until(dt)
#    await coro()
#    while True:
#        sleep_one_day()
#        await coro()

#時刻計算の参考 https://note.nkmk.me/python-datetime-usage/
#dt_next_day = datetime.datetime.today().day + 1
#dt_schedule = datetime.datetime(datetime.datetime.today().year, datetime.datetime.today().month, dt_next_day, 2, 0, 0)

#dt_schedule = datetime.datetime.today() + datetime.timedelta(seconds=30)
#async def log_schedule():
#    global dt_schedule
#    loop = asyncio.get_event_loop()
#    loop.create_task(await run_at(dt_schedule, remake_logfile()))
#    loop.run_forever()

#log_schedule()


#初期設定
@bot.listen()
async def on_ready():
    print('Logged in as\n' + bot.user.name + "\n" + str(bot.user.id) + "\n------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/in, /out'))
    await bot.user.edit(username='部屋人数管理システム')
    chs = [bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['two'][1])]
    for i in chs:
        await i.send("部屋人数管理システムを起動しました。現在の部屋人数は" + str(count) + "人です。異なる場合は/setコマンドを使用してください。")

@bot.slash_command(guild_ids = [id_dict['one'][0], id_dict['two'][0]], name = "in", description="部屋に入室するときのコマンドです。")
async def enter(
    ctx,
    num: Option(int, '利用人数を入力してください'),
):
    one_ch, two_ch = bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['two'][1])
    count_manage(num, False)
    if count > max_count:
        count_manage(-num, False)
        embed = add_embed("満員", f"同時利用人数は{max_count}人以下にして下さい。", "er")
        await ctx.respond(embed=embed)
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

@bot.slash_command(guild_ids = [id_dict['one'][0], id_dict['two'][0]], name = "out", description="部屋を退室するときのコマンドです。")
async def out(
    ctx,
    num: Option(int, '退出人数を入力してください'),
):
    one_ch, two_ch = bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['two'][1])
    count_manage(-num, False)
    if count < 0:
        count_manage(num, False)
        embed = add_embed("エラー", "0人を下回らないで下さい。", "er")
        await ctx.respond(embed=embed)
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

@bot.slash_command(guild_ids=[id_dict['one'][0], id_dict['two'][0]], description="現在の人数が部屋の人数と会わない場合、気づいた人が現在人数を設定しなおしてください。")
async def set(
    ctx,
    num: Option(int, '現在の人数を入力してください'),
):
    count_manage(num, True)
    one_ch, two_ch = bot.get_partial_messageable(id_dict['one'][1]), bot.get_partial_messageable(id_dict['two'][1])
    if count < 0 or count > max_count:
        embed = add_embed("エラー", "0人未満または" + str(max_count) + "人以下の数字を入力してください。", "er")
        await ctx.respond(embed=embed)
        return
    
    if str(ctx.channel.id) == id_dict['one'][1]:
        embed = add_embed("現在の人数", f'現在の人数は{count}人です。\n({first_server_name}で編集されました。)', "one")
        await ctx.respond(embed=embed)
        await two_ch.send(embed=embed)
        write_logfile(ctx.author, num, "set", first_server_name)
    else:
        embed = add_embed("現在の人数", f'現在の人数は{count}人です。\n({second_server_name}で編集されました。)', "two")
        await ctx.respond(embed=embed)
        await one_ch.send(embed=embed)
        write_logfile(ctx.author, num, "set", second_server_name)

@bot.slash_command(description="使わないでください。botを停止します。") #botをログファイルを閉じて停止させる
async def stop(ctx):
    f.close()
    await ctx.respond("botを停止しました。")
    await bot.close()

bot.run(TOKEN)
