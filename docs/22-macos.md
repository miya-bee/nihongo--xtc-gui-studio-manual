# 22. macOS版で使う

日本語XTC GUI Studio には、Windows版のほかに **macOS版（アプリ `TategakiXTC_GUI_Studio.app`）** があります。
画面の作りと変換の結果は Windows版と同じです。このマニュアルのほかの章は、そのまま macOS版にも当てはまります。

この章では、macOS版だけの手順（入れ方・初めての起動・許可の確認）と、Windows版と呼び方や場所が違うところをまとめます。

## 動作環境

- **Apple シリコン（M1 以降）または Intel プロセッサを搭載した Mac**
- **macOS 14 Sonoma 以降**。それより前の macOS では起動できません

Mac の種類は、アップルメニュー →「この Mac について」で確かめられます。
「チップ」に「Apple M1」などとあれば Apple シリコン版を、「プロセッサ」に「Intel」とあれば Intel版を選んでください。

## 入れ方

1. 配布ページからお使いの Mac に合う ZIP をダウンロードします。Apple シリコンは `_macos-arm64.zip`、Intel Mac は `_macos-intel.zip` です
2. 「ダウンロード」フォルダの ZIP をダブルクリックして展開します
3. できたフォルダの中の **`TategakiXTC_GUI_Studio.app`** を「アプリケーション」フォルダへドラッグします
   （ほかの場所でも動きますが、移しておくと Launchpad や Spotlight から起動できます）

同じフォルダの `README_FIRST_macos.txt` に、この章と同じ手順が書いてあります。

> Trial版のアプリは **`TategakiXTC_GUI_Studio_Trial.app`** という別の名前です。Full版と並べて置けます
> （設定は Full版と共通です）。版の違いは [17章](17-editions.md) を見てください。

## 初めて起動するとき（1回だけ必要）

このアプリは Apple の公証（Notarization）を受けていません。そのため、ダウンロードしたアプリを初めて開くと、
「“TategakiXTC_GUI_Studio.app”を開けませんでした」「マルウェアが含まれていないことを検証できませんでした」などと表示されて止まります
（macOS の版によって文言は少し違います）。**故障ではありません。** 次のどちらかで開けます。

### 方法A：システム設定から許可する（おすすめ）

ターミナルを使わずに済みます。

1. 表示された画面で **［完了］** を押して閉じます（［ゴミ箱に入れる］は押さないでください）
2. アップルメニュー →「システム設定」→「プライバシーとセキュリティ」を開きます
3. 下の方の「セキュリティ」に、このアプリがブロックされたという表示と **［このまま開く］** が出ているので、押します
4. もう一度確認が出たら **［このまま開く］** を押し、Mac のパスワード（または Touch ID）で許可します

> macOS 15 Sequoia 以降は、Finder の右クリック →［開く］では開けません。古い解説記事のやり方では回避できないので、方法Aを使ってください。

### 方法B：ターミナルを使う

ZIP を**展開する前に**、ZIP から「ダウンロードした印」（隔離属性）を外します。そのあとで ZIP をダブルクリックして展開すると、確認なしで開けます。
ZIP の名前と場所は、実際のものに読み替えてください。

```bash
xattr -d com.apple.quarantine ~/Downloads/tategaki-xtc-gui-studio_v4.0.4-full_macos-arm64.zip
```

すでに展開してしまった場合は、アプリに対して実行します。

```bash
xattr -dr com.apple.quarantine /Applications/TategakiXTC_GUI_Studio.app
```

Trial版を使う場合は、ZIP名を `tategaki-xtc-gui-studio_v4.0.4-trial_macos-arm64.zip` または
`tategaki-xtc-gui-studio_v4.0.4-trial_macos-intel.zip` に読み替えます。
Intel MacでFull版を使う場合は `tategaki-xtc-gui-studio_v4.0.4-full_macos-intel.zip` です。
Trial版のアプリ名は `TategakiXTC_GUI_Studio_Trial.app` なので、展開後に方法Bを使う場合はアプリのパスも読み替えてください。

ここで「Operation not permitted」と出る場合は、macOS がアプリの変更を止めています。方法Aを使うか、ZIP から方法Bをやり直してください。

**2回目からは、普通にダブルクリックで起動します。** アプリを別の場所へ移しても、確認は最初の1回だけです。

## 最初の操作で出る許可の確認

macOS は、アプリが次のことを初めてするときに許可を求めます。どれも **［許可］** を押してください。
確認の画面には、アプリが使う理由が表示されます。

| 確認が出るとき | 許可しないと |
|---|---|
| X3/X4 へ本を送るとき（「ローカルネットワーク上のデバイスの検出と接続」。macOS 15 以降） | 端末へ送れません |
| 「書類」「デスクトップ」「ダウンロード」フォルダの本を初めて開く・保存するとき | そのフォルダの本を読めず、保存もできません |
| SD カード・USB メモリ、ネットワーク上のフォルダを初めて使うとき | その場所の本を読み書きできません |

あとから変えるときは、「システム設定」→「プライバシーとセキュリティ」の「ローカルネットワーク」「ファイルとフォルダ」で、このアプリをオンにします。

## 以前の設定を取り込む（初回だけ）

`.app` を初めて起動すると、**「以前の設定の取り込み」** という確認が出ます。

- ソース版（`run_gui.command`）で使っていた場合は **［ファイルを選んで取り込む］** を押し、そのフォルダにある `tategakiXTC_gui_studio.ini` を選びます。
  プリセット・画面の配置・最近使ったフォルダなどが引き継がれます
- 初めて使う場合は **［取り込まない］** を押します。初期設定で起動します

> Windows版の「設定引き継ぎツール」（`START_SETTINGS_MIGRATE.bat`、[1章](01-getting-started.md#新しい版へ乗り換えるとき設定引き継ぎツール)）は macOS版にはありません。
> macOS版の `.app` は、新しい版に入れ替えても下の「保存場所」の設定をそのまま使うので、版を上げるたびに引き継ぐ必要はありません。

## 設定・ログ・データの保存場所

macOS版の `.app` は、設定やデータを**アプリの中ではなく**、次のフォルダに保存します
（アプリの中は書き換えられない場所にあることが多く、書き換えると署名も壊れるためです）。

```
~/Library/Application Support/TategakiXTC-GUI-Studio/
```

- 設定ファイル `tategakiXTC_gui_studio.ini`、ログ `logs/`
- 小説URLの登録作品・narou.rs の管理データ（`narou_rs_library/`）・EPUBキャッシュなど

Finder で開くには、メニュー「移動」→「フォルダへ移動…」に上の場所を貼り付けます。
（`~/Library` は Finder では隠れているフォルダです。）

## 同梱しているもの・していないもの

| | 内容 |
|---|---|
| 同梱 | 記事URLの「本文＋画像」「Web表示」に使う Chromium（headless shell） |
| 同梱 | RAR／CBR の展開に使う 7-Zip（`7zz`） |
| 同梱 | 同梱フォント（Noto Sans JP・Noto Serif JP） |
| **同梱していない** | 小説URL（URL→EPUB）で使う Java 21 以上・AozoraEpub3-JDK21・narou.rs（Windows版と同じ。[下記](#小説urlの準備macos)） |

## Windows版と呼び方・場所が違うところ

ほかの章の説明を macOS版で読むときは、次のように読み替えてください。

| ほかの章の書き方（Windows版） | macOS版では |
|---|---|
| `TategakiXTC_GUI_Studio.exe`、`START_TATEGAKI_XTC_GUI.bat` | `TategakiXTC_GUI_Studio.app` |
| エクスプローラーで開く（［保存先を開く］など） | Finder で開く |
| `%LOCALAPPDATA%\TategakiXTC-GUI-Studio\` | `~/Library/Application Support/TategakiXTC-GUI-Studio/` |
| 設定引き継ぎツール（`START_SETTINGS_MIGRATE.bat`） | 初回起動時の「以前の設定の取り込み」（[上記](#以前の設定を取り込む初回だけ)） |
| `narou_rs.exe` | `narou_rs`（拡張子なし） |
| `java.exe` | `bin/java` |
| Windows の Wi-Fi 設定 | macOS の Wi-Fi 設定（メニューバーの Wi-Fi アイコン、または「システム設定」→「Wi-Fi」） |
| 右クリック | 右クリック（トラックパッドは2本指でクリック、または control キーを押しながらクリック） |
| F5（読み直し） | F5。キーボードによっては **fn** キーを押しながら F5 |
| 游明朝などの Windows のフォント | ヒラギノ明朝・ヒラギノ角ゴシックなど、Mac に入っているフォント |

フォントの［参照］は、Font Book で入れたフォントがあれば `~/Library/Fonts` から、なければ Mac 標準のフォント（ヒラギノなど）がある `/System/Library/Fonts` から始まります。

## 小説URLの準備（macOS）

小説URL（[11章](11-narou.md)）で使う Java・AozoraEpub3・narou.rs は、Windows版と同じく別に入れます。
小説URL画面の **［導入手順］** ボタンに、macOS 向けの手順が出ます。要点は次のとおりです。

- **Java 21 以上**: [Adoptium（Temurin）](https://adoptium.net/temurin/releases/) で「macOS」「aarch64」（Apple シリコン）または「x64」（Intel）、「JDK」「21 LTS」の .pkg を入れます。
  インストール後、［自動検出］で見つかります
- **AozoraEpub3-JDK21**: 配布物をホームフォルダの `AozoraEpub3-JDK21` フォルダへ展開します（`~/AozoraEpub3-JDK21`）。
  中に `AozoraEpub3.jar` があれば準備完了です（`.exe` は Windows 用なので不要です）
- **narou.rs**（使う場合）: [配布ページ](https://github.com/Rumia-Channel/narou.rs)の Releases から、Apple シリコンは `narou_rs_mac_arm64.zip`、Intel Mac は `narou_rs_mac_x64.zip` を入れ、
  ホームフォルダの `narou.rs` フォルダへフォルダごと展開します（`~/narou.rs`）。配布ファイル名は変更されることがあるため、Releases の最新版を確認してください

> 「書類」「ダウンロード」フォルダへ置くと、macOS のアクセス制限で失敗することがあります。ホームフォルダの直下に置いてください。

### narou.rs が macOS に止められるとき

macOS 版の narou.rs には開発元の署名がないため、ブラウザでダウンロードしたままだと
「悪質なソフトウェアが含まれていないことを検証できない」と表示され、接続テストや変換が失敗します。
Studio はこの状態を見つけると、エンジンの確認結果に案内を出します。
公式の配布物であることを確かめたうえで、展開したフォルダに対してターミナルで次を実行してください。

```bash
xattr -dr com.apple.quarantine ~/narou.rs
```

## X3/X4 へ送る（macOS）

端末への転送（[16章](16-device-transfer.md)）は、Windows版と同じ手順で使えます。macOS で違う点は次のとおりです。

- 初めて送るときに出る「ローカルネットワーク」の確認で **［許可］** を押してください（macOS 15 以降）。許可しないと送れません
- かんたん接続ガイドの［Wi-Fi設定を開く］は、macOS の「システム設定」の Wi-Fi 画面を開きます
- macOS 14.4 以降は、接続中の Wi-Fi の名前（SSID）をアプリに知らせないことがあります。
  そのとき接続状態の欄に「macOSが表示しません」と出ます。**直接接続**では、端末を既定のアドレス（純正 192.168.3.3／CrossPoint 192.168.4.1）で登録していれば、
  SSID の代わりに **端末がそのアドレスで応答するか**で確かめてから送ります（応答しなければ送りません）
- 送っている間は、Mac がスリープしないようにしています

## バッチ実行（macOS）

バッチ実行（[20章](20-batch-mode.md)）は、`.app` の中の実行ファイルを、ターミナルから呼び出します。

```bash
/Applications/TategakiXTC_GUI_Studio.app/Contents/MacOS/TategakiXTC_GUI_Studio my.ini ~/books/a.epub ~/xtc
echo $?
```

引数・設定 INI・終了コードは 20章と同じです。macOS では終了を待ってから戻るので、Windows の `start /wait` は要りません。

## アンインストール

`TategakiXTC_GUI_Studio.app` をゴミ箱へ入れます。設定やデータも消す場合は、
[保存場所](#設定ログデータの保存場所)のフォルダ（`~/Library/Application Support/TategakiXTC-GUI-Studio/`）も削除します。



→ [README（目次）](../README.md)
