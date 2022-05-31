import sys
import discord

import logfile_rw
import cfg_rw

def get_decolator_fixed_id_list(ids):
    one = ids[0]
    two = ids[1]
    if one == two:
        return [one]
    else:
        return [one, two]

def main():
    bot = discord.Bot()
    cfg = cfg_rw.main()
    chs = []
    hook_list = []
    guilds = []
    logfile_rw.create_log_dir()
    logfile_rw.make_logfile()
    
    #デコレータに使用するチャンネルIDが重複する場合の対策
    ch_ids = get_decolator_fixed_id_list(cfg.channel_id_list)
    print('Starting...')

    try:
        if sys.argv[1] == 'continue':
            continue_flag = True
        else:
            continue_flag = False
    except:
        continue_flag = False

    if continue_flag:
        count = logfile_rw.read_latest_log()
    else:
        count = 0

    print("count = " + str(count))

    logfile_rw.write_logfile('system', 0, 'start', 'system', count)
    return bot, guilds, cfg, chs, continue_flag, count, ch_ids, hook_list

if __name__ == '__main__':
    main()