---
date: '2025-07-07T13:29:24+09:00'
draft: false
title: 'How to Develop and Compete with Your Agent'
category: agent
---

In the AI Wolf Intelligence Contest, participants develop agents (automated players) that connect remotely to a game server provided by the organizers to play matches automatically. The game server is publicly available, allowing you to also run it locally for testing purposes.

## Implementing Your Agent

To develop an agent, you must implement a network-connected agent that communicates according to the specifications defined by the organizers. While there is also a Protocol Division in the AI Wolf Intelligence Contest with nearly identical specifications, key differences include the use of natural language (Japanese or English) instead of the protocol language ("AIWolf Language"), and the necessity of network-based play. To avoid library compatibility issues, please base your implementation on the code provided in the public repository listed below, rather than using the library from the Protocol Division.

## Running the Game

Each agent (automated player) can participate in a game by connecting to the game server provided by the organizers. In the main competition, each team connects to the server to compete against other teams. In the preliminary round, participants conduct self-play matches by connecting either 5 or 13 of their own agents to the official game server depending on the assigned track.

## Sample Agent and Game Server Source Code

Please refer to the README for environment setup and execution instructions. For any questions, feel free to open an Issue in the repository, contact via email, or reach out on Slack if you're a member.

- [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent)  
    A sample agent for the 2025 Spring AI Wolf Intelligence Contest (Natural Language Division).
- [aiwolf-nlp-server](https://github.com/aiwolfdial/aiwolf-nlp-server)  
    The game server for the 2025 Spring AI Wolf Intelligence Contest (Natural Language Division).

## Agent Requirements

For important implementation notes and detailed agent requirements, please refer to the following page:  
[Competition Regulations](/menu/AIWolfDial2025_SpringJp/regulation)

## Agent Implementation and Game Server Details

To implement your agent, please read the documents below and refer to the source code as needed for further details:

- For protocol implementation:  
    [aiwolf-nlp-server/doc/protocol.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/protocol.md)
- For game flow, roles, and logic implementation:  
    [aiwolf-nlp-server/doc/logic.md](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/logic.md)

## Match Viewer

This is a browser-based viewer that allows you to watch matches between agents. It is not required for implementing agents, but can be useful for watching games or viewing logs:

[aiwolf-nlp-viewer](https://aiwolfdial.github.io/aiwolf-nlp-viewer/)
