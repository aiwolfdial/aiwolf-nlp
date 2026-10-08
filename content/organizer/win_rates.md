---
date: '2026-10-08T10:00:00+09:00'
draft: false
title: 'ゲームスコアの配信と集計'
category: organizer_guide
ShowToc: true
---

勝率やゲーム指標（投票精度、疑われやすさなど）の計算は、公式ツール
[aiwolf-nlp-calculate-score](https://github.com/aiwolfdial/aiwolf-nlp-calculate-score) で行います。
使い方はリポジトリの README と `doc/ja/` に書いてあるので、**手順そのものは README に従ってください。**
このページには、README には書いていない運営側の決めごと（どこで・いつ動かすか、配り方、サイトへの反映）だけをまとめます。

ツールの使い方は 2 つあります。

| 場面 | 動かす場所 | README の節 |
|---|---|---|
| 本戦中の配信（ゲームが決着するたびに全チームの表を更新） | 大会サーバ（`ssh aiwolf`） | 「大会中にゲームスコアを配信する」 |
| 本戦後の集計とチーム別ファイルの生成 | 手元の PC | 「終了したログからゲームスコアを計算する」「チームごとのゲームスコアをまとめる」 |

## 本戦開始前（大会サーバ）

1. `ssh aiwolf` で入り、ホームディレクトリにリポジトリを置きます（初回だけ。2 回目以降は `git pull` で更新）。
   `uv` はサーバに入っています。見つからないときは `export PATH="$HOME/.local/bin:$PATH"` を先に実行してください。

    ```bash
    cd ~ && git clone https://github.com/aiwolfdial/aiwolf-nlp-calculate-score.git && cd aiwolf-nlp-calculate-score && uv sync
    ```

1. 大会ごとの作業ディレクトリ（サーバの設定 yml がある場所。例: `~/inlg2026-2`）で、各トラックの yml に `live_metrics:` を足します。
   `output_dir` は**そのトラックの公開ディレクトリ**にします。参加者はここに置かれる `metrics.ja.txt` / `metrics.en.txt` をブラウザで読みます。

    ```yaml
    live_metrics:
      output_dir: /var/www/html/aiwolf/<年>/<大会>/<トラック>   # 例: /var/www/html/aiwolf/2026/INLG2/MainTruck5
    ```

1. 同じディレクトリで `start_live.sh` を実行します（README のとおり）。**ゲームサーバを起動する前に立てておいて構いません。**
   トラックごとに tmux セッション `aiwolf` のウィンドウが立ち、全試合が終わると自分で止まります。

    ```bash
    cd ~/inlg2026-2
    ~/aiwolf-nlp-calculate-score/scripts/start_live.sh default_en_5.yml default_en_9.yml freeform_en_5.yml
    tmux attach -t aiwolf     # 様子を見る。抜けるのは Ctrl-b d
    ```

配信が動いていれば、決着したゲームの log は `<トラック>/log/success/` に自動でコピーされます。
これは結果・ログページで公開する「決着済みログ」と同じ場所なので、別途 success ディレクトリを作る作業は要りません。

## 本戦終了後（手元の PC）

1. 手元にもリポジトリを置き、`uv sync` します。
1. `scripts/fetch_logs.sh` でサーバから決着済みログと json を取得します。`ssh aiwolf` で繋がることが前提です
   （[運営を始める前に](./preparing.md) の `~/.ssh/config` の設定）。年度は自動判別され、`data/input/<大会>_<トラック>/` に並びます。
1. README のとおり `run` と `teams` を実行します。

    ```bash
    uv run src/main.py run data/input      # 全チームの集計 → data/output/<大会>_<トラック>/
    uv run src/main.py teams data/input    # チーム別ファイル → data/output/teams/
    ```

配信中に出していた全チーム表と、ここで出る値は同じ関数で計算されるので一致します。食い違う場合はログの取りこぼしを疑ってください（`uv run src/main.py check data/input`）。

## 参加者への配布

- 全チームの表（`data/output/teams/<大会>_<トラック>/all_team/`）は配信中と同じ内容なので、Slack のチャンネルにそのまま貼れます。
- チーム別のファイルは `data/output/teams/by_team/<チーム>/` に出場した全トラック分がまとまっています。これを 1 チーム 1 つの zip にして、各チームの Slack DM に送ります。

    ```bash
    cd data/output/teams/by_team
    for t in */; do t="${t%/}"; zip -qr "../../${t}_scores.zip" "$t"; done
    ls ../../*_scores.zip
    ```

Slack の文面は [Slack メッセージ一覧](./slack_message.md) を参照してください。

## サイトへの反映

結果・ログページのゲーム指標は、`run` が出す `data/output/<大会>_<トラック>/team_summary.csv` から転記します。
手順は [人狼知能大会ウェブサイト更新](./edit_website.md) の「大会が終わったらやること」を見てください。

[outlineへ戻る](./outline.md)
[前: 人狼知能人手評価手順](./subjective_evaluation.md)
[次: overview作成手伝い](./overview.md)
