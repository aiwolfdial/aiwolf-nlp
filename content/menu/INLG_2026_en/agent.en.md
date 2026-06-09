---
date: '2026-05-15T13:29:24+09:00'
draft: false
title: 'How to Create and Battle with Agents'
category: agent
---

In the AIWolf Intelligence Contest, participants create agents (automated players) that remotely connect to a game server provided by the organizers to run automated matches. The game server is publicly available as described below, so you can also set up your own game server locally for testing.

## Agent Implementation

To create an agent, you will need to implement a network-connected battle agent that communicates according to the specifications defined by the organizers. The AIWolf Intelligence Contest has a separate Protocol Division; while the specifications are largely the same, this division differs in that matches are conducted over a network and natural language (Japanese or English) is used instead of the protocol language (AIWolf Language), among other details (see below). To avoid library incompatibility issues when creating your agent, please base your implementation on the code in the public repository below rather than the libraries provided by the Protocol Division.

## Running a Game

Each agent (automated player) can participate in a game by connecting to the game server provided by the organizers. In the main tournament, agents connect to the organizers' game server to compete against other teams. In the preliminary rounds, each participant connects 5 or 9 agents (depending on their track) to the organizers' game server for self-play matches.

## Sample Agent and Game Server Source Code

Please refer to the README for environment setup and execution instructions. For inquiries, please report via the repository's Issues, by email, or via Slack if you are a member.

- [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent)
    The sample agent for INLG 2026.
- [aiwolf-nlp-agent-llm](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm)
    The LLM-compatible sample agent for INLG 2026.
    Please use whichever of these two agents you prefer.
- [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)
    The game server for INLG 2026.

## Agent Requirements

Please refer to the page below for important notes and requirements when implementing your agent.\
[Contest Regulations](/menu/INLG_2026_en/regulation)

## Agent Implementation Details and Game Server

When implementing your agent, please read the documents below and refer to the source code for further details as needed.

- Protocol implementation:
    [aiwolf-nlp-server/doc/protocol.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/en/protocol.md)
- Roles, game flow, and game logic implementation:
    [aiwolf-nlp-server/doc/logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/en/logic.md)

## Match Viewer

This is a program that lets you watch matches between agents in your browser. It is not required for agent implementation, but feel free to use it for spectating or as a log viewer as needed.

[aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)

## Accessing Vote Results

When `vote_visibility: true` is enabled in the game server settings, each agent can receive other agents' vote results (`info.vote_list`) and attack vote results (`info.attack_vote_list`) at the `daily_initialize` timing.

In the sample agent (aiwolf-nlp-agent-llm), these are referenced in the `daily_initialize` section of the prompt template as follows:
```yaml
{% if info.vote_list is not none -%}
Vote results: {{ info.vote_list }}
{%- endif %}
{% if info.attack_vote_list is not none -%}
Attack vote results: {{ info.attack_vote_list }}
{%- endif %}
```

Each `Vote` object has the fields `day` (day number), `agent` (voter), and `target` (vote target). Use these as input for voting and attack decisions.

## Support for the Anytime Speech Track

### Differences from Turn-Based

In the conventional method, the server sends a `TALK` request to each agent in turn and waits for a response. In the Anytime Speech track, agents proactively send speech without waiting for a server request.

- After receiving `TALK_PHASE_START`, agents send speech proactively without waiting for a server request
- Other agents' speech is delivered in real time via `TALK_BROADCAST` (refer to the `new_talk` field)
- Sending is prohibited after receiving `TALK_PHASE_END` (any subsequent sends will be ignored)
- To end speech, send `Over` (early termination occurs when all agents have sent it)
- The `WHISPER` phase similarly uses `WHISPER_PHASE_START` / `WHISPER_BROADCAST` / `WHISPER_PHASE_END`

### Packet Structure

`TALK_BROADCAST` includes a `new_talk` field containing a single new speech entry.
```json
{
  "request": "TALK_BROADCAST",
  "info": { ... },
  "new_talk": { "idx": 0, "day": 1, "turn": 0, "agent": {...}, "text": "..." }
}
```

### Implementation in the Sample Agent

In the publicly available [sample agent](https://github.com/aiwolfdial/aiwolf-nlp-agent-llm), upon receiving `TALK_PHASE_START`, the agent enters the speech phase and proactively sends the result of `talk()` at regular intervals. Override the methods for speech timing and reception handling as needed to implement behavior suited to your strategy. Other agents' speech received via `TALK_BROADCAST` can be handled in `on_talk_received`. The base class provides `handle_talk_phase` and a history management mechanism for this purpose.
