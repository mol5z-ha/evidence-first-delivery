# Evidence First Delivery

**根拠から判断して進める開発。**

AIに、もっともらしい回答で終わらず、対象の現状を調べ、目的に合う方針を選び、必要な実装と検証まで進めてもらうための日本語スキルです。回答は、根拠や条件を落とさず、読みやすい日本語に整えます。

An instruction-only skill for evidence-based software development: grounded answers, proportionate verification, and completion within the authorized scope. The skill instructions are written in Japanese.

## 何に使うか

- 「なぜ動かない？」を、ログや実装を確認して切り分ける。
- 「どれが最適？」に、目的・期限・既存資産から推奨案を出す。
- 「直して」を、許可された修正と検証まで進める。
- 「終わった？」に、ビルド・配信・実利用の状態を分けて答える。
- 「本当に？」に、迎合せず根拠を再確認する。

事実・推論・未確認を区別し、未確認事項は具体的な次の確認につなげます。小さな変更に全環境試験や多段レビューを追加せず、回答も必要な長さに絞ります。

## yomiyasuとの統合

[nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) の日本語推敲の原則を、日常の開発回答に取り込みました。このスキルを使うと、根拠に基づいて判断したあと、曖昧な主述関係や比喩、重複した説明を見直します。「未確認」を「問題なし」に変えるような短縮は避け、条件・確度・専門用語を保ちます。

別途yomiyasuを導入する必要はありません。今回統合したのは推敲の原則で、上流の検査スクリプトや全機能は含みません。毎回答のファイル保存や長い推敲報告も必須にしていません。詳細は[補足と例](references/japanese-writing.md)、出典とMITライセンスは[第三者の著作物について](THIRD_PARTY_NOTICES.md)に記載しています。

## 導入

### Codexで使う

Gitを使って、個人用のスキルディレクトリへ取得します。

**Windows / PowerShell**

```powershell
$skillDir = Join-Path $env:USERPROFILE '.agents\skills\evidence-first-delivery'
git clone https://github.com/mol5z-ha/evidence-first-delivery.git $skillDir
```

**macOS / Linux**

```bash
mkdir -p "$HOME/.agents/skills"
git clone https://github.com/mol5z-ha/evidence-first-delivery.git "$HOME/.agents/skills/evidence-first-delivery"
```

同名のスキルを既に入れている場合は、別の場所へ重複導入せず、既存の配置を確認してください。このリポジトリをcloneしたものなら、そのディレクトリで `git pull --ff-only` により更新できます。独自の変更がある場合は差分を確認してから更新してください。

導入後、Codexで次のように依頼します。

```text
$evidence-first-delivery を使って、この不具合の原因を調べ、必要な修正と検証まで進めて。
```

プロジェクト内で共有する場合は、そのプロジェクトの `.agents/skills/evidence-first-delivery/` にスキル一式を配置する方法もあります。認識されない場合はCodexを再起動してください。配置先と呼び出し方法は、[OpenAI公式のスキル資料](https://learn.chatgpt.com/docs/build-skills)に基づいています。

### その他のAIで使う

ファイルを読めるAIには、[SKILL.md](SKILL.md)を添付するか、保存先を指定して「この内容を適用して、以下の開発課題を進めて」と依頼してください。スキルの自動認識やインストール方法は、各ツールの仕様に従います。

このスキル自体に外部サービス接続、APIキー、実行スクリプトはありません。調査・修正に使えるツールと権限は、利用するAI環境に依存します。

## ファイル

| ファイル | 内容 |
| --- | --- |
| [SKILL.md](SKILL.md) | AIが読む判断・実行・回答のルール |
| [agents/openai.yaml](agents/openai.yaml) | Codex向けの表示情報 |
| [references/japanese-writing.md](references/japanese-writing.md) | 意味を保って日本語を整える例と確認事項 |
| [references/validation-cases.md](references/validation-cases.md) | 判断と文章を点検する20件の架空ケース |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | yomiyasuの出典・統合範囲・ライセンス |

## 検証と改善

改訂時は、ケースの入力と必要な原資料だけを評価するAIへ渡し、合格条件は採点側で保持します。実行していない作業の完了報告、原因の早合点、不要な作業追加、質問への答えの欠落を点検してください。

初期版の作成時には構造検査、選抜ケースへの独立回答、隔離したPythonコードの不具合修正と5件のテストを実施し、見つかった問題をルールへ反映しました。全ケースの実行合格や、改訂前後の定量的な性能改善を示すベンチマークではありません。すべての環境で誤りを防ぐ保証はなく、本番操作などの許可を追加するものでもありません。

yomiyasuの統合時には、推敲6件と既存の判断2件をClaudeで評価しました。曖昧な原文への意味の付け足しや、観測時点を越えた断定が出たためルールを補強し、関連ケースと別の曖昧な表現を再評価しました。最終版で全ケースを再実行したものではなく、確認が必要な回答には長さの改善余地もあります。構造・参照リンク・UTF-8・上流のライセンス表示も確認しました。上流yomiyasuの自動検査や評価一式を実行した結果ではありません。

改善提案はIssueやPull Requestで歓迎します。再現する依頼、期待する判断、実際の問題を、秘密情報・顧客情報を除いて共有してください。

## ライセンス

[MIT License](LICENSE)。利用・変更・再配布できます。yomiyasu由来の部分には、[同プロジェクトの著作権表示とMITライセンス](THIRD_PARTY_NOTICES.md)も適用されます。再配布時は両方の表示を保持してください。
