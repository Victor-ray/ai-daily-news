from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_config():
    return yaml.safe_load((ROOT / "config" / "config.yaml").read_text(encoding="utf-8"))


def enabled_rss_feeds(config):
    return [
        feed
        for feed in config["rss"]["feeds"]
        if feed.get("enabled", True)
    ]


def test_personal_digest_uses_incremental_ai_filtering():
    """增量模式 + AI 筛选 + 关键字展示"""
    config = load_config()

    assert config["app"]["timezone"] == "Asia/Shanghai"
    assert config["report"]["mode"] == "incremental"
    assert config["report"]["display_mode"] == "keyword"
    assert config["report"]["max_news_per_keyword"] == 5
    assert config["filter"]["method"] == "ai"
    assert config["ai_filter"]["min_score"] >= 0.7


def test_rss_sources_are_configured_for_three_sections():
    """RSS 源覆盖三大板块：AI资讯、GitHub项目、求职实习"""
    config = load_config()

    assert config["rss"]["enabled"] is True
    assert config["rss"]["freshness_filter"] == {
        "enabled": True,
        "max_age_days": 7,
    }

    feeds = enabled_rss_feeds(config)
    feed_ids = {feed["id"] for feed in feeds}

    # AI 资讯源
    assert "hacker-news-ai" in feed_ids
    assert "hacker-news-openai" in feed_ids
    assert "hacker-news-anthropic" in feed_ids
    assert "hacker-news-deepseek" in feed_ids
    # GitHub 项目源
    assert "github-trending-python" in feed_ids
    assert "github-trending-all" in feed_ids
    assert "hn-show" in feed_ids
    # 求职实习源
    assert "campus2026" in feed_ids
    assert "weloveinterns" in feed_ids
    assert "campus-recruitment-questions" in feed_ids

    assert all(feed["url"].startswith("https://") for feed in feeds)


def test_secrets_are_not_committed():
    """Webhook 和 API Key 不写入配置文件"""
    config = load_config()

    assert config["notification"]["channels"]["feishu"]["webhook_url"] == ""
    assert config["ai"]["api_key"] == ""


def test_ai_analysis_is_chinese_bounded_and_includes_rss():
    """AI 分析配置适配三大板块"""
    config = load_config()

    assert config["ai_analysis"]["enabled"] is True
    assert config["ai_analysis"]["language"] == "Chinese"
    assert config["ai_analysis"]["include_rss"] is True
    assert config["ai_analysis"]["max_news_for_analysis"] <= 30
