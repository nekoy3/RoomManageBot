import sys
import discord

import logfile_rw
import cfg_rw

def main():
    bot = discord.Bot()
    cfg = cfg_rw.main()
    class File:
        pass
    chs = []
    logfile_rw.make_logfile()

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
    return bot, cfg, File, chs, continue_flag, count

if __name__ == '__main__':
    main()