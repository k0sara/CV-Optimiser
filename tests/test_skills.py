from src.skills import match_skills, coverage


def test_aliases_and_punctuation_match_without_substring_false_positives():
    result = match_skills("Postgres, K8s, C++, C#, .NET and JavaScript", "PostgreSQL Kubernetes C++ C# .NET Java")
    assert {item.skill for item in result if item.matched} == {"PostgreSQL", "Kubernetes", "C++", "C#", ".NET"}
    assert next(item for item in result if item.skill == "Java").matched is False


def test_required_skills_have_double_weight_and_evidence():
    matches = match_skills("Built Python services", "Requirements\nPython\nNice to have\nDocker")
    assert coverage(matches) == 67
    assert matches[0].evidence == "Built Python services"
    assert next(item for item in matches if item.skill == "Docker").priority == "preferred"


def test_generic_job_language_is_not_classified_as_a_skill():
    assert match_skills("Friendly and reliable", "We need a reliable colleague for our growing team") == []
