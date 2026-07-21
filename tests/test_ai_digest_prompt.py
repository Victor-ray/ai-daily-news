from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "config" / "ai_analysis_prompt.txt"
INTERESTS = ROOT / "config" / "ai_interests.txt"


def test_analysis_prompt_is_tailored_for_ai_and_internship_digest():
    text = PROMPT.read_text(encoding="utf-8")

    assert "AI 每日情报助手" in text
    assert "实习" in text
    assert "校招" in text
    assert "行动项" in text
    assert "投递线索" in text


def test_analysis_prompt_keeps_json_contract():
    text = PROMPT.read_text(encoding="utf-8")

    assert "以 JSON 格式输出分析结果" in text
    assert '"core_trends"' in text
    assert '"rss_insights"' in text
    assert '"outlook_strategy"' in text


def test_interests_prioritize_jobs_before_general_ai_news():
    text = INTERESTS.read_text(encoding="utf-8")

    jobs_index = text.index("AI 实习、校招与提前批机会")
    model_index = text.index("大模型与多模态进展")

    assert jobs_index < model_index
    assert "岗位、城市、批次、截止时间或投递入口" in text
