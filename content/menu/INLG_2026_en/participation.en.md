---
date: '2026-05-15T13:29:24+09:00'
draft: false
title: 'How to Participate'
category: schedule
---

## Connection Check and Main Competition

- The competition will be conducted in English.
- The competition consists of three divisions based on the combination of speech mode (turn-based / speak-anytime) and village size (5-player / 9-player). Please choose the division(s) you wish to enter (multiple divisions allowed). For the detailed rules of each division, see the [Competition Regulations](/menu/INLG_2026_en/regulation).
  - Turn-Based × 5-player village
  - Turn-Based × 9-player village
  - Speak-Anytime × 5-player village
- Role compositions are as follows:
  - 5-player village: Villager ×2, Werewolf ×1, Seer ×1, Possessed ×1
  - 9-player village: Villager ×3, Werewolf ×2, Seer ×1, Possessed ×1, Medium ×1, Bodyguard ×1

### Connection Check

- The connection check is intended to confirm that your agent connects and operates correctly.
- The connection check is conducted by submitting self-play logs (games played among agents of the same team). Please submit 3 self-play logs per division you are entering (see [How to Submit Self-Play Logs](#how-to-submit-self-play-logs) below for the submission procedure).
- Please submit by 2 days before the start of each round's (Round 1 / Round 2) Main Competition. This is the same as the registration deadline (see the [Home](/page/INLG_2026#important-dates-shared-task) page for dates).
- Logs generated during the connection check may be viewed and used by other teams.
- It is acceptable for your system or implementation to differ between the connection check and the Main Competition; however, please use the connection-check server to thoroughly verify your agent's behavior in order to avoid connection issues or unexpected behavior during the Main Competition.
- Teams that do not submit their connection-check self-play logs within the submission period will be treated as having withdrawn.

### Main Competition

- The Main Competition consists of cross-team matches (games between agents from different teams). The Main Competition is held for each of Round 1 and Round 2. In both, the number of matches per team per division follows the table below.

| Division | Matches per Team |
| --- | --- |
| Turn-Based × 5-player village | 75–100 matches |
| Turn-Based × 9-player village | 12–18 matches |
| Speak-Anytime × 5-player village | 8–12 matches |

Turn-based 5-player games run quickly, so more matches are scheduled for that division. For other divisions, the number of matches is set so that each team can play each role approximately 2–3 times.

In this competition, the Main Competition logs are evaluated according to the [Evaluation Criteria](/menu/INLG_2026_en/regulation#evaluation-criteria) to produce a ranking. The Main Competition logs of matches played among the top-ranked teams are then extracted and treated as the de facto final logs.

## How to Participate

- Teams must consist of at least one person. There are no eligibility requirements; anyone is welcome to participate.
- Please choose your entry type: "Round 1 + Round 2" or "Round 2 only." Deadlines for both Round 1 and Round 2 are accepted through the same form. Please check the [Home](/page/INLG_2026#important-dates-shared-task) page for each round's deadline.
- Each team should register via the [Google Form](https://forms.gle/53MJBSaLTe6xDw5o6). The form asks for the following information:
  - Representative's name
  - Representative's email address
  - Representative's affiliation (organization)
  - Other team members
  - Team name
  - Round(s) to participate in (Round 1 + Round 2 / Round 2 only)
  - Game(s) to participate in (Turn-Based 5-player / Turn-Based 9-player / Speak-Anytime 5-player)
  - Whether names and affiliations may be made public (if not, only the team name will be used)
  - Email address(es) for Slack registration (multiple allowed)
- We will invite the registered email addresses to our Slack workspace.
- There is no registration fee.
- After the competition, participants are asked to submit a document describing their system in detail.
- Participants are encouraged to attend INLG 2026 in person or online.
- Submitted documents and competition logs may be made publicly available and used for research purposes.
<!-- - Top-placing teams will receive a cash prize and gifts from Spiral.AI, a company developing proprietary large language models for spoken multi-turn conversation. -->
<!-- - Details on paper submission to be added -->

## How to Submit Self-Play Logs

- Connect your agent to the connection-check server provided by the organizers and run self-play games.
- Detailed instructions for connecting to the connection-check server will be provided to registered participants via Slack.
- Please submit 3 self-play logs per division you are entering (e.g., if entering all 3 divisions, 9 logs in total). Send the links to the generated game logs to the submission address announced on Slack.
- Please check the [Home](/page/INLG_2026#important-dates-shared-task) page for the submission deadline.
- For further technical details, see [How to Create and Battle with Agents](/menu/INLG_2026_en/agent).
