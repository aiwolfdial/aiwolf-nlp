---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: '事前準備'
category: participants_guide
---

## 開発前に揃えておきたいもの

人狼知能大会のエージェント開発では **Python 3.11以上** が必須です。  
Pythonのバージョンが古いと、依存ライブラリのインストールや実行時にエラーが出ることがあります。  
まずは、Python 3.11 以降の環境を整えることから始めましょう。

---

### Python と仮想環境の準備

エージェントの開発には Python 3.11 以上が必要です。  
まだインストールしていない場合は、次の手順で環境を整えましょう。

```bash
# システムを最新状態に更新
sudo apt update

# Python コマンドを python3 と同じにする
sudo apt install -y python-is-python3

# Python の仮想環境を作るためのツールをインストール
sudo apt install -y python3-venv
```

---

### コマンドの意味を簡単に解説

| コマンド                                    | 説明                                                           |
| --------------------------------------- | ------------------------------------------------------------ |
| `sudo apt update`                       | パッケージ情報を最新に更新します。新しいソフトを入れる前の基本操作です。                         |
| `sudo apt install -y python-is-python3` | `python` コマンドを `python3` と同じ動作にします。これで `python` と入力するだけでOK。  |
| `sudo apt install -y python3-venv`      | Python の仮想環境（venv）を作るための機能をインストールします。プロジェクトごとに環境を分けるために重要です。 |

---

### Python のバージョンを確認しよう

次のコマンドで、Python が正しくインストールされているか確認します。

```bash
python --version
```

結果の例：

```bash
Python 3.11.9
```

上記のように **Python 3.11 以上** が表示されればOKです。
もし 3.10 以下の場合は、以下のように新しいバージョンをインストールしてください。

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv
```

その後、`python3.11 --version` でバージョンを再確認しましょう。

---

### まとめ

* 人狼知能エージェントの開発には **Python 3.11 以上が必須**
* `python3-venv` で仮想環境を使えるようにしておく
* 以降の手順（クローンやAPI設定など）はこの環境で進めます

---

以上で事前準備の解説を完了します。

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[前へ（事前準備）](../overview/aiwolfdial_repo.md)\
[次へ（リポジトリのクローン）](./clone_repo.md)
