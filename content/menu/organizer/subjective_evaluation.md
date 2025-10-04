# 人狼知能人手評価手順
<details>
<summary>本戦が完了次第、本戦で行われた試合の中から適当な試合数ピックする</summary>

[aiwolf-nlp-log-picker](https://github.com/aiwolfdial/aiwolf-nlp-log-picker)
各チームの出場回数と役職担当回数がなるべく均一になるように設定済み

</details>

<details>
<summary>国際大会の場合、ピックした試合のログを日本語へ翻訳する</summary>

[aiwolf-nlp-log-translator](https://github.com/aiwolfdial/aiwolf-nlp-log-translator)

</details>

<details>
<summary>ピックしたログファイルは.log形式であることを確認してログビュアーへ更新</summary>

[aiwolf-nlp-viewer](https://github.com/aiwolfdial/aiwolf-nlp-viewer)
- `aiwolf-nlp-viewer/static/assets/` 以下に保存
- 5人村ログフォルダ：`_truck5`、13人村ログフォルダ：`_truck13` で識別
- 国際大会の場合は英語版も更新：`_en` で識別

</details>

<details>
<summary> 評価者へ配るGoogleFormの作成</summary>

フォームの作成はこちらの
[スプレッドシート](https://docs.google.com/spreadsheets/d/1VQLYCpSdBoyq1TxWM9OeoZue4oXOtPjFTQEpDMKnf98/edit?usp=sharing) から AppScripts を実行。

1. スプレッドシートに評価用のログファイルリンクを追加
   → `log_link_5`, `log_link_13` の A列に、行ごとに `http` から始まるゲームログのリンクを記述
   ※ `log_link13` シート参考。

2. コード内該当部分の修正
   - 7行目：`playerNum`
   - 24行目：`sheetName`

3. `createFormMain` を実行

分担評価も可能：[参考フォーム](https://docs.google.com/forms/d/1dLSN6w_gLY7MZeUxOtjVfWIj8cJn4GrBEgH0ZHqD5tc/edit)

</details>
    
<details>
<summary>slackで案内</summary>
    GoogleFormのリンクを評価者へ配布する<br>
</details>

<details>
<summary>結果集計</summary>

[5人村分析](https://docs.google.com/spreadsheets/d/19LyLTa02Sv2CSXgGT4vA6PpOBDRpAxprxeWU_6qTMW8/edit?usp=sharing)

- `log_link` シートを作成
  A列に行ごとに `http` から始まるゲームログのリンクを記述
  ※ `log_link` シート参考。
- `split.gs`（`createGameSpreadSheet`）, `totalling.gs`（`main`）を実行
- `totalling.gs` で生成された `totalling` シートから各評価項目ごとのチームのスコア平均をまとめた**総合評価の表**を作成。
  `-A` や `-B` など複数エージェントを出場させたチームがいた場合は、それらを**統合させた場合の表も作成**する。
  詳細はリンクの `totalling` シート参照。

[13人村分析](https://docs.google.com/spreadsheets/d/1qZQjjameUV0dH41rJBb1l2jLAqbswDGhPKPSrfrpnGg/edit?usp=sharing)

- `log_link` シートを作成
  A列に行ごとに `http` から始まるゲームログのリンクを記述
  ※ `log_link` シート参考。
- `split.gs`（`createGameSpreadSheet`）, `totalling.gs`（`main`）を実行
- `totalling.gs` で生成された `totalling` シートから各評価項目ごとのチームのスコア平均をまとめた**総合評価の表**を作成。
  `-A` や `-B` など複数エージェントを出場させたチームがいた場合は、それらを**統合させた場合の表も作成**する。
  詳細はリンクの `totalling` シート参照。

</details>

<details>
<summary>評価者アンケートの実施</summary>

[こちら](https://docs.google.com/forms/d/16gtDxyZttEbWw7cErXPTTNV-_UdK-Z5h0QCB-rYYjKY/edit)を適宜編集して配布。
</details>

<details>
<summary>※ 備考：gsコードの使いかた</summary>
    
    拡張機能→AppScript
    
    該当コードエディタに移動後実行をクリック
    
    初回実行の場合：
    
    承認が必要です：権限を確認
    
    アカウントの選択：kanolab.share@gmail.com
    
    このアプリはGoogleで確認されていません：詳細→無題のプロジェクト（安全ではないページ）に移動
    
    無題のプロジェクトがGoogleアカウントへのアクセスを求めています：すべて選択→続行
</details>
