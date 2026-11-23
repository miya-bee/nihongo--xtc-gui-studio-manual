# 23. Linux版で使う

【v4.0.3から】日本語XTC GUI Studio には、Windows版・macOS版のほかに **Linux版（AppImage `TategakiXTC_GUI_Studio-x86_64.AppImage`）** があります。
画面の作りと変換の結果は Windows版と同じです。このマニュアルのほかの章は、そのまま Linux版にも当てはまります。

この章では、Linux版だけの手順（入れ方・起動できないとき）と、Windows版と呼び方や場所が違うところをまとめます。

## 動作環境

- **x86_64（64ビットの Intel / AMD）の Linux**。ARM（Raspberry Pi など）では動きません
- **Ubuntu 22.04・Debian 12・Fedora 36 以降に相当する環境**（glibc 2.35 以降）
- X11 または Wayland のデスクトップ環境
- ディストリビューションやデスクトップ環境によっては、追加のライブラリが必要です（[起動できないとき](#起動できないとき)）
- Python は要りません（AppImage の中に入っています）

## ダウンロード

Trial版には出力ページ数の上限があります。Full版との違いは[17章](17-editions.md)をご覧ください。

- [Linux x86_64 Trial版 v4.0.4](https://drive.google.com/file/d/1cpRPETf33MIRpkT2xCGcDT_8y4b6btjO/view?usp=drive_link)
- [Linux x86_64 Full版 v4.0.4](https://drive.google.com/file/d/1wJMqqjgtnsUJkjc_OeuP3f8s6wJuJIp6/view?usp=drive_link)

## 入れ方と起動

1. Linux版の ZIP（名前の末尾が `_linux-x86_64.zip`）をダウンロードして展開します
2. 中の AppImage（1つのファイル）を、好きな場所へ移します（例: ホームフォルダの `Applications` フォルダ）。
   Full版は **`TategakiXTC_GUI_Studio-x86_64.AppImage`**、Trial版は **`TategakiXTC_GUI_Studio_Trial-x86_64.AppImage`** です
3. ダブルクリックで起動します

起動しないときは、ファイルを右クリック →「プロパティ」→「アクセス権」で「プログラムとして実行可能」にします。
ターミナルなら、次のように実行権限を付けて起動します。

```bash
chmod +x TategakiXTC_GUI_Studio-x86_64.AppImage
./TategakiXTC_GUI_Studio-x86_64.AppImage
```

Trial版では、ファイル名を `TategakiXTC_GUI_Studio_Trial-x86_64.AppImage` に読み替えてください。
同じ ZIP の `README_FIRST_linux.txt` に、この章と同じ手順が書いてあります。

> AppImage はそれだけではアプリケーションメニューに登録されません。登録したいときは、AppImageLauncher や Gear Lever などの AppImage 管理ツールを使ってください。

## 起動できないとき

| 出るメッセージ | 対処 |
|---|---|
| 「FUSE」に関するメッセージ | ディストリビューションに合わせて FUSE を入れます。Ubuntu 22.04 以降・Debian: `sudo apt install libfuse2`（Ubuntu 24.04 では環境によって `libfuse2t64`）、Fedora: まず `sudo dnf install fuse3`。入れられない環境では `./TategakiXTC_GUI_Studio-x86_64.AppImage --appimage-extract-and-run` で起動できます（毎回展開するので起動が遅くなります） |
| 「Could not load the Qt platform plugin "xcb"」 | Debian / Ubuntu は `sudo apt install libxcb-cursor0`、Fedora / Arch は `xcb-util-cursor` を入れます |

## 日本語の入力

【v4.0.6.1から】fcitx（fcitx5 + Mozc など）を使っている環境でも、書籍情報や記事URLの欄に日本語を入力できます。
AppImage には fcitx 用の部品が入っていないため、起動時に、fcitx5 の ibus 互換の窓口へつなぎます。特別な設定は要りません。

日本語のフォントが入っていない環境でも、同梱の Noto Sans JP で画面の日本語を表示します。

## 設定・ログ・データの保存場所

```
~/.local/share/TategakiXTC-GUI-Studio/
```

- 設定ファイル `tategakiXTC_gui_studio.ini`、ログ `logs/`
- 小説URLの登録作品・narou.rs の管理データ（`narou_rs_library/`）・EPUBキャッシュなど
- 【v5.1.0から】組版タブの［参照］で追加したフォント（`font/`）。AppImage の中には書き込めないので、ここに入れます。v5.0.0 では、［参照］で選んでもフォントが一覧に出ませんでした

AppImage を新しい版のものに置き換えても、ここの設定をそのまま使います。版を上げるたびに設定を引き継ぐ作業は要りません。

> ホームフォルダの直下に古いデータフォルダ（`~/.tategaki-xtc-gui-studio`）がある場合は、そちらを使い続けます（以前の版から使っている人の登録作品が見えなくならないようにするためです）。

## 同梱しているもの・していないもの

| | 内容 |
|---|---|
| 同梱 | 記事URLの「本文＋画像」「Web表示」に使う Chromium（headless shell） |
| 同梱 | RAR／CBR の展開に使う 7-Zip |
| 同梱 | 同梱フォント（Noto Sans JP・Noto Serif JP） |
| **同梱していない** | 小説URL（URL→EPUB）で使う Java 21 以上・AozoraEpub3-JDK21・narou.rs（Windows版と同じく、別に入れます。[11章](11-narou.md)） |

- まれに、システムのライブラリが足りずに Chromium が起動しないことがあります。そのときはアプリに案内が出ます
  （Debian / Ubuntu の例: `sudo apt install libnss3 libgbm1 libasound2`）
- 有料・ログインが必要な記事の「ログイン設定」は、パソコンに入っている Chrome・Edge・Brave・Chromium のどれかを使います（[9章](09-article-url.md)）
- AozoraEpub3 は、設定した Java で `java -jar AozoraEpub3.jar` として起動します（`.exe` は Windows 用なので使いません）

## Windows版と呼び方・場所が違うところ

ほかの章の説明を Linux版で読むときは、次のように読み替えてください。

| ほかの章の書き方（Windows版） | Linux版では |
|---|---|
| `TategakiXTC_GUI_Studio.exe`、`START_TATEGAKI_XTC_GUI.bat` | `TategakiXTC_GUI_Studio-x86_64.AppImage` |
| エクスプローラーで開く（［保存先を開く］など） | デスクトップのファイルマネージャーで開く |
| `%LOCALAPPDATA%\TategakiXTC-GUI-Studio\` | `~/.local/share/TategakiXTC-GUI-Studio/` |
| 設定引き継ぎツール（`START_SETTINGS_MIGRATE.bat`） | ありません（AppImage を置き換えても設定はそのまま） |
| `narou_rs.exe` | `narou_rs`（拡張子なし） |
| `java.exe` | `bin/java` |
| Windows の Wi-Fi 設定 | デスクトップ（GNOME・KDE など）の Wi-Fi 設定 |
| 游明朝などの Windows のフォント | Noto や IPA など、Linux に入れたフォント |

## X3/X4 へ送る（Linux）

端末への転送（[16章](16-device-transfer.md)）は、Windows版と同じ手順で使えます。Linux で違う点は次のとおりです。

- 直接接続モードでは、NetworkManager（`nmcli`）で接続中の Wi-Fi の名前（SSID）を確かめます
- かんたん接続ガイドの［Wi-Fi設定を開く］は、デスクトップに合った設定アプリ（GNOME の設定、KDE のシステム設定、`nm-connection-editor` など）を開きます
- 送っている間は、使えれば `systemd-inhibit` でパソコンがスリープしないようにします

## そのほかの違い

- バッチ実行（[20章](20-batch-mode.md)）は、AppImage に引数を付けてターミナルから呼び出します。引数・設定 INI・終了コードは 20章と同じです

```bash
./TategakiXTC_GUI_Studio-x86_64.AppImage my.ini ~/books/a.epub ~/xtc
echo $?
```

## アンインストール

`TategakiXTC_GUI_Studio-x86_64.AppImage` を削除します。設定やデータも消す場合は、
[保存場所](#設定ログデータの保存場所)のフォルダ（`~/.local/share/TategakiXTC-GUI-Studio/`）も削除します。

→ [README（目次）](../README.md)
