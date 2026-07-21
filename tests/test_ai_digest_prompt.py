from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "config" / "ai_analysis_prompt.txt"
INTERESTS = ROOT / "config" / "ai_interests.txt"


def test_analysis_prompt_has_three_sections():
    """Prompt 包含三大板块：热点速览、AI资讯、求职实习"""
    text = PROMPT.read_text(encoding="utf-8")

    assert "今日热点速览" in text
    assert "AI 资讯" in text
    assert "求职与实习" in text

    # 对应 JSON 字段
    assert "core_trends" in text
    assert "rss_insights" in text
    assert "outlook_strategy" in text


def test_analysis_prompt_keeps_json_contract():
    """保持 JSON 6 字段输出格式"""
    text = PROMPT.read_text(encoding="utf-8")

    assert "以 JSON 格式输出" in text
    assert '"core_trends"' in text
    assert '"rss_insights"' in text
    assert '"outlook_strategy"' in text
    assert '"signals"' in text
    assert '"sentiment_controversy"' in text
    assert '"standalone_summaries"' in text


def test_analysis_prioritizes_actionable_job_info():
    """Prompt 要求求职信息给出行动项"""
    text = PROMPT.read_text(encoding="utf-8")

    assert "行动项" in text
    assert "投递" in text
    assert "不编造" in text


def test_interests_cover_three_areas():
    """兴趣描述覆盖三大板块"""
    text = INTERESTS.read_text(encoding="utf-8")

    # 三大板块
    assert "今日热点速览" in text
    assert "AI 资讯" in text
    assert "求职与实习" in text

    # 关键方向覆盖
    assert "大模型" in text
    assert "GitHub" in text
    assert "后端" in text
    assert "校招" in text
