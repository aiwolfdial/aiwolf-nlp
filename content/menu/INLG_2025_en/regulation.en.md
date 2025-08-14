---
date: '2025-07-07T13:29:24+09:00'
draft: false
title: 'Competition Regulations'
ShowToc: true
custom_style: 'documentPage'
---

## Notes

The following explains the regulations for the general public. If you are a participant implementing an agent, please see [How to create an agent and how to compete](/menu/INLG_2025/agent) for technical details.

- In the AIWolf Contest (Natural Language Division), matches are played over the internet with agents run on each participant’s own machine rather than by submitting executable files. Therefore, in both the preliminary and final rounds, you must run your program on your own device. The game server is operated by the organizers, but you are responsible for preparing the runtime environment required for your agent.
- Matches may include human players as well as automated agent players.
- Games are played with 5 or 13 players. For details, see [About roles used in hosted games](#Roles-Used-in-Hosted-Games).
- For game progression, see [Flow of the game](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/en/logic.md#Game-Flow).
- In the conversation phase (“talk”), interaction is conducted in natural language (English). The use of any protocol or other non-natural-language formats is prohibited. If you do not speak, return `Skip`; if you will not speak at all on that day, return `Over` (same as the Protocol Division).
- There is a per-utterance cap in the conversation phase. For details, see [Limit per utterance](#Limit-per-Utterance).
- For an agent’s character settings, use the character settings sent from the game server. (For details on character settings, see [About character settings](#About-Character-Settings).)
- When referring to a player by name in talk, use the character name sent by the game server. (Example: Daisuke is a Werewolf.)
- By adding an anchor like “@Daisuke” at the beginning of a talk utterance, you can direct your speech to a specific agent. An agent who is addressed is expected to respond in some way.
- For specifying targets such as voting, attacking, divining, or guarding, send only the character’s name. For details, see [How to specify targets for voting, attacks, divination, etc.](#How-to-Specify-Targets-for-Voting-Attacks-Divination-etc).
- For details on how voting and attack targets are determined, see [Phase flow](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/doc/en/logic.md#About-Phases).
- Utterances may be played aloud (e.g., via a robot). Please refrain from using emoticons, emojis, or symbols that cannot be rendered in speech (except standard punctuation such as ., !, ?).
- The response time limit is 1 minute. If the time limit is exceeded, actions such as talk will be ignored.
- Talk is also conducted on the first day (Day 0). This is intended for greetings, etc.
- A day consists of multiple turns. In the morning, the player attacked by werewolves during the previous night is announced and win/loss is checked. During the day, players discuss who the werewolves are. Then everyone votes for one player to execute; the player with the most votes is executed immediately. At night, roles with special actions take their turns.
- In each daytime turn, each agent is required to speak once, but the order is random. Therefore, you may be prompted to speak again immediately after speaking, or only after eight other utterances have occurred since your previous one.

## Roles Used in Hosted Games

The AIWolf Contest (Natural Language Division) runs 5-player and 13-player games. The roles and counts are as follows.

### For 5-player games

Roles in a 5-player game:

| Role    | Side      | Count | Special Ability                                                                 |
| ------- | --------- | ----- | ------------------------------------------------------------------------------- |
| Villager | Villagers | 2     | None                                                                            |
| Seer    | Villagers | 1     | At night, choose 1 player and learn that player’s side                          |
| Werewolf | Werewolves | 1   | At night, choose 1 player to attack and remove from the game                    |
| Madman  | Werewolves | 1    | Wins when the Werewolf side wins                                                |

### For 13-player games

Roles in a 13-player game:

| Role     | Side       | Count | Special Ability                                                                 |
| -------- | ---------- | ----- | -------------------------------------------------------------------------------- |
| Villager | Villagers  | 6     | None                                                                             |
| Seer     | Villagers  | 1     | At night, choose 1 player and learn that player’s side                           |
| Medium   | Villagers  | 1     | Learn the side of the player executed by vote                                    |
| Knight   | Villagers  | 1     | At night, choose 1 player to protect from a werewolf attack                      |
| Werewolf | Werewolves | 3     | At night, choose 1 player to attack and remove from the game                     |
| Madman   | Werewolves | 1     | Wins when the Werewolf side wins                                                 |

In 13-player games, due to the additional roles, you must also implement the Knight’s `guard` and the Werewolves’ `whisper`.\
For how to implement these in your agent, see [aiwolf-nlp-agent](https://github.com/aiwolfdial/aiwolf-nlp-agent/blob/main/README.en.md#how-to-customize-agents).


## About Character Settings

For each game, different character settings are automatically generated using a generative AI and sent from the game server to the agent.\
The four elements generated and sent are:

1. Name
1. Age
1. Gender
1. Personality

### Example

An example of character information provided by the game server:

```text
Minato:
Age: 10
Gender: Male
Personality: Minato has a laid-back temperament and prefers to interact gently with those around him. He can be a bit airheaded and sometimes wears an expression that makes it hard to tell what he’s thinking, but his innocence has a calming effect on others. He is very curious, loves learning new things, and is highly sensitive to others’ feelings. However, he is not good at asserting himself and sometimes has trouble expressing his own opinions.
```

For other concrete examples, see:
5-player game: [aiwolf-nlp-server/config/default_en_5.yml](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/config/default_en_5.yml#L16)
13-player game: [aiwolf-nlp-server/config/default_en_13.yml](https://github.com/aiwolfdial/aiwolf-nlp-server/blob/main/config/default_en_13.yml#L16)

### Prompt Used for Character Generation

To be posted once finalized.

## How to Specify Targets for Voting, Attacks, Divination, etc.

For actions that designate a single other player such as `VOTE`, `ATTACK`, `DIVINE`, and `GUARD`, use the character settings provided by the game server and send only that character’s name to the game server.

### Example: Designating Minato

Send only the name, as follows.

```text
Minato
```

## Limit per Utterance

Each utterance in the conversation phase has an upper limit. The cap for one utterance is 125 characters; any excess will be automatically truncated by the game server. Counting is by character, not by word, and spaces between words are not counted as characters.

### Normal utterances

The base_length sent from the game server limits the number of characters in the part of the utterance that has no mention.\
As shown in the image below, any excess is truncated.
![base_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/base_length.png#center)

### Utterances with a mention

The mention_length sent from the game server limits the number of characters in the portion of the utterance that includes a mention.\
The mention portion is not counted as characters, and any excess is truncated just like normal utterances.
![mention_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/mention_length.png#center)

### Utterances mixing normal text and mentions

As shown below, base_length applies to the utterance up to the mention, and any excess is discarded.\
Similarly, mention_length applies only to the portion that includes a mention, and any excess is discarded.
![base_mention_length](https://aiwolfdial.github.io/aiwolf-nlp/images/en/base_mention_length.png#center)
