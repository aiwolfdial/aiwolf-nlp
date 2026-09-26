---
date: '2026-09-26T00:00:00+09:00'
draft: false
title: 'Links'
description: 'Official accounts, the log viewer, official repositories, and how to browse past results and logs.'
---

## Official Accounts

- Official X: [@aiwolfdial_nlp](https://x.com/aiwolfdial_nlp) \
    Announcements about the contests and updates to this site.
- Official GitHub: [github.com/aiwolfdial](https://github.com/aiwolfdial) \
    The organization that hosts the repositories of the Natural Language Division.
- AIWolf Project: [aiwolf.org](https://aiwolf.org/) \
    The official website of the AIWolf project as a whole.

## Log Viewer (aiwolf-nlp-viewer)

A viewer for watching and replaying game logs in the browser. No installation is needed; use the hosted version.

- Hosted version: [aiwolfdial.github.io/aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)
- Source code: [aiwolf-nlp-viewer](https://github.com/aiwolfdial/aiwolf-nlp-viewer)

How to use it:

1. **Open a published log directly**: open a "Log list" from [Game Logs by Track](/results/logs) (links for every contest and track) or from a contest's results page, and press "▶ 開く" (open) in the row of the log. The viewer opens with that log loaded.
1. **Choose a bundled log**: on the viewer's [archive page](https://aiwolfdial.github.io/aiwolf-nlp-viewer/archive), choose Select Folder (contest) and then Select Log (file) to view the logs used for the human evaluation of past contests.
1. **Open a local file**: on the same archive page, select a file, or copy the text of a log and press "Paste from Clipboard". Logs from your own server can be viewed this way too.
1. **Share by URL**: a link of the form `https://aiwolfdial.github.io/aiwolf-nlp-viewer/archive?url=<URL of the log>` opens that log (published log server only).

## Official Repositories

Repositories used for agent development. Please refer to each README for setup and usage.

| Repository | Description |
|---|---|
| [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent) | Sample agent |
| [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm) | Sample agent using an LLM |
| [aiwolf-nlp-common](https://github.com/aiwolfdial/aiwolf-nlp-common) | Common package for agents |
| [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server) | Game server |
| [aiwolf-nlp-viewer](https://github.com/aiwolfdial/aiwolf-nlp-viewer) | Log viewer (see above) |
| [aiwolf-nlp-llm-judge](https://github.com/aiwolfdial/aiwolf-nlp-llm-judge) | LLM-as-a-Judge relative evaluation of game logs |

## How to Browse Past Results and Logs

Results and logs of the contests since 2024 are collected on [Results & Logs](/results).

- **Pick a contest**: open a contest card on the Results & Logs page to reach its results page. The same page is also reachable from "Results & Logs" in each contest's menu.
- **Page structure**: official results (awards), win rates, game metrics, human evaluation, LLM-as-a-Judge (relative evaluation) and game logs, with a table of contents at the top. Each section starts with a short explanation of the metric.
- **Across contests**: the "Across contests" group at the top of the Results & Logs page has four pages: awards by contest, evaluation methods (judges and models), agreement with human evaluation, and [game logs by track](/results/logs).
- **View or save logs**: [Game Logs by Track](/results/logs) or the "Game Logs" section at the end of each results page links to the log listings on the public log server. In a listing, "▶ 開く" opens a log in the viewer, "⬇ 保存" saves one file, and "⬇ zip" in a folder row downloads the whole folder as a zip.
