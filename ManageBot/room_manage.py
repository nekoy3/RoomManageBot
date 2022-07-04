# coding: utf_8 
import discord
from discord import Webhook
from discord.commands import Option
from datetime import datetime
import asyncio
import aiohttp

import logfile_rw
import f_global
import start

stop_warn_infomation_flag = False

bot, guilds, cfg, chs, continue_flag, count, ch_ids, hook_list = start.main()
def count_manage(n, set_boolean):
    global count
    if set_boolean:
        count = n
    else:
        count += n

def add_embed(title, descrip, type):
    embed = discord.Embed(title=title, description=descrip, color=int(cfg.type_dict[type], 16))
    return embed

async def webhook_send(url, str, username, icon):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(url, session=session)
        #print(webhook.channel_id + " " + webhook.guild_id)
        await webhook.send(str, username=username) #, avatar_url=icon)

@bot.listen()
async def on_ready():
    global chs, hook_list, guilds
    print('Logged in as\n' + bot.user.name + "\n" + str(bot.user.id) + "\n------")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/in, /out, /gc'))
    await bot.user.edit(username='部屋人数管理システム')
    chs = [bot.get_partial_messageable(cfg.channel_id_list[0]), bot.get_partial_messageable(cfg.channel_id_list[1])]
    #guilds = [bot.get_guild(cfg.guild_id_list[0]), bot.get_guild(cfg.guild_id_list[1])]
    try:
        guilds = [bot.get_guild(cfg.guild_id_list[0]), bot.get_guild(cfg.guild_id_list[1])]
    except:
        guilds = [bot.get_guild(cfg.guild_id_list[0])]
    

    
    #channel = bot.get_channel(cfg.channel_id_list[0])
    #print(channel)
    # --> None
    '''
    #チャンネルからwebhookを取得する
    for ch in chs:
        for hook in ch.webhooks:
            hook_list.append(hook)
    #チャンネルがTextChannelオブジェクトでは無くPartialMessageableオブジェクトのため、webhook取得が不可
    #TextChannelオブジェクトの取得(get_channel)はNoneTypeを返すため、不可（原因不明）
    #webhookからチャンネル取得->webhookオブジェクトにchannel(もしくはchannel_id)属性が存在はするがNoneを返してくるため不可
    '''

    task = asyncio.get_event_loop().create_task(loop())

#メッセージ取得時メッセージ内容にアクセスすることが出来ないためスラッシュコマンドでの実装（応急処置）
@bot.slash_command(guild_id=ch_ids, name="gc", description="相手サーバーにメッセージを送信するためのコマンドです。")
async def global_chat(
    ctx,
    msg: Option(str, '渡す文字列を入力'),
):
    global guilds
    #ユーザー名とアイコンを取得
    if ctx.author.nick != None:
        user_name = ctx.author.nick
    else:
        user_name = ctx.author.name

    cid = ctx.channel.id
    #member_id = ctx.author.id

    if cid == cfg.globalchat_channel_id_list[0]:
        #member = guilds[0].get_member(member_id)
        #user_icon = member.avatar_url
        #guildが取得できないためパス(アイコン取得)
        await webhook_send(cfg.webhooks[1], msg, user_name, None)
        await webhook_send(cfg.webhooks[0], msg, user_name, None)

    if cid == cfg.globalchat_channel_id_list[1]:
        #member = guilds[1].get_member(member_id)
        #user_icon = member.avatar_url
        await webhook_send(cfg.webhooks[0], msg, user_name, None)
        await webhook_send(cfg.webhooks[1], msg, user_name, None)
    
    await ctx.respond('sent > ' + msg)
    await ctx.delete()


@bot.slash_command(guild_id=ch_ids, name="in", description="部屋に入室するときのコマンドです。")
async def enter(
    ctx,
    num: Option(int, '利用人数を入力してください'),
):
    global chs
    count_manage(num, False)
    if count > cfg.max_count and cfg.can_max_over == "False":
        count_manage(-num, False)
        embed = add_embed("満員", f"同時利用人数は{cfg.max_count}人以下にして下さい。", "er")
        await ctx.respond(embed=embed)
        return

    if ctx.channel.id == cfg.channel_id_list[0]:
        embed = add_embed("利用通知", f'{cfg.first_server_name}で{num}人入室しました。現在の利用人数は{count}人です。', "one")
        await ctx.respond(embed=embed)
        await chs[1].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "in", cfg.first_server_name, count)

    elif ctx.channel.id == cfg.channel_id_list[1]:
        embed = add_embed("利用通知", f'{cfg.second_server_name}で{num}人入室しました。現在の利用人数は{count}人です。', "two")
        await ctx.respond(embed=embed)
        await chs[0].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "in", cfg.second_server_name, count)

    if count > cfg.max_count and stop_warn_infomation_flag == False:
        embed = add_embed("警告", f"定員{cfg.max_count}人に対して、現在大人数が入室しています。\n換気し、私語を控えるようにしてください。", "er")
        [await channel.send(embed=embed) for channel in chs]

@bot.slash_command(guild_id=ch_ids, name="out", description="部屋を退室するときのコマンドです。")
async def out(
    ctx,
    num: Option(int, '退出人数を入力してください'),
):
    global chs
    count_manage(-num, False)
    if count < 0:
        count_manage(num, False)
        embed = add_embed("エラー", "0人を下回らないで下さい。", "er")
        await ctx.respond(embed=embed)
        return

    if ctx.channel.id == cfg.channel_id_list[0]:
        embed = add_embed("利用通知", f'{cfg.first_server_name}で{num}人退室しました。現在の利用人数は{count}人です。', "one")
        await ctx.respond(embed=embed)
        await chs[1].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "out", cfg.first_server_name, count)

    elif ctx.channel.id == cfg.channel_id_list[1]:
        embed = add_embed("利用通知", f'{cfg.second_server_name}で{num}人退室しました。現在の利用人数は{count}人です。', "two")
        await ctx.respond(embed=embed)
        await chs[0].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "out", cfg.second_server_name, count)

@bot.slash_command(guild_id=ch_ids, description="現在の人数が部屋の人数と会わない場合、気づいた人が現在人数を設定しなおしてください。")
async def set(
    ctx,
    num: Option(int, '現在の人数を入力してください'),
):
    count_manage(num, True)
    global chs
    if count < 0:
        embed = add_embed("エラー", "0人以上の数字を入力してください。", "er")
        await ctx.respond(embed=embed)
        return
    
    if ctx.channel.id == cfg.channel_id_list[0]:
        embed = add_embed("現在の人数", f'現在の人数は{count}人です。\n({cfg.first_server_name}で編集されました。)', "one")
        await ctx.respond(embed=embed)
        await chs[1].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "set", cfg.first_server_name, count)
    else:
        embed = add_embed("現在の人数", f'現在の人数は{count}人です。\n({cfg.second_server_name}で編集されました。)', "two")
        await ctx.respond(embed=embed)
        await chs[0].send(embed=embed)
        logfile_rw.write_logfile(ctx.author, num, "set", cfg.second_server_name, count)
    
    if count > cfg.max_count and stop_warn_infomation_flag == False:
        embed = add_embed("警告", f"定員{cfg.max_count}人に対して、現在大人数が入室しています。\n換気し、私語を控えるようにしてください。", "er")
        [await channel.send(embed=embed) for channel in chs]

@bot.slash_command(guild_id=ch_ids, description="使わないでください。botを停止します。") #botをログファイルを閉じて停止させる
async def stop(ctx):
    f_global.f.close()
    await ctx.respond("botを停止しました。")
    await bot.close()

def stop_warn():
    return datetime.now().strftime('%H:%M'), None

async def loop():
    await asyncio.sleep(30) #botが起動するまで待機する目安
    global count, cfg, bot, chs, stop_warn_infomation_flag
    stop_warn_time = "00:00"
    while True:
        if stop_warn_infomation_flag:
            stop_warn_time, stop_warn_infomation_flag = stop_warn()
        
        now = datetime.now().strftime('%H:%M')
        if now == cfg.daily_reset_time:
            if count != 0:
                count = 0
                logfile_rw.write_logfile("reset", 0, "reset", "", 0)
                for i in chs:
                    await i.send(embed=add_embed("現在の人数", f'人数が0で無かったため、リセットされました。', "one"))
            
            #ログファイルを再生成する
            f_global.f.close()
            logfile_rw.make_logfile()
            logfile_rw.write_logfile("reset", 0, "reset", "", 0)
        
        if now == stop_warn_time and stop_warn_infomation_flag == None:
            stop_warn_infomation_flag = False
        
        await asyncio.sleep(30)

bot.run(cfg.TOKEN)
