---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: '開発環境の準備'
category: participants_guide
---

こちらのページでは、エージェントを動かすために必要な **Python環境** を準備します。
初めてPythonを使う方でも進められるように、できるだけシンプルな手順にしています。

> Windowsで開発する方は、先に [WSLとターミナル](../background/about_wsl.md) をひととおり読んで、Ubuntu ターミナルを用意しておくとスムーズです。

---

## Python 3.11以上を用意する

サンプルエージェントは **Python 3.11以上** が必要です。まずは手元のPythonのバージョンを確認しましょう。

```bash
python3 --version
```

`Python 3.11.x` のように表示されれば問題ありません。
もし古いバージョンしか入っていない場合は、次の手順でインストールします。

### Ubuntu / WSL の場合

```bash
sudo apt update
sudo apt install -y python3 python3-venv
```

それでもバージョンが古い場合は、新しい Python を追加でインストールします。

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-venv
```

### macOS の場合

[Homebrew](https://brew.sh/index_ja) を使うのがおすすめです。

```bash
brew install python@3.11
```

---

## uv をインストールする

本プロジェクトは **[uv](https://docs.astral.sh/uv/)** というツールを使って Python 環境を整えます。
`uv` は依存関係のインストールを自動化してくれる高速なツールで、`pip` や `venv` の操作を覚える必要がなくなります。

次のコマンドでインストールできます。

```bash
# Linux / macOS / WSL
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

インストール後、ターミナルを開き直して次のコマンドでバージョンを確認します。

```bash
uv --version
```

バージョン番号が表示されれば準備完了です。

---

## uv を使わずに進めたい場合

会社や学校の環境で `uv` が使えない場合は、従来の `venv` + `pip` でも開発できます。
次のページでは両方の手順を併記しているので、都合のよい方を選んでください。

---

[参加者マニュアルトップへ](../_index.md)\
[準備トップへ](./_index.md)\
[次へ（リポジトリのクローン）](./clone_repo.md)
