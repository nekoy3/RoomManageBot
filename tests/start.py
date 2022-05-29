import discord

import cfg_rw

def main():
    bot = discord.Bot()
    cfg = cfg_rw.main()

    print('Starting...')

    return bot, cfg

if __name__ == '__main__':
    main()
