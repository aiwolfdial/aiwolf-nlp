---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: 'サイト更新'
category: organizer_guide
weight: 4
ShowToc: true
---

大会データベースの情報から大会のページを作り（初回）、以後はシートの変更をサイトに反映します。**localhost で確認してから自分で push** します。

## 大会情報入力

[大会定義シート](https://docs.google.com/spreadsheets/d/1NzFe2zl2lPqE9MQSbj_PVA4LMDwuje9Uez7GmGDdORg/edit)の D1 で「**サイト**」を選び、濃い黄色（サイトに必須）の行を埋めます。学会名、学会の URL、学会期間、サイトの言語、日程など です。
英語のページも作る大会は「サイトの言語」を「両方」にし、「大会_en」タブも埋めます。

## 大会データベース更新

シートのメニュー「大会データ → 大会データを更新」を押します。

## サイト更新

aiwolf-nlp のターミナルで実行します。

### 初回（大会のページを作る）

```bash
cd aiwolf-nlp
git pull
bash scripts/contest/sync.sh                                            # 大会データベースの最新を取り込む
python3 scripts/contest/new.py <大会 id> --from <直近の国際大会 id>      # ページ一式を作る（例: --from inlg_2026）
python3 scripts/contest/check.py <大会 id> --from <直近の国際大会 id>    # 直すところを一覧にする
```

- **国内大会も直近の国際大会から作ります。** 国際大会のページが最新のルールと説明を持っているためです。回数・国内 / 国際・対戦言語・論文の有無で変わる文は、雛形が自動で出し分けます。
- 日本語・英語のどちらのページを作るかは「サイトの言語」で決まります。論文投稿の無い大会では論文提出のページを作りません。
- 前回の大会名・学会名などは自動で今回のものに置き換わり、トップの更新情報は空になります（載せるときはコメントを外す）。

`check.py` の結果はこう読みます。

```text
aiwolfdial2027_springjp: 直すところ 1 件（ファイル名:行番号 をクリックするとその行が開きます）

content/menu/aiwolfdial2027_springjp/program.md
  content/menu/aiwolfdial2027_springjp/program.md:9
      未記入 — placeholder '決定次第'
      > プログラムは決定次第掲載します。
```

`ファイル名:行番号` を VS Code のターミナルで Ctrl を押しながらクリックするとその行が開きます。その下が直す理由、`>` が問題の行です。
**プログラムの「決定次第」だけが残れば完了**です。それ以外は直して、もう一度 `check.py` を流します。

### 2 回目以降（シートの変更を反映する）

```bash
bash scripts/contest/sync.sh
```

日付やフォームの URL はシートから自動で入るので、ページを作り直す必要はありません。

## 確認

プレビューのサーバを起動していなければ、別のターミナルで起動します。

```bash
hugo server -D --poll 700ms --port 1313 --baseURL http://localhost:1313/aiwolf-nlp/ --appendPort=false
```

`sync.sh`・`new.py`・`check.py` の最後に、確認するページの URL が出ます。VS Code のターミナルで Ctrl を押しながらクリックすると開きます（VS Code がポートを手元に転送します）。
ファイルを直すと、開いているページが自動で更新されます。

確認すること:

- 埋め込まれたリンク（参加フォーム、学会のページ、各ページへのリンク）がきちんと動くか
- 大会名、日程、学会、トラック、役職などの大会情報に誤りがないか
- 前の大会の文章が残っていないか

## 公開

問題が無ければ commit して main に push します。GitHub Actions がビルドし、数分で公開サイトに反映されます。

```bash
git add -A && git commit -m "feat: 2027 春季国内大会のページを追加" && git push
```

`layouts` の変更など大きな変更はブランチを切ってプルリクエストにします（[大きな変更をするとき](./advanced.md)）。

### 大会一覧の仕切り

トップページの「次回大会」「過去大会」の仕切りは、学会期間の終わりが今日以降かどうかで自動的に入ります。毎朝 6 時（日本時間）にサイトが再ビルドされ、会期が過ぎた翌朝に仕切りが移ります。手で動かす必要はありません。
