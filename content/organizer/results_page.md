---
date: '2025-10-04T09:00:00+09:00'
draft: false
title: '結果・ログのページ'
category: organizer_guide
weight: 17
ShowToc: true
---

大会が終わったあとの結果・ログのページの作り方です（この手順は今後、運営の道具の `ops results` に合わせて更新します）。

## result.md

`new.py` が生成します（`layout: result`、`result_page: true`、`results_data: <大会 id>`、`contest: <大会 id>`）。
表はすべて contests の `results.yaml` から描画され、結果・ログタブの `/results/<大会 id>/` と「大会横断の比較」の 4 ページも自動で作られます。

### 大会が終わったらやること

1. **success ディレクトリを確認する**（aiwolf サーバ）。本戦中にゲームスコアの配信（[ゲームスコアの配信と集計](./win_rates.md)）を動かしていれば、決着したゲームのログは `<トラック>/log/success/` に揃っています。動かしていなかった場合だけ、次で作ります。

    ```bash
    ssh aiwolf
    cd /var/www/html/aiwolf
    python3 ~/bin/make_success_dir.py 2027/INLG/MainTruck5/log 2027/INLG/MainTruck9/log   # <トラック>/log/success ができる
    ```

1. **success ログを手元に取得**し、`scripts/results/contests/<大会 id>.yaml` を書く（`example.yaml` をコピー）。
1. **ゲーム指標と LLM 相対評価の元ファイルを用意する**（任意。無ければその節は「準備中」と表示される）。
    - ゲーム指標: [aiwolf-nlp-calculate-score](https://github.com/aiwolfdial/aiwolf-nlp-calculate-score) の `run` が出す `data/output/<大会>_<トラック>/team_summary.csv`
    - LLM 相対評価: aiwolf-nlp-llm-judge の出力 `team_aggregation.csv`（モデルごとに 1 つ。複数指定すると平均される）
    - 人手評価: 評価フォームの集計シート（totalling CSV）
1. **results.yaml を生成して contests に push する。**

    ```bash
    python3 scripts/results/build_contest_yaml.py scripts/results/contests/<大会 id>.yaml   # external/aiwolf-nlp-contest-data/contests/<大会 id>/results.yaml に書く
    git -C external/aiwolf-nlp-contest-data add -A && git -C external/aiwolf-nlp-contest-data commit -m "結果: <大会 id>" && git -C external/aiwolf-nlp-contest-data push
    ```

1. **表彰を書く。** 発表後に `results.yaml` の `awards.items` へ追加し、`awards.status` を `published` にします（設定ファイルの `awards:` に書いて再生成しても同じ）。
1. サイト側で submodule の参照を進めてコミットし、`hugo server -D` で確認してからデプロイします。

### results.yaml の項目（抜粋）

| 項目 | 内容 |
|---|---|
| `awards.items[]` | `title` / `title_en` / `team` / `note` / `note_en`（受賞理由や審査員名など任意。チーム名の後ろに括弧書きで出る） |
| `awards.remark` / `remark_en` | 表彰についての補足説明（任意、Markdown 可）。表彰の表の下に段落として出ます。集計の訂正など、受賞そのものは変えずに事情を書くときに使います |
| `availability.human_eval` | `ok` / `none`（未実施）/ `pending`（準備中）。節の文言が切り替わる |
| `availability.llm_judge` | 同上。`posthoc` は「大会後に事後実施」の注記が付く |
| `human_eval_short` | 評価方法ページの表に出す短い表記（例: 学生評価者 3 名） |
| `tracks[].win_rates` | `winrate.py` の出力。`macro`（総合）/ `micro` / `weighted`（構成加重）/ `by_role` |
| `tracks[].game_metrics` | aiwolf-nlp-calculate-score の team_summary.csv から転記した 6 指標 |
| `tracks[].human_eval` | `scale` は `rank`（順位平均）か `rating5`（5 点評点）。`source` は表の上に出る注記 |
| `tracks[].llm_judge` | `models`（評価方法ページの表に出る）/ `source`（表の上に出る注記）/ `posthoc` |
| `tracks[].logs` | ログ一覧の URL（対戦ログ節と対戦ログ一覧ページに出る） |

LLM-as-a-Judge の定量カウントは現在ページから外しています。データは `data/results_archive/quantitative/`（git 管理外）に退避してあり、
復帰させる場合はテンプレートの節を戻す必要があります。
