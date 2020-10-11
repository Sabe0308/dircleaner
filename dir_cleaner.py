# ライブラリのインポート
import os
import datetime
import shutil

# 変数設定
today = datetime.date.today()
trashcan = today.strftime('%Y%m%d')
delete_kouho = "削除候補フォルダ"
downloadpath = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\Downloads"
delete_kouho_path = downloadpath + "\削除候補フォルダ"

# 関数部
#Transporter 使用されなかったファイル削除候補フォルダにを移動する
def transporter():
    os.chdir(downloadpath)
    os.mkdir(trashcan)
    move_list = []

    if not os.path.exists(delete_kouho):
        os.mkdir(delete_kouho)
        print('ダウンロードフォルダの中に「削除候補フォルダ」を作成しました')

    # ファイル更新日から60日以上経過しているファイルを移動
    contents = os.listdir(downloadpath)
    for file in contents:
        if os.path.isfile(file):
            timestamp = datetime.date.fromtimestamp(os.path.getmtime(file))
            diff = today - timestamp
            if diff.days > 60:
                move_list.append(file)
                shutil.move(file, trashcan)

    if len(move_list) == 0:
        shutil.rmtree(trashcan)
        print('削除候補に移動されたファイルはありませんでした')
    elif len(move_list) >= 10:
        shutil.move(trashcan, delete_kouho)
        print('多数のファイルが削除候補に移動されました')
        print('削除候補の中のフォルダは30日間で削除されます')
    else:
        for file in move_list:
            print(file)
        shutil.move(trashcan, delete_kouho)
        print('上記のファイルが削除候補に移動されました')
        print('削除候補の中のフォルダは30日間で削除されます')

#deleter transporter関数で作られた削除候補フォルダの内、30日以上使用されなかったものを移動する
def deleter():
    delete_list = []
    os.chdir(delete_kouho_path)
    contents = os.listdir(delete_kouho_path)
    for dir in contents:
        timestamp = datetime.date.fromtimestamp(os.path.getmtime(dir))
        diff = today - timestamp
        if diff.days > 30:
            delete_list.append(dir)
            shutil.rmtree(dir)

    if len(delete_list) == 0:
        print('削除したフォルダはありませんでした')
    else:
        for dir in delete_list:
            print(dir)
        print('上記のフォルダを削除しました')

#処理部
transporter()
deleter()
input()
