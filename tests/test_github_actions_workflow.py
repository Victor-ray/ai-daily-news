from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "crawler.yml"


def load_workflow():
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_workflow_name_is_daily_news_push():
    """工作流名称应为 每日资讯推送"""
    workflow = load_workflow()
    assert workflow.get("name") == "每日资讯推送"


def test_workflow_runs_daily_at_beijing_0800():
    """每天北京时间 08:00 自动运行"""
    workflow = load_workflow()
    on_config = workflow.get("on") or workflow[True]

    assert on_config["schedule"] == [{"cron": "0 0 * * *"}]
    assert "workflow_dispatch" in on_config


def test_workflow_does_not_self_disable():
    """不包含试用期/自动停用逻辑"""
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "Check Expiration" not in text
    assert "gh workflow disable" not in text
    assert "Trial" not in text
    assert "试用" not in text


def test_workflow_uses_required_secrets():
    """使用 FEISHU_WEBHOOK_URL 和 AI_API_KEY"""
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}" in text
    assert "AI_API_KEY: ${{ secrets.AI_API_KEY }}" in text
