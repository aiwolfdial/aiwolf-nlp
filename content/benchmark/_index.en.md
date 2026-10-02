---
date: '2026-10-02T00:00:00+09:00'
draft: false
title: 'Benchmark'
description: 'Two benchmarks run by the organizers: agents built on public LLMs playing under the contest rules, and LLM judges measured by their agreement with human evaluation.'
menu_id: benchmark
---

Separately from the contest results, the organizers run two benchmarks under identical conditions.

- **Agents**: the official sample agent with its LLM swapped for each public model, playing under the contest rules, ranked by the LLM-as-a-Judge relative evaluation, with the count judge's evaluation alongside. Useful for comparing the LLMs that contest agents are built on.
- **Relative judge**: how closely each public LLM, used as the ranking judge of the contests, agrees with the human evaluation (per-rater rankings) of past contests. This is the basis for choosing the judge model used in the contests.
- **Count judge**: a different kind of LLM judge that counts deduction and addition events per utterance, with its agreement with the same human evaluation.
- **Game scores**: judge-independent scores computed from the game records alone.
- **Review**: a cross-analysis of the relative evaluation and the game scores.
