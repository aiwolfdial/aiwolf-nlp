---
date: '2025-10-04T10:00:00+09:00'
draft: false
title: '人狼知能大会ウェブサイト更新'
category: organizer_guide
---

主に以下のフォルダ内を編集・ページを追加

https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/menu

https://github.com/aiwolfdial/aiwolf-nlp/tree/main/content/page

- 方法

    上記のリポジトリのフォルダに前回大会分のコピーを作成

    今回大会用に日時等修正する

- 注意点

    開発はわざわざブランチは切らなくて良い

    必ずローカルホストで確認してからデプロイ

    ```bash
    hugo server -D
    ```

    ページはmd形式で作成。作成の際には以下のルールを守ること。

    - [公式ルール](https://raw.githubusercontent.com/DavidAnson/markdownlint/main/doc/Rules.md)
    - [カスタム](https://github.com/aiwolfdial/aiwolf-nlp/blob/main/config/custom.markdownlint.jsonc)
