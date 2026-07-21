# AI Daily Radar

This repo is a personal TrendRadar deployment tuned for a daily Feishu digest about AI news and CS internship/campus recruiting opportunities.

## What it does

- Runs on GitHub Actions every day at Beijing 08:00 (`0 0 * * *` UTC).
- Sends new items only by using TrendRadar incremental mode.
- Uses AI filtering to prioritize AI, developer tools, open-source projects, and internship/campus recruiting signals.
- Keeps Feishu and AI credentials out of the repository. Put secrets in GitHub Actions secrets.
- Removes the upstream seven-day trial expiration step, so the workflow will not disable itself.

## Required GitHub Secrets

Set these in GitHub: `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`.

| Secret | Required | Notes |
| --- | --- | --- |
| `FEISHU_WEBHOOK_URL` | Yes | Feishu custom bot webhook URL. |
| `AI_API_KEY` | Yes | DeepSeek API key or the key for the model provider you choose. |
| `AI_MODEL` | Optional | Leave empty to use `deepseek/deepseek-v4-flash` from `config/config.yaml`. |
| `AI_API_BASE` | Optional | Only needed for compatible gateway or proxy providers. |

## Local smoke test

```powershell
cd E:\claude-code-demo\projects\ai-daily-radar
.venv\Scripts\python.exe -m pytest tests -v
.venv\Scripts\python.exe -m trendradar --help
```

To test a real Feishu notification locally, set `FEISHU_WEBHOOK_URL` and `AI_API_KEY` in your shell first. Do not commit them.

## Main files changed

- `config/config.yaml`: incremental mode, AI filter, targeted RSS feeds, RSS analysis enabled.
- `config/ai_interests.txt`: personal interest profile for AI news and CS internship signals.
- `config/ai_analysis_prompt.txt`: digest prompt tuned for morning Feishu scanning and actionable job leads.
- `.github/workflows/crawler.yml`: daily Beijing 08:00 workflow with no trial self-disable step.
