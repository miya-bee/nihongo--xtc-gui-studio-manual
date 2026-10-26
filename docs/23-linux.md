# 23. Linux版で使う

日本語XTC GUI Studio には、x86_64 Linux向けのAppImage版があります。
インストール作業は不要で、ZIPを展開してアプリを実行します。

## 動作環境

- x86_64（64ビットのIntel / AMD）Linux。ARM機（Raspberry Piなど）は対象外です
- Ubuntu 22.04、Debian 12、Fedora 36相当以降を目安とします。ディストリビューションやデスクトップ環境により、追加ライブラリが必要な場合があります
- X11とWaylandのどちらでも動作する想定です

## ダウンロードと展開

Trial版には出力ページ数の上限があります。Full版との違いは[17章](17-editions.md)をご覧ください。

- [Linux x86_64 Trial版 v4.0.4](https://drive.google.com/file/d/1cpRPETf33MIRpkT2xCGcDT_8y4b6btjO/view?usp=drive_link)
- [Linux x86_64 Full版 v4.0.4](https://drive.google.com/file/d/1wJMqqjgtnsUJkjc_OeuP3f8s6wJuJIp6/view?usp=drive_link)

ZIPを展開してください。中のAppImageを好きな場所へ移して使えます。アプリ本体をインストールする必要はありません。

## 起動する

AppImageをダブルクリックします。起動しないときは、ファイルを右クリックして［プロパティ］→［アクセス権］を開き、
「プログラムとして実行可能」にチェックを入れてください。

ターミナルから起動する場合は、展開先のフォルダへ移動して実行します。Trial版の例です。

```bash
chmod +x TategakiXTC_GUI_Studio_Trial-x86_64.AppImage
./TategakiXTC_GUI_Studio_Trial-x86_64.AppImage
```

Full版では、展開したZIPに含まれるAppImageのファイル名を確認し、その名前で同じように実行してください。

## 起動できないとき

### FUSEについてのメッセージが出る

ディストリビューションに合わせてFUSEを入れてください。

- Ubuntu 22.04以降・Debian: `sudo apt install libfuse2`
- Ubuntu 24.04: 環境によっては `sudo apt install libfuse2t64`
- Fedora: まず `sudo dnf install fuse3` を試してください

FUSEをインストールできない環境では、次の方法で起動できる場合があります。
毎回ファイルを展開するため、通常より起動に時間がかかります。

```bash
./TategakiXTC_GUI_Studio_Trial-x86_64.AppImage --appimage-extract-and-run
```

### Qtの「xcb」プラグインを読み込めない

「Could not load the Qt platform plugin “xcb”」と表示された場合、不足ライブラリを追加します。

- Debian / Ubuntu: `sudo apt install libxcb-cursor0`
- Fedora / Arch: `xcb-util-cursor` パッケージ

### Web記事の取り込みだけが動かない

同梱Chromiumの起動に必要なシステムライブラリが不足している可能性があります。
アプリ内の案内を確認してください。Debian / Ubuntuでは、次で解消することがあります。

```bash
sudo apt install libnss3 libgbm1 libasound2
```

### アプリケーションメニューに登録したい

AppImageはそのままではアプリケーションメニューに表示されません。
AppImageLauncherやGear Leverなどの管理ツールを使って登録できます。

設定は `~/.local/share/TategakiXTC-GUI-Studio/` に保存されます。

→ [README（目次）](../README.md)
