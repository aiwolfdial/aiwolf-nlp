---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: '大会での対戦方法'
category: participants_guide
---

## 予選の対戦方法

予選は参加登録後に招待されるSlack上で公開されるアドレスに接続することで、対戦できます。\
config.ymlからweb_socketの該当項目を変更したうえで、エージェントを実行してください。

## 本戦の対戦方法

本戦は参加登録後に招待されるSlack上で公開されるアドレスに接続することで、対戦できます。\
本戦では`web_socket.auto_reconnect`を`true`にしてください。\
config.ymlからweb_socketの該当項目を変更したうえで、エージェントを実行してください。\
対戦状況によって大会運営サーバを停止している時間帯があるため、接続エラー(`[Errno 61] Connection refused`)が発生し、自動で再接続を繰り返す可能性があります。

---

以上で大会の対戦方法のまとめを完了します。

---

[参加者マニュアルトップへ](../_index.md)\
[大会トップへ](./_index.md)\
[前へ（エージェントのカスタマイズ方法）](../enhancement/customize_agent.md)\
[次へ（serverの編集・起動方法）](../extras/local_battle_setup.md)
