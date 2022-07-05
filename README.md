# RoomManageBot
このbotは、異なるサーバー間で部屋の利用状況を管理するためのbotです。  
コロナ渦においてn人以上同時に部屋を利用して密になることを避けることを目的としています。  
(定員はデフォルトで10人 config.iniにより変更可能)  
py-cord 2.0.0b7を使用  

# Usage
必要なライブラリ（environment.txtに記述)をインストールし、room_manage.pyを動作に必要なid,botのトークンをconfig.ini設定し実行することで動作します。  
config.iniを記述して、その2つのチャンネル間でのみ動作します。
実行時にcontinueを引数で与えると、前回実行時の部屋人数を引き継ぎます。

### 使い方
discordにおける「スラッシュコマンド」を使います。  
部屋に入るときに「/in num:人数」を打ち込むと、入室認証  
部屋を出るときに「/out num:人数」を打ち込むと、退室認証
部屋人数に矛盾がある場合は、「set num:人数」で整合性を取ります。

入退室認証のこれらのコマンドは、どちらか一方のチャンネルで入力すると両方のチャンネルで入退室の通知が行われます。  
![スクリーンショット 2022-02-21 212927](https://user-images.githubusercontent.com/84169441/154955585-a3ba2edd-e0f5-4ac7-9af5-daf4a1d93ef0.png)  

特定人数以上/以下の場合はエラーを表示します。（特定人数の調整はconfig.iniから設定可能）  
![スクリーンショット 2022-02-21 213143](https://user-images.githubusercontent.com/84169441/154955797-f8db6d5d-2284-4b7a-921a-f46da4d46f18.png)

### 人数オーバー時の警告
in,out,setで人数が変わった時点で人数がオーバーしている場合、密である趣旨の警告を表示します。  
警告を表示する間隔は、最小で150分(デフォルトの場合)です。  
※この警告機能はまだ未実装です。(2022/05/31)  

### グローバルチャット機能
あらかじめ決めておいた２つのチャンネル（２つのサーバーidの中のみ）において、  
互いにチャットを共有することが出来ます。  
- 使い方  
  1. 登録されたチャンネルで、「/gc msg:テキストの中身」を入力する  
  2. botからの返信「sent> テキストの中身」が来ていることを確認（メッセージを送信した意味の通知）  
これをお互いにすることで、チャンネル超えてやりとりを共有することが出来ます。  
 
# Note
実行ディレクトリにログファイル「room-yy-mm-dd-hh-mm-ss.log」の形式で出力します。入退室ログをここに出力します。  
![a](https://user-images.githubusercontent.com/84169441/154956338-6c9e3289-a5f6-47c1-af4a-587504a146f8.png)  
 
このプログラムは開発途中です。至らぬ部分や、こうしたらよくなる等の案をぜひお願いします。  

*    *    *
# version
### 2022/3/5  
- ***異常終了時の処理***  
異常終了し、botを再起動した場合にcontinueを引数で与えると最終ログから入室人数を引き継ぐ機能を追加  
  
### 2022/03/24
- ***不具合修正***  
    - config.iniが不十分の状態で起動してしまう不具合を修正  
    - 予期しない入退室をしたときにbotが呈しうる不具合を修正
- ***通知内容***  
通知のembedの無駄な情報を削除  
- ***コマンド名変更***  
enterをinに、exitをoutにコマンド名を変更  
- ***コマンド入力候補***  
コマンドの入力候補にどういったコマンドなのか説明する文を追加  

### 2022/03/26
- ***不具合修正***  
ログファイルに出力する値が正常でない不具合を修正  

### 2022/04/26
- ***一日周期処理の追加***  
config.iniで決められた時刻にログファイルの保存と入室人数を0にリセットするように変更  

### 2022/04/27
- ***定員を超える管理の実装***  
定員を超えてもエラーでは無く、警告メッセージのみ出すように変更  

### 2022/05/17
- ***a,警告表示ルールを変更***  
in時かつ、上限人数を超えているのみ警告を表示していたが、  
in,set構わず10人以上であるときに警告を表示し、一定時間（デフォルト150分）警告を表示しないように変更  
→5/26同様開発途中  

### 2022/05/26(開発途中)
- ***b,グローバルチャットの実装（途中）***  
2サーバー間特定のチャンネルのみチャットをお互いに送信しやりとりが  
出来るようにする機能を追加（configでon/off,チャンネルIDの設定が出来る予定)  
※Webhookを使ってやり取りする方式の予定？  

### 2022/05/31
- ***bの実装***  
最低限使えるように実装  
（使い方はUsageに）  

### 2022/07/05
- ***グローバルチャットの変更***  
グローバルチャットで送信した場合に送信したDiscordサーバー側のメッセージは削除され、  
代わりにwebhookのメッセージが出るように変更  

### 2022/07/05
- ***定員を超えた場合の警告文の送信頻度の変更***  
定員を超えた場合に送信される警告文が一度送信されると、  
指定した間は送信されないように変更  