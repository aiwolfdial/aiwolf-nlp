---
date: '2026-04-20T14:00:00+09:00'
draft: false
title: 'WSLとLinux'
category: participants_guide
ShowToc: true
---

このページは、開発の土台になる **Linux とは何か**、そして Windows しか使ったことがない人が **なぜ・どうやって Linux を使うのか** を順に説明します。
実際にターミナルを開いてコマンドを打つ方法は、次の [ターミナル操作とコマンド](./about_terminal.md) で扱います。

---

## OS の一種が Linux

**OS（オペレーティングシステム）** は、コンピュータ全体を動かす土台になるソフトウェアです。その OS には、いろいろな種類があります。

* iPhone … **iOS**
* Android スマホ … **Android**
* Windows パソコン … **Windows**
* Mac … **macOS**

これらと並んで、**Linux** という OS があります。今回の開発で土台にするのが、この Linux です。

<svg viewBox="0 0 560 150" xmlns="http://www.w3.org/2000/svg" role="img" style="max-width:560px;width:100%;height:auto;font-family:system-ui,sans-serif">
  <title>さまざまな OS の種類。これらに並んで Linux がある</title>
  <desc>iPhoneはiOS、AndroidはAndroid、WindowsはWindows、MacはmacOS、そしてそれらに並んでLinuxというOSがある</desc>
  <g font-size="12" text-anchor="middle">
    <rect x="14"  y="40" width="96" height="64" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.3"/>
    <text x="62"  y="66" fill="#334155">iPhone</text><text x="62" y="88" fill="#0f172a" font-weight="bold">iOS</text>
    <rect x="124" y="40" width="96" height="64" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.3"/>
    <text x="172" y="66" fill="#334155">Android</text><text x="172" y="88" fill="#0f172a" font-weight="bold">Android</text>
    <rect x="234" y="40" width="96" height="64" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.3"/>
    <text x="282" y="66" fill="#334155">PC</text><text x="282" y="88" fill="#0f172a" font-weight="bold">Windows</text>
    <rect x="344" y="40" width="96" height="64" rx="8" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1.3"/>
    <text x="392" y="66" fill="#334155">Mac</text><text x="392" y="88" fill="#0f172a" font-weight="bold">macOS</text>
    <rect x="454" y="40" width="96" height="64" rx="8" fill="#fff7ed" stroke="#ea580c" stroke-width="1.8"/>
    <text x="502" y="66" fill="#9a3412">開発で使う</text><text x="502" y="88" fill="#9a3412" font-weight="bold">Linux</text>
  </g>
  <text x="280" y="22" text-anchor="middle" font-size="13" fill="#475569" font-weight="bold">OS にはいろいろな種類がある</text>
</svg>

---

## OS が違うと、動くものも違う

iPhone には iPhone でしか遊べないゲームがあり、まったく同じものは Windows では遊べません。OS が違うと、その上で動くソフトの作り方も変わるためです。

Linux も同じで、**Linux でしか動かないシステム** があり、それは Windows では動きません。
そして開発の世界では、この **Linux 環境が非常に多く使われています**。Web サービスやサーバの多くが Linux を前提に作られているため、開発・コーディングを行う側も **Linux 環境で行うのが基本** です。Linux 上で動くことを前提に作られたものは、同じ Linux 環境で開発する方が、手順もコマンドもそのまま通り、つまずきが減ります。

---

## Windows から Linux を使うには

とはいえ、普段使っているのは Windows です。開発のために Linux を使いたい——このとき、どうすればよいでしょうか。

ここで、スマホとパソコンの場合と比べてみます。
iPhone を使っていて Windows も使いたくなったら、Windows のパソコンを **新しく買う** 必要がありました。デバイスそのものが別だからです。

ところが、**Windows を使っていて Linux を使いたくなった場合は、新しいデバイスを買う必要はありません**。Windows の中から、直接 Linux の環境にアクセスできます。
それを可能にするのが **WSL（Windows Subsystem for Linux）** です。**WSL は、Windows から Linux の環境を触るためのツール** です。

<svg viewBox="0 0 560 170" xmlns="http://www.w3.org/2000/svg" role="img" style="max-width:560px;width:100%;height:auto;font-family:system-ui,sans-serif">
  <title>WSLを使うとWindowsの中からLinux環境にアクセスできる</title>
  <desc>大きなWindowsの枠の中に、WSLというツールを通してLinux環境（Ubuntu）が入っている。デバイスの買い替えは不要</desc>
  <rect x="10" y="14" width="540" height="142" rx="10" fill="#eff6ff" stroke="#2563eb" stroke-width="2"/>
  <text x="28" y="38" font-size="13" fill="#1e3a8a" font-weight="bold">Windows（いつもの PC・買い替え不要）</text>
  <rect x="300" y="54" width="226" height="86" rx="8" fill="#fff7ed" stroke="#ea580c" stroke-width="1.5"/>
  <text x="413" y="78" text-anchor="middle" font-size="12" fill="#9a3412" font-weight="bold">WSL（つなぐツール）</text>
  <rect x="320" y="92" width="186" height="38" rx="6" fill="#feffe7" stroke="#ca8a04" stroke-width="1.5"/>
  <text x="413" y="116" text-anchor="middle" font-size="12" fill="#713f12">Linux 環境（Ubuntu）</text>
  <text x="150" y="100" text-anchor="middle" font-size="12" fill="#1e40af">いつもの Windows 操作</text>
  <g stroke="#2563eb" stroke-width="1.6" fill="#2563eb">
    <line x1="232" y1="97" x2="296" y2="97" marker-end="url(#aw)"/>
  </g>
  <defs>
    <marker id="aw" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M2 1 L8 5 L2 9" fill="none" stroke="#2563eb" stroke-width="1.6"/>
    </marker>
  </defs>
  <text x="264" y="90" text-anchor="middle" font-size="10" fill="#1d4ed8">WSL 経由</text>
</svg>

これからは、この **WSL を使って Windows から Linux 環境にアクセスし、開発を行っていきます**。

### 「Linux」「WSL」「Ubuntu」の関係

言葉が混ざりやすいので、一度整理します。

* **Linux** … OS の種類そのもの。
* **Ubuntu** … その Linux の具体的な製品のひとつで、WSLでは既定でUbuntuが入ります。
* **WSL** … その Linux（Ubuntu）を、Windows から使えるようにするツール。

---

## 起動して開発を始める

WSL の起動はかんたんです。

1. **Windows ボタン**（スタートメニュー）を押す
2. **`wsl`** と入力して **Enter**

これでターミナルが開き、Linux の **`/home/ユーザー名`** という場所から操作を始められます。
ここでコマンドを打ったり、VS Code を開いたりすれば、Linux 環境での開発ができます。

> 実際のコマンド操作（ファイルの一覧表示や移動など）は、次の [ターミナル操作とコマンド](./about_terminal.md) で扱います。

---

## 所在地の確認：Windows と Linux はファイルの置き場所が別

はじめてlinuxやwslを使うとここで混乱する人が多いです。

Windows の **エクスプローラー**（フォルダを開くアプリ）を見ると、**ドキュメント・ダウンロード・ミュージック・ビデオ** などがあります。これらは **Windows 環境** のフォルダやファイルです。
一方、**WSL を通して Linux 環境に作ったフォルダやファイルは、この Windows のフォルダの中にはありません**。

たとえば、Windows で作ったファイルが、ある日突然 iPhone の中に入っていることはありません。iPhone で撮った写真が、何もしないのに Windows へ移っていることもありません。**デバイス（環境）が違えば、保存場所も別** だからです。
これと同じで、**WSL で Linux に作ったファイルは Windows 側には保存されておらず、見たければ「Linux のフォルダ」の中を開く必要があります**。

### Linux 側のファイルを開く

エクスプローラーの **左サイドバーを下までスクロール** すると、ペンギンのアイコンで **Linux** という項目があります。そこから、

```
Linux → Ubuntu → home → ユーザー名
```

とたどると、これまでに作ったフォルダやファイルが見えます。
WSL は起動すると `/home/ユーザー名` から始まり、そこで `mkdir`（フォルダ作成）や `git clone` を行うため、作ったものはこの場所に保存されているからです。

<svg viewBox="0 0 440 250" xmlns="http://www.w3.org/2000/svg" role="img" style="max-width:440px;width:100%;height:auto;font-family:system-ui,sans-serif">
  <title>エクスプローラーでWindowsのフォルダとLinuxが別枠で並ぶ</title>
  <desc>左サイドバーに、PCの下のドキュメントやダウンロード（Windows側）と、下にスクロールした先のLinux項目（Ubuntu→home→ユーザー名）が別々にある様子</desc>
  <rect x="8" y="10" width="424" height="232" rx="8" fill="#fafafa" stroke="#cbd5e1" stroke-width="1.5"/>
  <text x="24" y="32" font-size="12" fill="#475569" font-weight="bold">エクスプローラー（左サイドバー）</text>
  <text x="30" y="60" font-size="13" fill="#334155">💻 PC</text>
  <rect x="44" y="70" width="280" height="74" rx="6" fill="#eff6ff" stroke="#2563eb" stroke-width="1.3"/>
  <text x="58" y="89" font-size="12" fill="#1e3a8a">📄 ドキュメント / ⬇ ダウンロード</text>
  <text x="58" y="108" font-size="12" fill="#1e3a8a">🎵 ミュージック / 🎬 ビデオ</text>
  <text x="58" y="130" font-size="11" fill="#1d4ed8">＝ Windows 側のファイル</text>
  <text x="200" y="166" font-size="11" fill="#94a3b8" text-anchor="middle">… サイドバーを下にスクロール …</text>
  <rect x="24" y="176" width="392" height="58" rx="6" fill="#fff7ed" stroke="#ea580c" stroke-width="1.4"/>
  <text x="36" y="196" font-size="13" fill="#9a3412">🐧 Linux → Ubuntu → home → ユーザー名</text>
  <text x="36" y="216" font-size="11" fill="#7c2d12">＝ Linux 側のファイル（作ったものはここ）</text>
</svg>

> アドレスバーに `\\wsl$\Ubuntu\home\ユーザー名` と入力しても、同じ場所を開けます。
> サイドバーに Linux が表示されない場合は、一度 WSL を起動してから Windows を再起動すると現れることがあります。

---

## 補足：Linux の設計思想（なぜ開発で好まれるか）

Linux（のもとになった Unix）には、一貫した設計思想があります。これは次ページのコマンド操作の前提になります。

* **小さい道具を組み合わせる**。1つのコマンドは1つの役割だけを持ち、それらを **つないで** 大きな仕事をする。
* **入出力の扱いを共通にする**。「読む・書く」をどの道具でも同じやり方で扱うため、覚えることが少なくて済む。

この「小さな道具をつなぐ」発想が、次ページで出てくる **コマンドをパイプ（`|`）でつなぐ** 操作にそのままつながります。

---

## 補足：WSL のインストールと起動

すでに WSL が使える場合は読み飛ばして構いません。

### 1. インストール（Windows 10 / 11）

**PowerShell** または **ターミナル** を「**管理者として実行**」で開き、次を実行します。

```powershell
wsl --install
```

これで **WSL2 と Ubuntu** がまとめて導入されます（途中で再起動を求められることがあります）。

### 2. 初回起動とユーザー設定

導入後、スタートメニューで **`wsl`**（または **Ubuntu**）と入力して起動します。
初回起動時に、Linux 用の **ユーザー名とパスワード** を決めます（Windows のログイン情報とは別物です）。

---

## まとめ

* **Linux** は OS の一種。iOS / Android / Windows / macOS と並ぶ存在で、**開発で広く使われている**。
* OS が違うと動くものも違う。多くのシステムが Linux 前提で作られているため、**開発は Linux 環境で行うのが基本**。
* Windows から Linux を使うのに、新しいデバイスは要らない。**WSL を使えば Windows から直接 Linux 環境にアクセスできる**。
* 起動は **Windows ボタン → `wsl` → Enter**。`/home/ユーザー名` から開発を始められる。
* **Windows と Linux はファイルの置き場所が別**。Linux に作ったものは、エクスプローラーの **Linux → Ubuntu → home → ユーザー名** から見る。

次は、この Linux 環境で実際にコマンドを打っていきます。

---

[参加者マニュアルトップへ](../_index.md)\
[背景知識トップへ](./_index.md)\
[次へ（ターミナル操作とコマンド）](./about_terminal.md)
