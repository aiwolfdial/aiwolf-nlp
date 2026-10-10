#!/usr/bin/env bash
# contests（大会データ）の submodule を最新にして、サイト側にその参照をコミットする。push はしない。
#   bash scripts/contest/sync.sh            # origin の既定ブランチの最新へ
set -euo pipefail
cd "$(dirname "$0")/../.."
git -C external/aiwolf-nlp-contest-data fetch -q origin
git -C external/aiwolf-nlp-contest-data checkout -q --detach origin/HEAD 2>/dev/null || git -C external/aiwolf-nlp-contest-data checkout -q --detach origin/main 2>/dev/null || git -C external/aiwolf-nlp-contest-data checkout -q --detach origin/master
if git diff --quiet -- external/aiwolf-nlp-contest-data; then echo "contests: 変更なし（$(git -C external/aiwolf-nlp-contest-data log --oneline -1)）"; exit 0; fi
git add external/aiwolf-nlp-contest-data
git commit -q -m "data: 大会データを更新（$(git -C external/aiwolf-nlp-contest-data log -1 --format=%h)）"
echo "コミットしました: $(git log --oneline -1)"; echo "push すると公開サイトに反映されます: git push origin main"
