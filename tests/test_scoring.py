from src.scoring import extract_keywords, keyword_match, overall_score


def test_extract_keywords_ranks_repeated_terms_first():
    keywords = extract_keywords("Python developer. Python, SQL and Docker.")
    assert keywords[0] == "python"
    assert {"sql", "docker"}.issubset(keywords)


def test_keyword_match_returns_coverage():
    strengths, missing, score = keyword_match(
        "Python and SQL", "Python Python SQL Docker"
    )
    assert {"python", "sql"}.issubset(strengths)
    assert "docker" in missing
    assert score == 67


def test_overall_score_uses_weighted_components():
    assert overall_score(80, 100, 60) == 82

