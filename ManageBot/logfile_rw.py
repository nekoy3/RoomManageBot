import os
import glob
import time

import f_global

#ログファイル生成
def create_log_dir():
    os.mkdir('logs') if not os.path.exists('logs') else None

def tail(fn):
    with open(fn, 'r') as latest_file:
        lines = latest_file.readlines()
    print(str(lines))
    if len(lines) == 1:
        return lines[0]
    else:
        return lines[-1]

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

#ログファイル作成
def make_logfile():
    filename = time.strftime("room-%Y-%m-%d-%H-%M-%S") + ".log"
    f_global.f = open("./logs/" + filename, "a")

#ログ書き込み
def write_logfile(username, c, io_type, server_name, sum):
    f_global.f.write(f"{time.strftime('%Y/%m/%d %H:%M:%S')} {server_name} {username} {io_type}:{c} sum:{sum}\n")

def main():
    pass

if __name__ == '__main__':
    main()