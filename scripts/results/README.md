# scripts/results — 結果ページ用データの生成

`external/aiwolf-nlp-contest-data/contests/<slug>/results.yaml`（大会データリポジトリ）を作るためのスクリプト群。運用手順は
[運営マニュアル（ウェブサイト更新）](../../content/organizer/edit_website.md) の「結果・ログページ」を参照。

| ファイル | 役割 |
|---|---|
| `server/make_success_dir.py` | aiwolf サーバ側で実行。決着したゲームのログだけを `success/` に集める（サーバの `~/bin/` にも同じものがある） |
| `winrate.py` | success ログからチーム別勝率（総合・役職別・構成加重）を集計して JSON を出す。2024 形式と 2025 以降の形式の両対応 |
| `human_totalling.py` | 人手評価フォームの集計シート（totalling CSV）からチーム別の平均順位を出す |
| `build_contest_yaml.py` | 上記と aiwolf-nlp-calculate-score / aiwolf-nlp-llm-judge の出力をまとめて contests の `results.yaml` を書く |
| `contests/example.yaml` | `build_contest_yaml.py` の設定例 |

2024〜2026 の 7 大会分は、概要論文・発表スライド・評価シートからの転記を含む一回限りの手順で作成した
（作業スクリプトは静岡大学狩野研の `calculate_meta/site_results/` に保管）。以後の大会はこのディレクトリの手順で足す。
