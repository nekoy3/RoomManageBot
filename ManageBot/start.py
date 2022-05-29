import sys
import discord

import logfile_rw
import cfg_rw

def decolator_fix(ids):
    one = ids['one'][0]
    two = ids['two'][0]
    if one == two:
        return [one]
    else:
        return [one, two]

def main():
    bot = discord.Bot()
    cfg = cfg_rw.main()
    chs = []
    logfile_rw.create_log_dir()
    logfile_rw.make_logfile()

    guilds = [bot.get_guild(cfg.id_dict['one'][0]), bot.get_guild(cfg.id_dict['two'][0])]
    
    #デコレータに使用するチャンネルIDが重複する場合の対策
    ch_ids = decolator_fix(cfg.id_dict)
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
    return bot, guilds, cfg, chs, continue_flag, count, ch_ids

if __name__ == '__main__':
    main()