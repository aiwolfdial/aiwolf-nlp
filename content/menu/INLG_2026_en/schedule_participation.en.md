---
date: '2026-05-15T13:29:24+09:00'
draft: false
title: 'Schedule and How to Participate'
category: schedule
---

## Schedule

※ For paper-related dates (submission deadline, acceptance notification, camera-ready, and presentation), please refer to [paper_submission](/menu/INLG_2026/paper_submission).

<!-- Registration, preliminary, and main round dates are being finalized and will be updated once decided.
- 2026/07/20: Registration deadline
- 2026/08/01: Preliminary round (self-play) log submission deadline
- 2026/08 (early): Main round (online)
-->
- Registration, preliminary, and main round dates are being finalized and will be updated once decided.
- 2026/10/17–10/21: Workshop (presentation of peer-reviewed papers and results, etc.)

## Preliminary Round and Main Round

- The competition will be conducted in English.
- The competition consists of three divisions based on the combination of speech mode (turn-based / free-talk) and village size (5-player / 9-player). Please choose the division(s) you wish to enter (multiple divisions allowed). For the detailed rules of each division, see the [Competition Regulations](/menu/INLG_2026/regulation).
  - Turn-based × 5-player village
  - Turn-based × 9-player village
  - Free-talk × 5-player village
- Role compositions are as follows:
  - 5-player village: Villager ×2, Werewolf ×1, Seer ×1, Possessed ×1
  - 9-player village: Villager ×3, Werewolf ×2, Seer ×1, Possessed ×1, Medium ×1, Bodyguard ×1

### Preliminary Round

- The preliminary round is conducted by submitting self-play logs (games played among agents of the same team). Please submit 5 self-play logs per division you are entering (see [Self-Play (Preliminary) Submission](#self-play-preliminary-submission) below for the submission procedure).
- The preliminary round is primarily intended to verify that your agent works correctly, not to select teams for the main round.
- Logs generated during the preliminary round may be viewed and used by other teams.
- It is acceptable for your system or implementation to differ between the preliminary and main rounds; however, please use the preliminary server to thoroughly verify your agent's behavior in order to avoid connection issues or unexpected behavior during the main round.
- Teams that do not submit self-play logs within the submission period will be treated as having withdrawn.
<!-- - Depending on the number of participating teams, main-round participants may be selected based on preliminary round results. -->

### Main Round

- The main round consists of cross-team matches (games between agents from different teams). The number of matches per team per division is as follows (subject to change depending on competition progress):

| Division | Matches per Team |
| --- | --- |
| Turn-based × 5-player village | 75–100 matches |
| Turn-based × 9-player village | 12–18 matches |
| Free-talk × 5-player village | 8–12 matches |

Turn-based 5-player games run quickly, so more matches are scheduled for that division. For other divisions, the number of matches is set so that each team can play each role approximately 2–3 times.

## How to Participate

- Teams must consist of at least one person. There are no eligibility requirements; anyone is welcome to participate.
- Each team should fill out the [Google Form](https://forms.gle/53MJBSaLTe6xDw5o6). Required information includes: team name, representative contact email address, name(s) of the representative (and other members), affiliation, whether names and affiliation may be made public (if not, only the team name will be used), and the email address for Slack registration.
- We will invite the registered email addresses to our Slack workspace.
- There is no registration fee.
- After the competition, participants are asked to submit a document describing their system in detail.
- Participants are encouraged to attend INLG 2026 in person or online.
<!-- - Top-placing teams will receive a cash prize and gifts from Spiral.AI, a company developing proprietary large language models for spoken multi-turn conversation. -->
<!-- - Details on paper submission to be added -->
- Submitted documents and competition logs may be made publicly available and used for research purposes.

## Self-Play (Preliminary) Submission

- Connect your agent to the preliminary server provided by the organizers and run self-play games.
- Detailed instructions for connecting to the preliminary server will be provided to registered participants via Slack.
- Please submit 5 self-play logs per division you are entering (e.g., if entering all 3 divisions, 15 logs in total). Send the links to the generated game logs to the submission address announced on Slack.
- Please check the [Schedule](#schedule) for the submission deadline.
- For further technical details, see [Creating an Agent and How to Play](/menu/INLG_2026/agent).
