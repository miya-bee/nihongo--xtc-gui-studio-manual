# 20. バッチ実行（コマンドライン）

ウィンドウを出さずに、コマンドラインから XTC / XTCH へ変換する機能です。
ファイル・フォルダのほか、URL（なろう等のWeb小説・青空文庫の図書カード・Web記事）も指定できます。
決まった設定で何冊もまとめて変換したいときや、本棚管理アプリなど他のプログラムから呼び出すときに使います。

```
TategakiXTC_GUI_Studio.exe <ini> <in> [<in> ...] <out> [オプション]
```

| 引数 | 内容 |
|---|---|
| `ini` | 設定ファイル。Studio の設定 INI をコピーして使えます（[後述](#設定ini)） |
| `in` | 変換元。ファイル／フォルダ／`http(s)://` の URL。複数指定できます |
| `out` | 出力先フォルダ。入力が1件のときは `D:\out\book.xtch` のように出力ファイル名も指定できます（拡張子で形式が決まります） |

第1引数が `.ini` で終わるとき、または `--batch` を付けたときにバッチ実行になります。
引数なしで起動した場合は、これまでどおり画面が開きます。

## 例

```
:: EPUB 1冊
TategakiXTC_GUI_Studio.exe my.ini D:\books\a.epub D:\xtc

:: フォルダごと（中の変換対象を1つずつ変換し、D:\xtc に書く）
TategakiXTC_GUI_Studio.exe my.ini D:\books D:\xtc

:: Web小説（小説URL画面と同じ取得方法）
TategakiXTC_GUI_Studio.exe my.ini https://ncode.syosetu.com/n0000aa/ D:\xtc

:: 青空文庫の図書カード
TategakiXTC_GUI_Studio.exe my.ini https://www.aozora.gr.jp/cards/000148/card789.html D:\xtc

:: Web記事を、名前を付けて XTCH で
TategakiXTC_GUI_Studio.exe my.ini https://example.com/post D:\xtc\memo.xtch
```

> **Windows での注意** `TategakiXTC_GUI_Studio.exe` は画面を持つアプリなので、`cmd` から
> そのまま実行すると終了を待たずに戻ります（終了コードも受け取れません）。
> 次のように待って呼び出してください。
>
> ```
> start /wait "" TategakiXTC_GUI_Studio.exe my.ini a.epub D:\xtc
> echo %ERRORLEVEL%
> ```
>
> PowerShell では `Start-Process -Wait -PassThru`、他のプログラムから呼ぶときは終了を待つ呼び出し方を使うか、
> `--result-json` のファイルで結果を読んでください。

## コマンドラインオプション

| オプション | 内容 |
|---|---|
| `--format xtc\|xtch\|both\|xtch_v2\|both_v2` | 出力形式（INI の `output_format` を上書き）。`both` は XTC・XTCH、`both_v2` は XTC・XTCH v2 |
| `--conflict rename\|overwrite\|error` | 同名ファイルがあるときの扱い |
| `--name 名前` | 出力ファイル名（拡張子なし。入力が1件のときのみ） |
| `--url-mode auto\|novel\|article\|aozora` | URL の取得方法（[後述](#urlの振り分け)） |
| `--json` | 標準出力へ JSON Lines で進捗と結果を出す（他のアプリから呼ぶとき用） |
| `--quiet` / `-q` | 標準エラーへの進捗表示を止める |
| `--verbose` / `-v` | 外部エンジン（AozoraEpub3 / narou.rs）の出力も表示する |
| `--dry-run` | 何も取得・変換せず、解釈した内容だけを表示する |
| `--log ファイル` | ログをファイルへも書く |
| `--result-json ファイル` | 結果の要約を JSON で書く |
| `--keep-temp` | URL 取得の一時ファイルを消さない |
| `--version` | 版を JSON で1行表示して終了する |
| `--help` / `-h` | 使い方を表示する |

## 出力と終了コード

- 標準出力: 変換できたファイルのパスを1行ずつ（`--json` のときは JSON Lines）
- 標準エラー: 進捗とログ

| 終了コード | 意味 |
|---|---|
| 0 | すべて成功 |
| 1 | 失敗（変換エラー、入力が見つからない） |
| 2 | 一部だけ失敗（複数入力のうち一部、またはフォルダの中の一部） |
| 3 | 引数・INI の誤り |
| 4 | URL の取得失敗、または外部エンジンが見つからない |
| 5 | 変換は済んだが、`--result-json` の結果ファイルを書けなかった |
| 130 | 中断（Ctrl+C） |

### フォルダを入力にしたとき

- フォルダの中の変換対象（[一括変換](12-folder-batch.md)と同じ選び方）を1つずつ変換し、**指定した出力先**へ書きます。
  入力フォルダには書きません
- 出力名は一括変換と同じく、サブフォルダの名前を前に付けた平らな名前になります
  （`D:\books\著者\本.epub` → `D:\xtc\著者~~本.xtc`）
- `--name` は、フォルダの中の変換対象が1つのときだけ使います

## 設定INI

**Studio の設定 INI（`tategakiXTC_gui_studio.ini`）をコピーして編集する**のがいちばん確実です。
画面と同じキー名がそのまま使えます。書かなかったキーは既定値になるので、
変えたい項目だけの短い INI でも動きます。

```ini
[General]
font_file=NotoSansJP-SemiBold.ttf
font_size=28
line_spacing=44
writing_mode=vertical
profile=x4
output_format=xtch
```

- 保存先（`output_dir`）・変換対象（`target`）など、実行のたびに変わる値は INI にあっても使わず、
  コマンドラインの `in` / `out` を使います
- 手書きの INI では、パスの `\` は1本のままで書けます（`C:\Fonts\a.ttf`）。
  Studio が書いた INI に手でパスを足すときは、`\\` と2本重ねて書いてください
- 値の後ろに空白を空けて `; コメント` を書けます（`a;b` のように空白の無い `;` は値の一部です）
- 数値の項目に `inf` `nan` などを書くと、引数・INI の誤り（終了コード3）になります。
  数値でない文字は、警告を出して既定値を使います
- 文字コードは UTF-8（BOM 付きも可）。CP932 も読めます
- 書籍情報ダイアログで作品ごとに保存した書名・著者・表紙画像の設定は、バッチ実行では使いません
  （INI に書いたキーだけが有効です）

### `[batch]` セクション（URL取得と外部エンジン）

URL を指定するときの設定です。**書かなかった項目は、「小説URL」画面で最後に保存した設定を使います**
（Java・AozoraEpub3・narou.rs の場所、取得方式、挿絵の扱い）。画面で一度設定してあれば、
INI にはほとんど何も書かなくて済みます。

```ini
[batch]
url_mode=auto
fetch_engine=aozora_direct
java_path=C:\Program Files\Java\jdk-21\bin\java.exe
aozora_root=D:\tools\AozoraEpub3
```

| キー | 内容 |
|---|---|
| `url_mode` | `auto`（既定）／`novel`／`article`／`aozora` |
| `use_saved_engine_settings` | `false` にすると「小説URL」画面の保存設定を使わない |
| `fetch_engine` | `aozora_direct`（AozoraEpub3直接）／`narou_rs` |
| `java_path` `aozora_root` `aozora_profile_path` `narou_rs_path` | 外部エンジンの場所 |
| `illustration_policy` | `inherit`（既定）／`include`／`exclude` |
| `image_optimization` | `auto`（既定）／`off` |
| `keep_epub_dir` | 指定すると、取得した EPUB のコピーをそのフォルダへ保存する |
| `process_timeout_seconds` | 外部エンジン1回あたりの制限時間（0 は無制限） |
| `narou_allow_settings_change` | `true` で、Studio 管理外の narou.rs プロジェクトの設定変更を許可する |
| `article_mode` | Web記事: `text`（既定）／`text_images` |
| `article_full_page` | Web記事で全ページから抽出するとき `true` |
| `article_browser_session` | Web記事をブラウザ経由で取得するとき `true` |
| `aozora_source_mode` | 青空文庫: `html_then_text`（既定）／`text_only` |
| `aozora_br_mode` | 青空文庫 HTML の改行: `blank_line`（既定）／`single_break` |
| `format` | 出力形式（`--format` の代わり） |

### URLの振り分け

`url_mode=auto`（既定）では、URL を次の順に振り分けます。

1. 青空文庫の図書カード（`aozora.gr.jp/cards/…/card…html`）→ 作品一覧から作品を特定して本文を取得
   （Java は不要。初回だけ作品一覧をダウンロードして保存します）
2. 小説サイトとして対応している URL（小説家になろう・カクヨム・ハーメルン・アルファポリス等）
   → AozoraEpub3 / narou.rs で EPUB を作り、そこから変換
3. それ以外 → Web記事として本文を抽出して変換

`--url-mode` で強制できます（対応外のサイトを `novel` で試す、なろうの URL を記事として読む、など）。

### 外部エンジンについて

- Web小説の取得には Java 21 と AozoraEpub3-JDK21（narou.rs 方式では narou.rs も）が必要です。
  見つからない場合は終了コード4と、指定すべきキー名を含むメッセージを出します
- narou.rs 方式は、画面と同じ管理フォルダ・登録作品データを使います。初回取得か差分更新かの判断も同じです。
  ただし**確認ダイアログを出せない**ため、Studio 管理外の narou.rs プロジェクトの設定を書き換える必要があるときは、
  `narou_allow_settings_change=true` を書いたときだけ進みます（既定では中止して理由を表示します）
- 取得した EPUB は、一時フォルダで XTC へ変換したあと削除します。残したいときは `keep_epub_dir` を指定します

## `--json` の出力

1行1イベントの JSON です。最後の行は必ず `summary` です（引数・INI の誤りや想定外のエラーのときも出します）。

```json
{"event": "log", "level": "info", "message": "..."}
{"event": "progress", "current": 500, "total": 1000, "message": "..."}
{"event": "converted", "path": "D:\\xtc\\book.xtc", "source": "D:\\books\\a.epub"}
{"event": "error", "source": "...", "message": "...", "exit_code": 4}
{"event": "summary", "exit_code": 0, "run_id": "…", "total": 1, "succeeded": 1, "partial": 0, "failed": 0, "cancelled": 0, "files": {"succeeded": 1, "failed": 0}, "converted_files": ["..."], "errors": [], "result_json": {"path": "...", "written": true, "error": ""}}
```

- `total = succeeded + partial + failed + cancelled`（入力の単位）。フォルダの中の一部だけ失敗した入力は `partial` に数え、
  ファイル単位の件数は `files` に入ります
- `run_id` は実行ごとに変わります。`--result-json` のファイルにも同じ値が入るので、今回の結果かを確かめられます
- `--result-json` のファイルは、実行の始めに前回のものを消し、`summary` より先に書きます。
  書けなかったときは `result_json.written` が `false` になり、変換が成功していても終了コードは5です
- 呼び出し側は `--version` の `batch_api`（現在は3）で、コマンドラインの仕様の版を確認できます

## できないこと

- 記事URLの「Web表示」（ブラウザで見えたままを撮影する方式）
- 小説URL画面の登録作品の管理、続きだけのXTC（[11章](11-narou.md)）。バッチ実行は1 URLずつ取得して全体を変換します

→ [README（目次）](../README.md)
