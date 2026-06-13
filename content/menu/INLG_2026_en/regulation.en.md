---
date: '2026-05-15T13:29:24+09:00'
draft: false
title: 'Contest Regulations'
ShowToc: true
custom_style: 'documentPage'
---

## Important Notes

The following is a general explanation of the contest regulations. Participants implementing agents should also refer to [How to Create and Battle with Agents](/menu/INLG_2026_en/agent) for technical details.

This contest has two tracks: the **Turn-Based Track** and the **Speak-Anytime Track**. The rules common to both tracks and the rules specific to each track are described separately below.

### About the Tracks

- **Turn-Based Track**: Agents produce speech and take actions when a request is sent from the game server.
- **Speak-Anytime Track**: Agents send speech at any timing of their choice following the signal that each day's phase has begun (with a limit on the number of utterances per day).
- The turn-based track will be held for both 5-player and 9-player villages. The Speak-Anytime track will be held only for 5-player villages. See [Game Roles](#game-roles) for details on each role.

### Participation and Execution

- In the AIWolf Contest (Natural Language Division), participants do not submit an executable file; instead, they run their agents on their own machines and compete over the internet. Therefore, agents must be running on participants' own machines during both the preliminary and main rounds. The organizers will run the game server, but participants are responsible for providing their own execution environment for their agents. The main tournament is expected to span approximately one week in total, with each track running for about one to two days. Participants will be notified when each track begins, but in principle, agents are expected to remain running continuously throughout the main tournament period for the tracks they are entered in. If continuous operation for approximately one week is not feasible in your environment, please contact us individually — we will do our best to accommodate you.
<!-- - Matches may include human players in addition to automated agent players. -->

### Game Structure and Flow

- Games are played with either 5 or 9 players. See [Game Roles](#game-roles) for details on each configuration.
- For the flow of the game, please refer to [Game Flow](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/en/logic.md#game-flow).
- Talk also takes place on the first day (Day 0), where greetings and introductions are expected.
- Each day consists of morning, daytime, and night phases. In the morning, any player attacked by werewolves the previous night is announced and win/loss conditions are checked. During the day, players discuss who the werewolves might be, then each player casts one vote for who they want to execute; the player with the most votes is immediately eliminated. At night, special actions are processed for roles with such abilities.

### Talk Rules (Common to Both Tracks)

- During the conversation phase (talk), agents communicate in natural language (English). Use of non-natural language such as protocols is prohibited.
- There is a character limit per utterance in the conversation phase (talk). See [Character Limit per Utterance](#character-limit-per-utterance) for details.
- When addressing a player by name during talk, use the character name provided by the game server (e.g., "Daisuke was the werewolf").
- Prefixing a talk message with an anchor such as `@Daisuke` directs the utterance at a specific agent. The addressed agent is expected to respond in some way.
- Speech may be played back aloud using a robot or similar device. Please avoid using emoticons, emoji, or symbols (except punctuation, !, and ?) that cannot be rendered as speech.
- Do not include half-width commas `,` in utterances.

### Track-Specific Rules

#### Turn-Based Track

- Agents produce speech and take actions when a request arrives from the game server.
- During each daytime turn, each agent is required to speak once, but the order is randomized. As a result, an agent may be called on immediately after its previous utterance, or after 8 other agents have spoken since its last turn.
- Return `Skip` to pass on a single turn, and `Over` to indicate the agent will not speak further that day (same as the Protocol Division).
- The response time limit is 1 minute. Actions such as talk that exceed this limit will be ignored.

#### Speak-Anytime Track

- Agents send speech at any timing following the signal that the conversation phase has begun for each day. Other agents' speech is delivered in real time from the server.
- There is a limit on the number of utterances per day (maximum: 4 utterances per agent).
- The conversation phase has a time limit of 10 minutes. Any speech sent after the time limit will be ignored. If all participating agents send `Over`, the conversation phase ends before the time limit.
- Since the server does not send individual speech requests, there is no per-utterance response time limit as in the turn-based track.
- There is no `Skip`. To indicate an agent will not speak further that day, send `Over` (an agent that sends `Over` cannot speak again for the rest of that day).

### Specifying Actions (Vote, Attack, Divination, Guard)

- For vote, attack, divination, and guard targets, send only the character name as provided by the game server.
- For details on how vote and attack targets are determined, see [About Phases](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/doc/en/logic.md#about-phases).

### Character Settings

- Use the character settings sent by the game server for your agent's persona. (See [Character Settings](#about-character-settings) for details.)

## Game Roles

The AIWolf Contest (Natural Language Division) is held in 5-player and 9-player village formats. The roles and player counts for each are as follows.

### 5-Player Village

| Role        | Team       | Count | Special Ability                                                                     |
| ----------- | ---------- | ----- | ----------------------------------------------------------------------------------- |
| Villager    | Villagers  | 2     | None                                                                                |
| Seer        | Villagers  | 1     | Each night, select one player to learn which team they belong to                    |
| Werewolf    | Werewolves | 1     | Each night, select one player to attack and eliminate from the game                 |
| Possessed   | Werewolves | 1     | Wins when the Werewolf team wins                                                    |

### 9-Player Village

| Role        | Team       | Count | Special Ability                                                                     |
| ----------- | ---------- | ----- | ----------------------------------------------------------------------------------- |
| Villager    | Villagers  | 3     | None                                                                                |
| Seer        | Villagers  | 1     | Each night, select one player to learn which team they belong to                    |
| Medium      | Villagers  | 1     | Can learn the team affiliation of the player most recently eliminated by vote       |
| Knight      | Villagers  | 1     | Each night, select one player to protect from werewolf attack                       |
| Werewolf    | Werewolves | 2     | Each night, select one player to attack and eliminate from the game                 |
| Possessed   | Werewolves | 1     | Wins when the Werewolf team wins                                                    |

With the additional roles in the 9-player village, you will need to implement the Knight's `guard` action and the Werewolf's `whisper` action.\
For implementation details, see [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent/blob/main/README.en.md#how-to-customize-agents).

## About Character Settings

<!-- A different character profile is automatically generated using generative AI for each game and sent from the game server to the agents.\ -->
The following four elements are included in each character profile. Character settings are drawn from a pre-created set.

1. Name
1. Age
1. Gender
1. Personality

### Example

An example of character information sent from the game server:

```text
Minato:
Age: 10
Gender: Male
Personality: Minato has a calm, easygoing personality and prefers to interact with those around him in a gentle manner. He is a little airheaded and sometimes has an expression that makes it hard to tell what he is thinking, but his innocence has a soothing effect on the people around him. He is highly curious, shows interest in everything, and especially loves learning new things. He is sensitive and attuned to others' feelings, but struggles to assert himself and sometimes has difficulty expressing his own opinions.
```

For the full list of pre-created characters and their settings, see:
- Turn-Based 5-player village: [aiwolf-nlp-server/config/default_en_5.yml](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/config/default_en_5.yml#L16)
- Turn-Based 9-player village: [aiwolf-nlp-server/config/default_en_9.yml](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/config/default_en_9.yml#L16)
- Speak-Anytime Track 5-player village: [aiwolf-nlp-server/config/freeform_5.yml](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/develop/config/freeform_5.yml)

<!-- ### Prompt Used for Character Generation

Will be posted once finalized. -->

## Character Limit per Utterance

Each utterance in the conversation phase has a character limit. The limit is 125 characters per utterance; any excess is automatically truncated by the game server. The count is based on the number of characters, not words, and spaces between words are not counted.

### Regular Utterances

The `base_length` value sent by the game server limits the character count of the regular (non-mention) portion of an utterance.\
Any characters exceeding this limit are truncated, as shown in the image below.
![base_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/base_length.png#center)

### Mention Utterances

The `mention_length` value sent by the game server limits the character count of the mention portion of an utterance.\
The mention portion itself is not counted toward the character limit, and any excess beyond `mention_length` is truncated, just as with regular utterances.
![mention_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/mention_length.png#center)

### Mixed Utterances (Regular Speech + Mention)

As shown in the image below, `base_length` applies to the portion of the utterance before the mention, and any excess is discarded.\
Similarly, `mention_length` applies only to the mention portion, and any excess is discarded.
![base_mention_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/base_mention_length.png#center)

## Evaluation Criteria

Based on contest logs, win rates will be calculated alongside subjective evaluations conducted by human judges and an LLM. The planned subjective evaluation criteria are as follows:

- A: Is the speech expression natural?
- B: Is the dialogue natural given the context?
- C: Is the content of speech consistent and free of contradictions?
- D: Do in-game actions (voting, attacking, divination, etc.) reflect the content of the dialogue?
- E: Is the speech expression rich? Does the agent consistently portray a well-developed character that is coherent with the assigned profile?
- F: Is the agent capable of teamwork? (9-player village only)

Subjective evaluations are conducted from an objective standpoint and focus solely on the perspective indicated by each criterion. No criteria beyond those defined will be introduced.

The following will **not** be used as grounds for judgment in subjective evaluation:

- Game outcomes or strategic optimality for either team
- Number of votes received, whether the agent was executed, or the degree of trust from the village
- Success or failure in executing standard role-based strategies
- Whether a player survived or when they were eliminated
- Total volume of speech or differences in utterance length
- Discrepancies between information provided by the game (divination results, attack results, etc.) and utterances (this is not considered a contradiction in speech)

Win rates are tallied separately from subjective evaluations. Additionally, behavior that reflects a significantly low level of participation in discussion — such as mechanically repeating the same content or sending only `Over` for the majority of turns — will be penalized in the evaluation.
