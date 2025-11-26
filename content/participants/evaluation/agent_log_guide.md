---
date: '2025-10-30T14:00:00+09:00'
draft: false
title: 'エージェントログの見方'
category: participants_guide
---

このページでは、エージェントログの確認方法や見方を解説します。
エージェントログは/aiwolfdial/aiwolf-nlp-agent-llm/log/time-stamp/に保存されるログファイルで、起動したエージェントごとにファイルがagent_name.logとして保存されます（1ゲームあたり、5人村なら5ファイル、13人村なら13ファイル）。

## 生成物の確認方法

各行は以下の形式で記録されます。

```text
タイムスタンプ - エージェント名 - ログレベル - メッセージ
```

### DEBUG行

ゲームサーバーから受信した**リクエストパケット**の完全な内容を記録します。

#### カラム

- タイムスタンプ：`2025-10-12 23:31:00,742`
- エージェント名： `kanolab1`
- ログレベル：`DEBUG`
- メッセージ：`Packet(...)` オブジェクト全体

#### 含まれる主な情報

- `request`：リクエストタイプ(`INITIALIZE`, `DAILY_INITIALIZE`, `TALK`, `DAILY_FINISH`など)
- `info`：ゲーム情報(game_id, day, agent名, role, status_map, divine_result, executed_agentなど)
- `setting`：ゲーム設定(役職構成、最大発言数、タイムアウト設定など)
- `talk_history`：発言履歴
- `whisper_history`：囁き履歴

### INFO行

エージェントの**動作と応答**を記録します。

#### 2種類のINFO行

1. **LLMへの入出力** (`['LLM', プロンプト, LLMの応答]`)
    - LLMに送信したプロンプト
    - LLMから受け取った応答
2. **リクエストへの最終応答** (`['Request.XXX', 応答内容]`)
    - ゲームサーバーに返す実際の応答(発言内容、投票対象など)

実装は src/utils/agent_logger.py で確認できます。
自分の好みに応じてagent_logの出力形式は変更してください。

### エージェントログの抜粋（デフォルト設定における見本）

```jsx
2025-10-12 23:31:00,742 - kanolab2 - DEBUG - Packet(request=<Request.INITIALIZE: 'INITIALIZE'>, info=Info(game_id='01K7CD9YW35TJ0V6473CZJYYR1', day=0, agent='ケンジ', profile='年齢: 12\n性別: 男性\n性格: ケンジは好奇心旺盛で、物事に対して積極的に挑戦する性格です。友達を大切にし、周囲の人々とコミュニケーションを取ることを好みます。少しおっちょこちょいなところもありますが、常に前向きで、困っている人を見捨てることはありません。おおらかで、周りの人々からは親しみやすいと感じられる存在です。', medium_result=None, divine_result=None, executed_agent=None, attacked_agent=None, vote_list=None, attack_vote_list=None, status_map={'ケンジ': <Status.ALIVE: 'ALIVE'>, 'シズエ': <Status.ALIVE: 'ALIVE'>, 'メイ': <Status.ALIVE: 'ALIVE'>, 'リュウジ': <Status.ALIVE: 'ALIVE'>, 'ヴィクトリア': <Status.ALIVE: 'ALIVE'>}, role_map={'ケンジ': <Role.VILLAGER: 'VILLAGER'>}, remain_count=None, remain_length=None, remain_skip=None), setting=Setting(agent_count=5, max_day=None, role_num_map={<Role.BODYGUARD: 'BODYGUARD'>: 0, <Role.MEDIUM: 'MEDIUM'>: 0, <Role.POSSESSED: 'POSSESSED'>: 1, <Role.SEER: 'SEER'>: 1, <Role.VILLAGER: 'VILLAGER'>: 2, <Role.WEREWOLF: 'WEREWOLF'>: 1}, vote_visibility=False, talk=Talk(max_count=TalkMaxCount(per_agent=4, per_day=20), max_length=TalkMaxLength(count_in_word=False, count_spaces=False, per_talk=None, mention_length=50, per_agent=None, base_length=50), max_skip=0), whisper=Whisper(max_count=WhisperMaxCount(per_agent=0, per_day=0), max_length=WhisperMaxLength(count_in_word=False, count_spaces=False, per_talk=None, mention_length=50, per_agent=None, base_length=50), max_skip=0), vote=Vote(max_count=1, allow_self_vote=True), attack_vote=AttackVote(max_count=1, allow_self_vote=True, allow_no_target=False), timeout=Timeout(action=60000, response=120000)), talk_history=None, whisper_history=None)
2025-10-12 23:31:04,793 - kanolab2 - INFO - ['LLM', 'あなたは人狼ゲームのエージェントです。\nあなたの名前はケンジです。\nあなたの役職はVILLAGERです。\n\nこれからゲームを進行していきます。リクエストが来た際には、日本語で適切な応答を返してください。\n\nトークリクエストと囁きリクエストに対しては、ゲーム内で発言するべき内容のみを出力してください。\n履歴がある場合は、それを参考にしてください。ない場合は、適切な内容を出力してください。\nこれ以上の情報を得られないと考えたときなどトークを終了したい場合については「Over」と出力してください。\n\n他のリクエストに対しては、行動の対象となるエージェントの名前のみを出力してください。\n対象となる生存しているエージェントの一覧が付与されています。\n\nあなたのプロフィール: 年齢: 12\n性別: 男性\n性格: ケンジは好奇心旺盛で、物事に対して積極的に挑戦する性格です。友達を大切にし、周囲の人々とコミュニケーションを取ることを好みます。少しおっちょこちょいなところもありますが、常に前向きで、困っている人を見捨てることはありません。おおらかで、周りの人々からは親しみやすいと感じられる存在です。\n\nあなたのレスポンスはそのままゲーム内に送信されるため、不要な情報を含めないでください。', '了解しました。ケンジです。よろしくね！']
2025-10-12 23:31:04,793 - kanolab2 - DEBUG - Packet(request=<Request.DAILY_INITIALIZE: 'DAILY_INITIALIZE'>, info=Info(game_id='01K7CD9YW35TJ0V6473CZJYYR1', day=0, agent='ケンジ', profile=None, medium_result=None, divine_result=None, executed_agent=None, attacked_agent=None, vote_list=None, attack_vote_list=None, status_map={'ケンジ': <Status.ALIVE: 'ALIVE'>, 'シズエ': <Status.ALIVE: 'ALIVE'>, 'メイ': <Status.ALIVE: 'ALIVE'>, 'リュウジ': <Status.ALIVE: 'ALIVE'>, 'ヴィクトリア': <Status.ALIVE: 'ALIVE'>}, role_map={'ケンジ': <Role.VILLAGER: 'VILLAGER'>}, remain_count=None, remain_length=None, remain_skip=None), setting=Setting(agent_count=5, max_day=None, role_num_map={<Role.BODYGUARD: 'BODYGUARD'>: 0, <Role.MEDIUM: 'MEDIUM'>: 0, <Role.POSSESSED: 'POSSESSED'>: 1, <Role.SEER: 'SEER'>: 1, <Role.VILLAGER: 'VILLAGER'>: 2, <Role.WEREWOLF: 'WEREWOLF'>: 1}, vote_visibility=False, talk=Talk(max_count=TalkMaxCount(per_agent=4, per_day=20), max_length=TalkMaxLength(count_in_word=False, count_spaces=False, per_talk=None, mention_length=50, per_agent=None, base_length=50), max_skip=0), whisper=Whisper(max_count=WhisperMaxCount(per_agent=0, per_day=0), max_length=WhisperMaxLength(count_in_word=False, count_spaces=False, per_talk=None, mention_length=50, per_agent=None, base_length=50), max_skip=0), vote=Vote(max_count=1, allow_self_vote=True), attack_vote=AttackVote(max_count=1, allow_self_vote=True, allow_no_target=False), timeout=Timeout(action=60000, response=120000)), talk_history=None, whisper_history=None)
2025-10-12 23:31:08,352 - kanolab2 - INFO - ['LLM', '昼開始リクエスト\n0日目', 'えーっと、みんなで話し合いましょう！']
2025-10-12 23:31:15,613 - kanolab2 - DEBUG - Packet(request=<Request.TALK: 'TALK'>, info=Info(game_id='01K7CD9YW35TJ0V6473CZJYYR1', day=0, agent='ケンジ', profile=None, medium_result=None, divine_result=None, executed_agent=None, attacked_agent=None, vote_list=None, attack_vote_list=None, status_map={'ケンジ': <Status.ALIVE: 'ALIVE'>, 'シズエ': <Status.ALIVE: 'ALIVE'>, 'メイ': <Status.ALIVE: 'ALIVE'>, 'リュウジ': <Status.ALIVE: 'ALIVE'>, 'ヴィクトリア': <Status.ALIVE: 'ALIVE'>}, role_map={'ケンジ': <Role.VILLAGER: 'VILLAGER'>}, remain_count=3, remain_length=None, remain_skip=0), setting=None, talk_history=[Talk(idx=0, day=0, turn=0, agent='ヴィクトリア', text='村人Aは、私のことを疑っているようだ。', skip=False, over=False), Talk(idx=1, day=0, turn=0, agent='リュウジ', text='ヴィクトリア、それはどういう意味ですか？具体的に誰のことですか？', skip=False, over=False)], whisper_history=None)
2025-10-12 23:31:19,284 - kanolab2 - INFO - ['LLM', 'トークリクエスト\n履歴:\nヴィクトリア: 村人Aは、私のことを疑っているようだ。\nリュウジ: ヴィクトリア、それはどういう意味ですか？具体的に誰のことですか？', 'ヴィクトリアさん、誰のことですか？']
2025-10-12 23:31:19,284 - kanolab2 - INFO - ['Request.TALK', 'ヴィクトリアさん、誰のことですか？']
2025-10-12 23:31:34,138 - kanolab2 - DEBUG - Packet(request=<Request.TALK: 'TALK'>, info=Info(game_id='01K7CD9YW35TJ0V6473CZJYYR1', day=0, agent='ケンジ', profile=None, medium_result=None, divine_result=None, executed_agent=None, attacked_agent=None, vote_list=None, attack_vote_list=None, status_map={'ケンジ': <Status.ALIVE: 'ALIVE'>, 'シズエ': <Status.ALIVE: 'ALIVE'>, 'メイ': <Status.ALIVE: 'ALIVE'>, 'リュウジ': <Status.ALIVE: 'ALIVE'>, 'ヴィクトリア': <Status.ALIVE: 'ALIVE'>}, role_map={'ケンジ': <Role.VILLAGER: 'VILLAGER'>}, remain_count=2, remain_length=None, remain_skip=0), setting=None, talk_history=[Talk(idx=2, day=0, turn=0, agent='ケンジ', text='ヴィクトリアさん、誰のことですか？', skip=False, over=False), Talk(idx=3, day=0, turn=0, agent='メイ', text='ヴィクトリアさん、具体的に誰のことを疑っているのか教えていただけますか？', skip=False, over=False), Talk(idx=4, day=0, turn=0, agent='シズエ', text='ヴィクトリアさん、具体的に誰のことか教えていただけますか？', skip=False, over=False), Talk(idx=5, day=0, turn=1, agent='ヴィクトリア', text='村人Aのことだよ。', skip=False, over=False), Talk(idx=6, day=0, turn=1, agent='リュウジ', text='村人Aですか。何か根拠は？', skip=False, over=False)], whisper_history=None)
2025-10-12 23:31:37,785 - kanolab2 - INFO - ['LLM', 'トークリクエスト\n履歴:\nケンジ: ヴィクトリアさん、誰のことですか？\nメイ: ヴィクトリアさん、具体的に誰のことを疑っているのか教えていただけますか？\nシズエ: ヴィクトリアさん、具体的に誰のことか教えていただけますか？\nヴィクトリア: 村人Aのことだよ。\nリュウジ: 村人Aですか。何か根拠は？', '村人Aさん、何かしたんですか？']
2025-10-12 23:31:37,786 - kanolab2 - INFO - ['Request.TALK', '村人Aさん、何かしたんですか？']
```

以上でエージェントログの見方について説明を完了します。

---

[参加者マニュアルトップへ](../_index.md)\
[確認・評価トップへ](./_index.md)\
[前へ（ゲームログの見方）](./game_log_guide.md)\
[次へ（ビュアーの使いかた）](./viewer_usage.md)
