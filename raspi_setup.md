## このリポジトリについて
おもちゃ箱用プログラム

## セットアップ手順
ラズパイ公式からNOOBS最新版をダウンロードし、SDカードにコピーする。  
https://www.raspberrypi.org/downloads/noobs/

SDカードをラズパイに差し込み、ラズパイを起動させる。  
Raspbianを選択し、インストールする。  
OSのセットアップが完了し、WiFiの設定も行った後、まずは既存のソフトをアップデートしておく。
```
sudo apt-get update
sudo apt-get upgrade
```

ラズパイで日本語入力を有効にしたい場合は下記を実行。
```
sudo apt-get install fcitx-mozc
sudo reboot
```
キーボードレイアウトをmozcに変更する。  
（参考：https://www.fabshop.jp/%E3%80%90step-10%E3%80%91%E6%97%A5%E6%9C%AC%E8%AA%9E%E5%85%A5%E5%8A%9B%E3%83%A1%E3%82%BD%E3%83%83%E3%83%89fcitx-mozc%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB/ ）  
ラズパイで開発を行うなど、日本語入力が必要な作業をする予定がないなら不要。


BLE関係のプログラムを動かすため、pyblenoをインストール
```
sudo pip3 install pybleno
```

ADC用のライブラリをインストール
```
sudo pip3 install adafruit-circuitpython-ads1x15
```

sudoなしでpyblenoを使えるよう設定変更
```
sudo setcap cap_net_raw+eip $(eval readlink -f $(which pyton3))
```

ラズパイ起動時にプログラムが立ち上がるよう設定する。
まずはcronの設定を開く
```
crontab -e
```
開いたら末尾に下記を追加
```
@reboot /usr/bin/python3 /home/pi/toybox/main.py
```

スピーカーから音が出るよう設定変更する。  
最新のraspbianではオーディオ設定がGUIからのみになっているので、画面右上のスピーカーアイコンを右クリック  
「HDMI」と「Analog」が出るが、ここはHDMIを選択しておく。  
モニターをHDMIでつないでいる時はAnalog設定でないとスピーカーから音が出ないが、  
モニターをつないでいない実装時はなぜかHDMI設定でないとスピーカーから音が出ないため。  
OS側のバグ？そのうち修正されると思うが...  
  
sshでデバッグできると便利なので、IPアドレスを固定する。
```
sudo nano /etc/dhcpcd.conf
```
で設定ファイルを開き、以下のように設定する。
```
interface eth0
static ip_address=192.168.0.20/24
```
あとはラズパイ自体の設定でsshを有効にすればつながる。  
sshのポートそのままだと不正アクセスが怖いので、変更しておく。
```
sudo nano /etc/ssh/sshd_config
```
この中の"#Port 22"のコメントアウトを外し、ポートを変更。
```
Port [任意の番号]
```
