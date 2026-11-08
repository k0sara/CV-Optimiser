"""Curated, boundary-aware technical skill matching with traceable evidence.

This intentionally small vocabulary is transparent and easy to extend. It does
not infer proficiency, years of experience, or skills absent from the CV.
"""
import re

from src.models import SkillEvidence

SKILLS = {
    "Python": ("python",),
    "SQL": ("sql",),
    "JavaScript": ("javascript",),
    "TypeScript": ("typescript",),
    "Java": ("java",),
    "C++": ("c++",),
    "C#": ("c#", "c sharp"),
    ".NET": (".net", "dotnet"),
    "Go": ("golang", "go"),
    "Rust": ("rust",),
    "FastAPI": ("fastapi", "fast api"),
    "Flask": ("flask",),
    "Django": ("django",),
    "React": ("react", "react.js", "reactjs"),
    "Node.js": ("node.js", "nodejs"),
    "PostgreSQL": ("postgresql", "postgres"),
    "MySQL": ("mysql",),
    "MongoDB": ("mongodb",),
    "Redis": ("redis",),
    "AWS": ("aws", "amazon web services"),
    "Azure": ("azure",),
    "Google Cloud": ("gcp", "google cloud"),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Terraform": ("terraform",),
    "GitHub Actions": ("github actions",),
    "CI/CD": ("ci/cd", "ci cd", "continuous integration", "continuous delivery"),
    "Pytest": ("pytest",),
    "Git": ("git",),
    "Linux": ("linux",),
    "REST APIs": ("rest api", "rest apis", "restful"),
    "GraphQL": ("graphql",),
    "Microservices": ("microservices", "microservice"),
    "Celery": ("celery",),
    "RabbitMQ": ("rabbitmq",),
    "Kafka": ("kafka",),
    "Prometheus": ("prometheus",),
    "Grafana": ("grafana",),
    "OpenTelemetry": ("opentelemetry",),
    "OAuth": ("oauth", "oauth2", "oauth 2.0"),
    "Pandas": ("pandas",),
    "NumPy": ("numpy",),
    "scikit-learn": ("scikit-learn", "sklearn"),
    "PyTorch": ("pytorch",),
    "TensorFlow": ("tensorflow",),
    "Machine learning": ("machine learning",),
    "Power BI": ("power bi", "powerbi"),
    "Tableau": ("tableau",),
    "Excel": ("excel",),
    "Agile": ("agile", "scrum"),
}


def contains_skill(text, aliases):
    return any(
        re.search(r"(?<![\w])" + re.escape(alias) + r"(?![\w])", text, re.I)
        for alias in aliases
    )


def match_skills(cv_text: str, job_text: str) -> list[SkillEvidence]:
    required, preferred = [], []
    is_preferred = False
    for line in job_text.splitlines():
        heading = line.strip().strip(":").lower()
        if heading in {"nice to have", "nice-to-have", "preferred", "preferred qualifications", "bonus"}:
            is_preferred = True
        elif heading in {"requirements", "required", "responsibilities", "essential", "required qualifications"}:
            is_preferred = False
        (preferred if is_preferred else required).append(line)
    required_text = "\n".join(required)
    results = []
    for skill, aliases in SKILLS.items():
        if not contains_skill(job_text, aliases):
            continue
        priority = "required" if contains_skill(required_text, aliases) else "preferred"
        evidence = next((line.strip() for line in cv_text.splitlines() if contains_skill(line, aliases)), "")
        results.append(SkillEvidence(skill=skill, matched=bool(evidence), priority=priority, evidence=evidence[:500]))
    return results


def coverage(matches: list[SkillEvidence]) -> int:
    total = sum(1 if item.priority == "preferred" else 2 for item in matches)
    earned = sum((1 if item.priority == "preferred" else 2) for item in matches if item.matched)
    return round(100 * earned / total) if total else 0
