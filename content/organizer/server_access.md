---
date: '2025-10-04T08:00:00+09:00'
draft: false
title: '大会サーバへの接続'
category: organizer_guide
weight: 16
---

予選・本戦を動かす人は、大会サーバに SSH で入れるようにします。

予選・本戦を動かす人は、大会サーバに SSH で入れるようにします。

1. 自分の PC で鍵のペアを作り、公開鍵を運営の人に渡します（参考: [SSH鍵を生成するコマンドと全手順解説](https://qiita.com/to3izo/items/9b5b80430e43cd3c4e3c)）。
1. 運営の人が公開鍵をサーバの `~/.ssh/authorized_keys` に追記します。
1. `~/.ssh/config` に次を書きます。IP アドレスは運営の人に聞いてください。

    ```text
    Host aiwolf
    HostName [人狼サーバの IP アドレス]
    User aiwolf
    IdentityFile ~/.ssh/[秘密鍵のファイル名]
    ```

1. `ssh aiwolf` で接続できることを確かめます。
