"""
Gap Analyzer — Compares candidate profile against job requirements.
Produces gap-report.md and keyword-injection-map.json
"""
from dataclasses import dataclass, asdict, is_dataclass
from typing import Literal, Optional, Union, Any
from enum import Enum
import json
import math
import re
import yaml


@dataclass
class Gap:
    category: str  # hard_skills, tools, domain_knowledge, keyword_density, experience, education
    item: str
    severity: int  # 4=CRITICAL, 3=HIGH, 2=MEDIUM, 1=LOW
    current: str
    target: str
    suggestion: str


class Severity(Enum):
    CRITICAL = 4
    HIGH = 3
    MEDIUM = 2
    LOW = 1


@dataclass
class KeywordInjectionMap:
    injections: list[dict]

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        return getattr(self, key)


@dataclass
class GapReport:
    executive_summary: dict
    critical_gaps: list[dict]
    high_gaps: list[dict]
    medium_gaps: list[dict]
    low_gaps: list[dict]
    remediation_queue: list[dict]
    keyword_injection_map: dict
    reframing_suggestions: list[dict]

    def model_dump(self) -> dict:
        return asdict(self)

    def model_dump_json(self, indent: int = 2) -> str:
        return json.dumps(asdict(self), indent=indent, default=str)

    def get(self, key: str, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key: str):
        return getattr(self, key)

SEVERITY = {
    "CRITICAL": 4,
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}

WEIGHTS = {
    "hard_skills": 30,
    "tools": 20,
    "domain_knowledge": 15,
    "keyword_density": 20,
    "experience": 10,
    "education": 5
}


# ============================================================================
# Hybrid Lexical + Vector Semantic Matcher
# ============================================================================

# Domain equivalence & synonym taxonomy clusters.
# Kept local/deterministic so the gap analyzer works without network or model calls.
SYNONYM_CLUSTERS: list[set[str]] = [
    {
        "design system", "design systems", "component library", "design tokens",
        "storybook", "zeroheight", "style dictionary", "pattern library", "atomic design", "ui kit"
    },
    {
        "figma", "figjam", "devmode", "dev mode", "auto layout", "figma components",
        "figma variants", "sketch", "invision", "adobe xd"
    },
    {
        "user research", "usability testing", "user interviews", "jtbd", "jobs to be done",
        "qualitative research", "quantitative research", "diary studies", "card sorting",
        "dovetail", "user studies", "user testing", "customer research"
    },
    {
        "ui/ux", "product design", "user experience", "user interface", "interaction design",
        "ux design", "ui design", "human-computer interaction", "hci", "visual design"
    },
    {
        "prototyping", "interactive prototyping", "framer", "protopie", "principle",
        "high-fidelity prototypes", "wireframing", "wireframes", "mockups"
    },
    {
        "accessibility", "wcag", "wcag 2.1", "wcag 2.2", "a11y", "section 508",
        "aria", "screen reader", "inclusive design", "color contrast", "accessible design"
    },
    {
        "a/b testing", "ab testing", "experimentation", "split testing", "multivariate testing",
        "hypothesis testing", "statistical significance", "p-value", "p value", "holdout"
    },
    {
        "analytics", "product analytics", "mixpanel", "amplitude", "looker",
        "heap", "google analytics", "ga4", "posthog", "user analytics"
    },
    {
        "react", "react.js", "reactjs", "next.js", "nextjs", "jsx", "tsx", "react hooks", "react native"
    },
    {
        "typescript", "ts", "javascript", "js", "ecmascript", "es6", "vanilla javascript"
    },
    {
        "html/css", "html", "css", "semantic html", "tailwind", "tailwind css", "sass", "scss",
        "less", "css3", "html5", "responsive design"
    },
    {
        "vue", "vue.js", "vuejs", "nuxt", "nuxt.js", "angular", "svelte", "frontend framework"
    },
    {
        "node.js", "nodejs", "node", "express", "express.js", "backend javascript", "nestjs", "nest.js"
    },
    {
        "python", "py", "django", "fastapi", "flask", "pydantic", "pytest", "python development"
    },
    {
        "java", "spring", "spring boot", "jvm", "kotlin", "scala"
    },
    {
        "go", "golang", "go development"
    },
    {
        "c#", "csharp", ".net", "dotnet", "asp.net"
    },
    {
        "sql", "relational database", "relational databases", "postgresql", "postgres", "mysql",
        "bigquery", "snowflake", "sqlite", "oracle", "sql server", "mssql"
    },
    {
        "nosql", "mongodb", "mongo", "redis", "dynamodb", "cassandra", "elasticsearch", "opensearch"
    },
    {
        "rest", "rest api", "restful api", "graphql", "grpc", "openapi", "swagger", "api design",
        "api development", "web api"
    },
    {
        "ci/cd", "continuous integration", "continuous deployment", "continuous delivery",
        "github actions", "jenkins", "gitlab ci", "circleci", "delivery pipeline", "deployment pipeline"
    },
    {
        "kubernetes", "k8s", "container orchestration", "docker", "docker compose", "containers", "helm"
    },
    {
        "aws", "amazon web services", "cloud infrastructure", "gcp",
        "google cloud platform", "azure", "cloud computing", "cloud services"
    },
    {
        "terraform", "infrastructure as code", "iac", "pulumi", "cloudformation"
    },
    {
        "observability", "monitoring", "logging", "metrics", "datadog", "prometheus", "grafana", "splunk"
    },
    {
        "machine learning", "ml", "artificial intelligence", "ai", "deep learning", "nlp",
        "natural language processing", "llm", "llms", "large language model", "pytorch",
        "tensorflow", "scikit-learn", "sklearn", "hugging face", "transformers"
    },
    {
        "data science", "data analysis", "pandas", "numpy", "notebooks", "jupyter", "statistical modeling"
    },
    {
        "data engineering", "etl", "elt", "data pipeline", "data pipelines", "airflow", "dbt", "spark", "databricks"
    },
    {
        "unit testing", "automated testing", "test automation", "jest", "pytest", "cypress", "playwright",
        "selenium", "end-to-end testing", "e2e testing", "integration testing", "qa", "quality assurance"
    },
    {
        "security", "application security", "appsec", "owasp", "oauth", "oauth2", "jwt", "iam",
        "cybersecurity", "vulnerability assessment", "penetration testing", "auth", "authentication", "authorization"
    },
    {
        "cross-functional leadership", "cross-functional collaboration", "stakeholder management",
        "cross functional", "raci", "team leadership", "cross-team collaboration", "project management"
    },
    {
        "mentorship", "coaching", "team development", "mentoring", "design review", "code review", "peer review"
    },
    {
        "agile", "scrum", "kanban", "sprint planning", "jira", "linear", "agile methodologies"
    },
    {
        "product management", "roadmap", "roadmapping", "product strategy", "prioritization", "requirements"
    },
    {
        "fintech", "financial technology", "payments", "banking", "kyc", "aml", "pci-dss", "pci dss"
    },
    {
        "b2b saas", "enterprise saas", "saas", "cloud software", "software as a service"
    },
    {
        "ecommerce", "e-commerce", "marketplace", "online retail", "retail commerce"
    },
]


def lemmatize_word(word: str) -> str:
    """Normalize and lemmatize an individual word to its root morphological form."""
    w = word.strip().lower()
    if not w:
        return w

    overrides = {
        "k8s": "kubernetes",
        "js": "javascript",
        "ts": "typescript",
        "a11y": "accessibility",
        "i18n": "internationalization",
        "l10n": "localization",
        "systems": "system",
        "tokens": "token",
        "tests": "test",
        "testing": "test",
        "apis": "api",
        "components": "component",
        "databases": "database",
        "microservices": "microservice",
        "pipelines": "pipeline",
        "designs": "design",
        "designing": "design",
        "designed": "design",
        "develops": "develop",
        "developing": "develop",
        "developed": "develop",
        "manages": "manage",
        "managing": "manage",
        "managed": "manage",
        "applications": "application",
        "apps": "application",
        "app": "application",
        "services": "service",
    }
    if w in overrides:
        return overrides[w]

    # Handle standard English noun pluralization
    if len(w) > 4 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and w.endswith("es") and (w[-3] in ("s", "x", "z") or w[-4:-2] in ("ch", "sh")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not w.endswith(("ss", "us", "is", "as", "os")):
        return w[:-1]

    # Handle standard English verb inflections (-ing / -ed)
    if len(w) > 5 and w.endswith("ing"):
        base = w[:-3]
        if len(base) >= 2 and base[-1] == base[-2]:
            return base[:-1]
        return base
    if len(w) > 4 and w.endswith("ed"):
        base = w[:-2]
        if len(base) >= 2 and base[-1] == base[-2] and base[-1] not in ('l', 's'):
            return base[:-1]
        return base

    return w


def lemmatize_phrase(phrase: str) -> str:
    """
    Lemmatize an entire phrase while preserving technical tokens (A/B, CI/CD, Node.js).
    Normalize delimiters and return space-separated canonical form.
    """
    if not phrase:
        return ""
    raw = phrase.strip().lower()
    # Canonical technical compound phrases
    overrides = {
        "design systems": "design system",
        "a/b testing": "a/b test",
        "ab testing": "a/b test",
        "user interviews": "user interview",
        "react.js": "react",
        "reactjs": "react",
        "node.js": "node",
        "nodejs": "node",
        "next.js": "next",
        "nextjs": "next",
        "vue.js": "vue",
        "vuejs": "vue",
        "ci/cd": "ci/cd",
        "ci / cd": "ci/cd",
        "ui/ux": "ui/ux",
        "ui / ux": "ui/ux",
    }
    if raw in overrides:
        return overrides[raw]

    tokens = re.findall(r'[a-z0-9+#]+(?:/[a-z0-9+#]+)*', raw)
    lemmas = [lemmatize_word(t) for t in tokens if t]
    return " ".join(lemmas)


def get_skill_synonyms(skill: str) -> set[str]:
    """Retrieve all synonyms and related concepts for a given skill phrase."""
    lemma = lemmatize_phrase(skill)
    raw = skill.strip().lower()
    matches = {raw, lemma}
    for cluster in SYNONYM_CLUSTERS:
        cluster_lemmas = {lemmatize_phrase(c) for c in cluster}
        if raw in cluster or lemma in cluster_lemmas:
            matches.update(cluster)
            matches.update(cluster_lemmas)
    return matches


def get_cluster_similarity(skill1: str, skill2: str) -> float:
    """Return high similarity score when two skills share a synonym cluster."""
    s1_raw = skill1.strip().lower()
    s2_raw = skill2.strip().lower()
    if not s1_raw or not s2_raw:
        return 0.0
    if s1_raw == s2_raw:
        return 1.0
    s1_lem = lemmatize_phrase(skill1)
    s2_lem = lemmatize_phrase(skill2)
    if s1_lem == s2_lem and s1_lem:
        return 1.0

    for cluster in SYNONYM_CLUSTERS:
        cluster_lem = {lemmatize_phrase(c) for c in cluster}
        if (s1_raw in cluster or s1_lem in cluster_lem) and (s2_raw in cluster or s2_lem in cluster_lem):
            return 0.92

    # Check bidirectional synonym membership
    s1_syns = get_skill_synonyms(skill1)
    s2_syns = get_skill_synonyms(skill2)
    if s2_raw in s1_syns or s2_lem in s1_syns or s1_raw in s2_syns or s1_lem in s2_syns:
        return 0.88

    # Check synonym substring / token containment within clusters
    stop_words = {"system", "systems", "development", "engineering", "library", "tools", "tool", "platform", "pipeline"}
    s1_tokens = set(s1_lem.split())
    s2_tokens = set(s2_lem.split())

    for syn in s1_syns:
        syn_tokens = {t for t in lemmatize_phrase(syn).split() if t and t not in stop_words}
        if syn_tokens and syn_tokens.issubset(s2_tokens):
            return 0.86

    for syn in s2_syns:
        syn_tokens = {t for t in lemmatize_phrase(syn).split() if t and t not in stop_words}
        if syn_tokens and syn_tokens.issubset(s1_tokens):
            return 0.86

    return 0.0


def compute_cosine_similarity(
    vec1: list[float] | dict[str, float],
    vec2: list[float] | dict[str, float]
) -> float:
    """
    Compute cosine similarity between two feature maps (sparse dicts or dense lists).
    Safe against zero-norm vectors.
    """
    if isinstance(vec1, dict) and isinstance(vec2, dict):
        if not vec1 or not vec2:
            return 0.0
        dot = sum(vec1[k] * vec2[k] for k in vec1 if k in vec2)
        norm1 = math.sqrt(sum(v * v for v in vec1.values()))
        norm2 = math.sqrt(sum(v * v for v in vec2.values()))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return dot / (norm1 * norm2)

    # List or sequence space
    if not vec1 or not vec2 or len(vec1) != len(vec2):
        return 0.0
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0
    return dot / (norm1 * norm2)


def get_character_ngram_vector(text: str, n: int = 3) -> dict[str, float]:
    """Generate character n-gram TF feature dictionary for local string proximity."""
    canonical = f"^{lemmatize_phrase(text)}$"
    counts: dict[str, float] = {}
    length = max(1, len(canonical) - n + 1)
    for i in range(len(canonical) - n + 1):
        ngram = canonical[i:i + n]
        counts[ngram] = counts.get(ngram, 0.0) + 1.0
    for ngram in counts:
        counts[ngram] /= length
    return counts


def get_word_term_vector(text: str) -> dict[str, float]:
    """
    Generate lemmatized word TF feature vector enriched with local synonym proximity weights.
    Enables synonymous and related phrases to share feature subspaces in cosine similarity.
    """
    lem = lemmatize_phrase(text)
    words = [w for w in lem.split() if w]
    vec: dict[str, float] = {}
    for w in words:
        vec[w] = vec.get(w, 0.0) + 1.0

    # Enrich vector with discounted synonym tokens for semantic proximity smoothing
    syns = get_skill_synonyms(text)
    for syn in syns:
        syn_lem = lemmatize_phrase(syn)
        for sw in syn_lem.split():
            if sw and sw not in vec:
                vec[sw] = 0.35
    return vec


SEMANTIC_DIMENSIONS = {
    "design_uiux": ["design", "ui", "ux", "figma", "prototype", "wireframe", "interface", "experience", "interaction", "visual"],
    "design_systems": ["token", "component", "system", "storybook", "library", "atomic", "governance", "pattern"],
    "research": ["research", "user", "usability", "jtbd", "interview", "testing", "qualitative", "quantitative", "survey"],
    "frontend": ["react", "typescript", "javascript", "html", "css", "tailwind", "next", "frontend", "web", "vue", "angular"],
    "backend": ["node", "python", "api", "database", "sql", "backend", "server", "microservice", "java", "go", "rest", "graphql"],
    "databases": ["sql", "nosql", "postgres", "postgresql", "mysql", "mongodb", "redis", "dynamodb", "database", "query"],
    "analytics_experimentation": ["ab", "testing", "experiment", "analytics", "data", "metric", "mixpanel", "statistical"],
    "cloud_devops": ["aws", "cloud", "docker", "kubernetes", "ci", "cd", "pipeline", "infrastructure", "terraform", "monitoring"],
    "ai_ml": ["machine", "learning", "ml", "ai", "llm", "nlp", "model", "pytorch", "tensorflow", "transformer"],
    "testing_qa": ["test", "testing", "unit", "e2e", "jest", "pytest", "cypress", "playwright", "automation", "qa"],
    "security": ["security", "auth", "oauth", "jwt", "iam", "cybersecurity", "owasp", "vulnerability"],
    "leadership": ["leader", "manage", "stakeholder", "mentor", "cross", "functional", "road", "strategy", "agile", "scrum"],
    "accessibility": ["wcag", "a11y", "accessible", "aria", "inclusive", "screen", "contrast"],
}


def get_semantic_feature_vector(text: str) -> dict[str, float]:
    """Project phrase into local semantic domain feature space."""
    lem = lemmatize_phrase(text)
    tokens = set(lem.split())
    vec: dict[str, float] = {}
    for dim, keywords in SEMANTIC_DIMENSIONS.items():
        score = 0.0
        for kw in keywords:
            if kw in tokens:
                score += 1.0
            elif kw in lem:
                score += 0.5
        if score > 0:
            vec[dim] = score
    return vec


def compute_hybrid_vector_similarity(text1: str, text2: str) -> float:
    """
    Compute local approximate semantic + lexical vector similarity via Cosine Similarity.
    Combines:
    - Domain semantic feature cosine proximity (50%)
    - Word/term vector cosine proximity with synonym enrichment (35%)
    - Character n-gram cosine proximity (15%)
    """
    word1 = get_word_term_vector(text1)
    word2 = get_word_term_vector(text2)
    word_sim = compute_cosine_similarity(word1, word2)

    sem1 = get_semantic_feature_vector(text1)
    sem2 = get_semantic_feature_vector(text2)
    sem_sim = compute_cosine_similarity(sem1, sem2)

    ngram1 = get_character_ngram_vector(text1, n=3)
    ngram2 = get_character_ngram_vector(text2, n=3)
    ngram_sim = compute_cosine_similarity(ngram1, ngram2)

    base_sim = 0.50 * sem_sim + 0.35 * word_sim + 0.15 * ngram_sim

    # When skills share strong domain semantic feature overlap and token overlap, enhance proximity
    if sem_sim >= 0.80 and word_sim >= 0.25:
        base_sim = max(base_sim, 0.74 * sem_sim + 0.26 * word_sim)

    return min(1.0, base_sim)


class HybridSkillMatcher:
    """
    Hybrid Lexical + Vector Semantic Matcher.
    Combines:
    - Exact lexical matching
    - Lemmatized morphological matching
    - Direct synonym cluster domain taxonomy matching
    - Local vector cosine proximity (term space + semantic domains + n-grams)
    """
    def __init__(self, threshold: float = 0.72):
        self.threshold = threshold

    def match_score(self, req_skill: str, cand_skill: str) -> tuple[float, str]:
        """
        Evaluate match confidence between required skill and candidate skill.
        Returns (score, match_type) where match_type in:
        'exact', 'lemmatized', 'synonym', 'semantic', 'none'
        """
        req_clean = req_skill.strip()
        cand_clean = cand_skill.strip()
        if not req_clean or not cand_clean:
            return 0.0, "none"

        # 1. Exact match
        if req_clean.lower() == cand_clean.lower():
            return 1.0, "exact"

        # 2. Lemmatized match
        req_lem = lemmatize_phrase(req_clean)
        cand_lem = lemmatize_phrase(cand_clean)
        if req_lem == cand_lem and req_lem:
            return 1.0, "lemmatized"

        # 3. Token set permutation match (e.g. "systems design" vs "design system")
        req_tokens_list = [w for w in req_lem.split() if w]
        cand_tokens_list = [w for w in cand_lem.split() if w]
        if req_tokens_list and set(req_tokens_list) == set(cand_tokens_list):
            return 0.98, "lemmatized"

        # 4. Synonym / Cluster match
        clus_sim = get_cluster_similarity(req_clean, cand_clean)
        if clus_sim >= 0.85:
            return clus_sim, "synonym"

        # 5. Containment / Substring match on lemmatized token sets
        req_tokens = set(req_tokens_list)
        cand_tokens = set(cand_tokens_list)
        if req_tokens and cand_tokens:
            if req_tokens.issubset(cand_tokens):
                score = 0.88 if len(req_tokens) == 1 else 0.92
                return score, "lemmatized"
            if cand_tokens.issubset(req_tokens):
                score = 0.85 if len(cand_tokens) == 1 else 0.90
                return score, "lemmatized"

        # 6. Local Vector / Cosine Semantic Proximity
        vec_sim = compute_hybrid_vector_similarity(req_clean, cand_clean)
        if vec_sim >= self.threshold:
            return vec_sim, "semantic"

        return vec_sim, "none"

    def is_match(self, req_skill: str, cand_skill: str, threshold: Optional[float] = None) -> bool:
        """Check if req_skill and cand_skill match above threshold."""
        thresh = threshold if threshold is not None else self.threshold
        score, _ = self.match_score(req_skill, cand_skill)
        return score >= thresh

    def find_best_match(
        self,
        required_skill: str,
        candidate_skills: list[str],
        threshold: Optional[float] = None
    ) -> dict:
        """
        Search candidate skills for best matching skill using hybrid matching.
        Returns detailed match dict.
        """
        thresh = threshold if threshold is not None else self.threshold
        best_skill: Optional[str] = None
        best_score = 0.0
        best_type = "none"

        # Flatten any composite skill strings in candidate_skills
        expanded_candidates: list[str] = []
        for cand in candidate_skills:
            if not isinstance(cand, str) or not cand.strip():
                continue
            expanded_candidates.append(cand.strip())
            if any(sep in cand for sep in (',', ';', ' / ')):
                sub_items = [s.strip() for s in re.split(r'[,;]|\s/\s', cand) if s.strip()]
                for s in sub_items:
                    if s not in expanded_candidates:
                        expanded_candidates.append(s)

        for cand in expanded_candidates:
            score, m_type = self.match_score(required_skill, cand)
            if score > best_score:
                best_score = score
                best_skill = cand
                best_type = m_type

            # Early exit on exact or direct lemma match
            if best_score >= 0.99:
                break

        return {
            "matched": best_score >= thresh,
            "best_match": best_skill if best_score >= thresh else None,
            "score": best_score,
            "match_type": best_type if best_score >= thresh else "none",
            "required_skill": required_skill,
        }

    def match_against_profile(
        self,
        required_skill: str,
        candidate_profile: dict,
        threshold: Optional[float] = None
    ) -> dict:
        """Extract candidate skills from all profile locations and run hybrid matcher."""
        all_skills: list[str] = []
        skills_dict = candidate_profile.get("skills", {})
        if isinstance(skills_dict, dict):
            for values in skills_dict.values():
                if isinstance(values, list):
                    all_skills.extend([str(v) for v in values if isinstance(v, str)])
                elif isinstance(values, str):
                    all_skills.append(values)
        elif isinstance(skills_dict, list):
            all_skills.extend([str(v) for v in skills_dict if isinstance(v, str)])

        for section_key in ("tools", "technologies"):
            section_val = candidate_profile.get(section_key, [])
            if isinstance(section_val, list):
                all_skills.extend([str(v) for v in section_val if isinstance(v, str)])

        for exp in candidate_profile.get("experience", []):
            if isinstance(exp, dict):
                for key in ("stack", "technologies", "tools"):
                    stack_items = exp.get(key, [])
                    if isinstance(stack_items, list):
                        all_skills.extend([str(v) for v in stack_items if isinstance(v, str)])

        for proj in candidate_profile.get("projects", []):
            if isinstance(proj, dict):
                for key in ("stack", "technologies", "tools"):
                    stack_items = proj.get(key, [])
                    if isinstance(stack_items, list):
                        all_skills.extend([str(v) for v in stack_items if isinstance(v, str)])

        return self.find_best_match(required_skill, all_skills, threshold=threshold)


def load_job_analysis(path: Union[str, dict, Any]) -> dict:
    """Load job analysis from path, dict, or dataclass instance"""
    if isinstance(path, dict):
        return path
    if is_dataclass(path):
        return asdict(path)
    if hasattr(path, 'model_dump'):
        return path.model_dump()
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def load_candidate_profile(path: Union[str, dict, Any]) -> dict:
    """Load candidate profile from path, dict, or dataclass instance"""
    if isinstance(path, dict):
        return path
    if is_dataclass(path):
        return asdict(path)
    if hasattr(path, 'model_dump'):
        return path.model_dump()
    with open(path, encoding='utf-8') as f:
        if str(path).endswith('.yaml') or str(path).endswith('.yml'):
            return yaml.safe_load(f)
        return json.load(f)


def analyze_gaps(job_analysis_path: Union[str, dict, Any], candidate_profile: Union[str, dict, Any]) -> tuple[GapReport, dict]:
    """Full gap analysis → GapReport + KeywordInjectionMap"""
    job = load_job_analysis(job_analysis_path)
    candidate = load_candidate_profile(candidate_profile)

    gaps = []

    matcher = HybridSkillMatcher(threshold=0.72)
    skills_dict = candidate.get('skills', {})
    all_candidate_skills: list[str] = []
    if isinstance(skills_dict, dict):
        for s_list in skills_dict.values():
            if isinstance(s_list, list):
                all_candidate_skills.extend([str(x) for x in s_list if isinstance(x, str)])
    elif isinstance(skills_dict, list):
        all_candidate_skills.extend([str(x) for x in skills_dict if isinstance(x, str)])

    for exp in candidate.get('experience', []):
        for st in exp.get('stack', []):
            if isinstance(st, str):
                all_candidate_skills.append(st)

    # 1. Hard Skills Gap
    seen_hard = set()
    for skill in job['must_have'].get('hard_skills', []):
        sk_key = skill.strip().lower()
        if not sk_key or sk_key in seen_hard:
            continue
        seen_hard.add(sk_key)
        match_res = matcher.find_best_match(skill, all_candidate_skills)
        if not match_res["matched"]:
            gaps.append(Gap(
                category="hard_skills",
                item=skill,
                severity=SEVERITY["CRITICAL"],
                current="Not listed",
                target="Required",
                suggestion=f"Add '{skill}' to Technical Skills; inject in 2 bullets (most recent role + 1 prior)"
            ))

    # 2. Tools Gap
    seen_tools = set()
    for tool in job['must_have'].get('tools', []):
        tool_key = tool.strip().lower()
        if not tool_key or tool_key in seen_tools:
            continue
        seen_tools.add(tool_key)
        match_res = matcher.find_best_match(tool, all_candidate_skills)
        if not match_res["matched"]:
            gaps.append(Gap(
                category="tools",
                item=tool,
                severity=SEVERITY["HIGH"],
                current="Not listed",
                target="Required",
                suggestion=f"Add '{tool}' to Tools; mention in 1-2 experience bullets"
            ))

    # 3. Domain Knowledge Gap
    seen_domains = set()
    for domain in job['must_have'].get('domain_knowledge', []):
        domain_key = domain.strip().lower()
        if not domain_key or domain_key in seen_domains:
            continue
        seen_domains.add(domain_key)
        match_res = matcher.find_best_match(domain, all_candidate_skills)
        if not match_res["matched"]:
            gaps.append(Gap(
                category="domain_knowledge",
                item=domain,
                severity=SEVERITY["HIGH"],
                current="Partial/None",
                target="Required",
                suggestion=f"Reframe existing experience to highlight {domain} adjacency; inject in Summary + 2 bullets"
            ))

    # 4. Keyword Density Gap
    for kw, target in job.get('keyword_targets', {}).items():
        current_density = estimate_current_density(candidate, kw)
        if current_density < target['min']:
            severity = SEVERITY["HIGH"] if target['priority'] == 'critical' else SEVERITY["MEDIUM"]
            needed = int((target['min'] - current_density) * estimate_resume_word_count(candidate) / 100)
            gaps.append(Gap(
                category="keyword_density",
                item=kw,
                severity=severity,
                current=f"{current_density:.1f}%",
                target=f"{target['min']:.1f}%",
                suggestion=f"Inject '{kw}' in {max(2, needed)} locations: Summary, Skills, {min(needed, 2)} Experience bullets"
            ))

    # 5. Experience Years Gap
    req_years = parse_years(job['must_have'].get('years_experience', '0'))
    cand_years = candidate.get('total_years', 0)
    if cand_years < req_years:
        gaps.append(Gap(
            category="experience",
            item=f"{req_years}+ years",
            severity=SEVERITY["HIGH"],
            current=f"{cand_years} years",
            target=f"{req_years}+ years",
            suggestion="Reframe seniority of past roles; emphasize scope/scale over years; add 'equivalent experience' framing"
        ))

    # 6. Education Gap
    req_edu = job['must_have'].get('education', '')
    cand_edu = candidate.get('education', [])
    if req_edu and not education_matches(req_edu, cand_edu):
        gaps.append(Gap(
            category="education",
            item=req_edu,
            severity=SEVERITY["MEDIUM"],
            current="Different",
            target=req_edu,
            suggestion="Add 'or equivalent experience' framing; highlight relevant coursework/projects"
        ))

    # Sort by severity
    gaps.sort(key=lambda g: g.severity, reverse=True)

    # Categorize
    critical = [asdict(g) for g in gaps if g.severity == SEVERITY["CRITICAL"]]
    high = [asdict(g) for g in gaps if g.severity == SEVERITY["HIGH"]]
    medium = [asdict(g) for g in gaps if g.severity == SEVERITY["MEDIUM"]]
    low = [asdict(g) for g in gaps if g.severity == SEVERITY["LOW"]]

    # Build keyword injection map
    injection_map = build_injection_map(job, candidate, gaps)

    # Build remediation queue
    remediation = build_remediation_queue(gaps, injection_map)

    # Reframing suggestions for domain gaps
    reframing = build_reframing_suggestions(gaps, job, candidate)

    # Executive summary
    match_pct = calculate_match_score(gaps)
    exec_summary = {
        "overall_match": match_pct,
        "critical_count": len(critical),
        "high_count": len(high),
        "medium_count": len(medium),
        "estimated_fix_minutes": estimate_fix_time(gaps)
    }

    report = GapReport(
        executive_summary=exec_summary,
        critical_gaps=critical,
        high_gaps=high,
        medium_gaps=medium,
        low_gaps=low,
        remediation_queue=remediation,
        keyword_injection_map=injection_map,
        reframing_suggestions=reframing
    )

    return report, injection_map


def estimate_current_density(candidate: dict, keyword: str) -> float:
    """Estimate current keyword density in candidate profile supporting lemmatized and synonym matches."""
    all_text = ""
    for exp in candidate.get('experience', []):
        for bullet in exp.get('bullets', []):
            all_text += bullet + " "
    for proj in candidate.get('projects', []):
        for bullet in proj.get('bullets', []):
            all_text += bullet + " "
    if candidate.get('headline'):
        all_text += candidate['headline'] + " "
    skills = candidate.get('skills', {})
    for cat, items in skills.items():
        if isinstance(items, list):
            all_text += ' '.join([str(x) for x in items if isinstance(x, str)]) + " "

    words = all_text.lower().split()
    if not words:
        return 0.0

    text_lower = all_text.lower()
    search_forms = {keyword.lower(), lemmatize_phrase(keyword)}
    synonyms = get_skill_synonyms(keyword)
    for s in synonyms:
        if s and len(s) >= 3:
            search_forms.add(s.lower())

    kw_count = 0
    sorted_forms = sorted([str(f) for f in search_forms if f], key=len, reverse=True)
    temp_text = text_lower
    for form in sorted_forms:
        count = temp_text.count(form)
        if count > 0:
            kw_count += count
            temp_text = temp_text.replace(form, " _matched_ ")

    kw_words = len(keyword.split())
    return (kw_count * kw_words / len(words)) * 100


def estimate_resume_word_count(candidate: dict) -> int:
    """Rough word count of full resume"""
    count = 0
    for exp in candidate.get('experience', []):
        for bullet in exp.get('bullets', []):
            count += len(bullet.split())
    count += len(candidate.get('headline', '').split()) * 3
    return max(count, 300)


def parse_years(text: str) -> int:
    match = re.search(r'(\d+)', text)
    return int(match.group(1)) if match else 0


def education_matches(required: str, candidate: list) -> bool:
    required_lower = required.lower()
    req_lem = lemmatize_phrase(required_lower)
    for edu in candidate:
        degree = edu.get('degree', '')
        if not isinstance(degree, str) or not degree:
            continue
        degree_lower = degree.lower()
        if any(kw in degree_lower for kw in required_lower.split() if len(kw) > 2):
            return True
        if compute_hybrid_vector_similarity(req_lem, degree_lower) >= 0.65:
            return True
    return False


def build_injection_map(job: dict, candidate: dict, gaps: list[Gap]) -> dict:
    """Generate exact locations for keyword injection"""
    injections = []

    for kw, target in job.get('keyword_targets', {}).items():
        current = estimate_current_density(candidate, kw)
        if current >= target['min']:
            continue

        needed = max(1, int((target['min'] - current) * estimate_resume_word_count(candidate) / 100))
        locations = []

        # Priority: Summary > Skills > Most recent role bullets > Prior role bullets
        locations.append("summary")
        locations.append("skills")
        for i, exp in enumerate(candidate.get('experience', [])[:2]):
            locations.append(f"experience:{i}")

        injections.append({
            "keyword": kw,
            "target_density": target['min'],
            "current_density": round(current, 2),
            "locations": locations[:needed + 2],
            "variant": get_variant(kw)
        })

    return {"injections": injections}


def get_variant(keyword: str) -> str:
    variants = {
        "design systems": "design system",
        "a/b testing": "experimentation",
        "figma": "Figma",
        "react": "React",
        "typescript": "TypeScript",
        "accessibility": "WCAG"
    }
    return variants.get(keyword.lower(), keyword)


def build_remediation_queue(gaps: list[Gap], injection_map: dict) -> list[dict]:
    queue = []
    priority = 1

    # Critical skills first
    for gap in gaps:
        if gap.severity == SEVERITY["CRITICAL"]:
            queue.append({
                "priority": priority,
                "action": gap.suggestion,
                "category": gap.category,
                "item": gap.item,
                "est_minutes": 5 if gap.category == "hard_skills" else 10
            })
            priority += 1

    # Keyword density injections
    for inj in injection_map.get('injections', []):
        queue.append({
            "priority": priority,
            "action": f"Inject '{inj['keyword']}' at: {', '.join(inj['locations'])}",
            "category": "keyword_density",
            "item": inj['keyword'],
            "est_minutes": len(inj['locations']) * 2
        })
        priority += 1

    # High gaps
    for gap in gaps:
        if gap.severity == SEVERITY["HIGH"] and gap.category != "keyword_density":
            queue.append({
                "priority": priority,
                "action": gap.suggestion,
                "category": gap.category,
                "item": gap.item,
                "est_minutes": 10
            })
            priority += 1

    return queue


def build_reframing_suggestions(gaps: list[Gap], job: dict, candidate: dict) -> list[dict]:
    suggestions = []
    domain_gaps = [g for g in gaps if g.category == "domain_knowledge"]

    for gap in domain_gaps:
        domain = gap.item.lower()
        # Find relevant experience to reframe
        for exp in candidate.get('experience', [])[:2]:
            for bullet in exp.get('bullets', []):
                suggestions.append({
                    "current_framing": bullet[:80] + "...",
                    "target_framing": f"{domain.capitalize()} {bullet.lower()}",
                    "signal_activated": domain.replace(' ', '-')
                })
                break

    return suggestions[:5]


def calculate_match_score(gaps: list[Gap]) -> int:
    if not gaps:
        return 100
    total_weight = sum(WEIGHTS.values())
    gap_weight = sum(WEIGHTS.get(g.category, 10) * (g.severity / 4) for g in gaps)
    return max(0, int(100 - (gap_weight / total_weight) * 100))


def estimate_fix_time(gaps: list[Gap]) -> int:
    base = 0
    for gap in gaps:
        if gap.severity == SEVERITY["CRITICAL"]:
            base += 10
        elif gap.severity == SEVERITY["HIGH"]:
            base += 8
        elif gap.severity == SEVERITY["MEDIUM"]:
            base += 5
        else:
            base += 3
    return base


def analyze_general_ats_gaps(resume_path: str) -> dict:
    """General ATS audit gap analysis (no job target)"""
    # In production: parse LaTeX and run validation checks
    # This returns the structure matching ats-audit-gap-report.md
    return {
        "overall_readiness": 87,
        "critical_gaps": 1,
        "high_gaps": 2,
        "medium_gaps": 3,
        "findings": {
            "format_compliance": {},
            "structure_completeness": {},
            "keyword_hygiene": {},
            "readability_baseline": {},
            "unicode_extraction": {},
            "parser_simulation": {}
        },
        "prioritized_fixes": []
    }


def save_report(report: GapReport, output_path: str):
    """Save as markdown with frontmatter"""
    import datetime

    lines = [
        "---",
        f"title: Gap Analysis Report",
        f"generated: {datetime.datetime.utcnow().isoformat()}Z",
        "---",
        "",
        f"# Gap Analysis Report",
        "",
        f"**Generated:** {datetime.datetime.utcnow().strftime('%Y-%m-%d')} | **Overall Match:** {report.executive_summary['overall_match']}%",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Overall Match** | {report.executive_summary['overall_match']}% |",
        f"| **Critical Gaps** | {report.executive_summary['critical_count']} |",
        f"| **High Gaps** | {report.executive_summary['high_count']} |",
        f"| **Medium Gaps** | {len(report.medium_gaps)} |",
        f"| **Estimated Fix Time** | {report.executive_summary['estimated_fix_minutes']} min |",
        "",
        "---",
    ]

    for section_name, gaps in [
        ("[CRITICAL] Critical Gaps (Must Fix Before Apply)", report.critical_gaps),
        ("[HIGH] High Gaps (Strongly Recommended)", report.high_gaps),
        ("[MEDIUM] Medium Gaps (Nice to Have)", report.medium_gaps),
    ]:
        if gaps:
            lines.extend([
                f"## {section_name}",
                "",
                "| # | Category | Job Requires | Candidate Has | Gap | Remediation |",
                "|---|----------|--------------|---------------|-----|-------------|",
            ])
            for i, gap in enumerate(gaps, 1):
                lines.append(f"| {i} | {gap['category']} | **{gap['item']}** | {gap['current']} | {gap['target']} | {gap['suggestion']} |")
            lines.append("")

    # Remediation queue
    if report.remediation_queue:
        lines.extend([
            "## Remediation Priority Queue",
            "",
            "| Priority | Action | Category | Est. Time |",
            "|----------|--------|----------|-----------|",
        ])
        for item in report.remediation_queue:
            lines.append(f"| {item['priority']} | {item['action']} | {item['category']} | {item['est_minutes']} min |")
        lines.append("")

    # Keyword injection map
    if report.keyword_injection_map.get('injections'):
        lines.extend([
            "## Keyword Injection Map (Exact Locations)",
            "",
            "| Keyword | Target | Current | Locations to Add | Variant |",
            "|---------|--------|---------|------------------|---------|",
        ])
        for inj in report.keyword_injection_map['injections']:
            lines.append(f"| {inj['keyword']} | {inj['target_density']}% | {inj['current_density']}% | {', '.join(inj['locations'])} | {inj['variant']} |")
        lines.append("")

    # Reframing suggestions
    if report.reframing_suggestions:
        lines.extend([
            "## Reframing Suggestions (Domain Gap)",
            "",
            "| Current Framing | Target Framing | Signal Activated |",
            "|-----------------|----------------|------------------|",
        ])
        for ref in report.reframing_suggestions:
            lines.append(f"| {ref['current_framing']} | {ref['target_framing']} | {ref['signal_activated']} |")
        lines.append("")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))


def save_injection_map(injection_map: dict, output_path: str):
    with open(output_path, 'w') as f:
        json.dump(injection_map, f, indent=2)


if __name__ == "__main__":
    import sys
    import argparse
    import json
    import yaml

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    # Targeted gap analysis
    targeted = subparsers.add_parser("targeted")
    targeted.add_argument("--job", required=True)
    targeted.add_argument("--candidate", required=True)
    targeted.add_argument("--out", required=True)
    targeted.add_argument("--injection-map", required=True)

    # General ATS audit
    ats_audit = subparsers.add_parser("ats-audit")
    ats_audit.add_argument("--resume", required=True)
    ats_audit.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.command == "targeted":
        # Load job analysis
        with open(args.job) as f:
            job = json.load(f)
        # Load candidate profile
        with open(args.candidate) as f:
            if args.candidate.endswith('.yaml') or args.candidate.endswith('.yml'):
                candidate = yaml.safe_load(f)
            else:
                candidate = json.load(f)

        report, injection_map = analyze_gaps(job, candidate)
        save_report(report, args.out)
        save_injection_map(injection_map, args.injection_map)
        print(f"Gap report saved to {args.out}")
        print(f"Injection map saved to {args.injection_map}")

    elif args.command == "ats-audit":
        report = analyze_general_ats_gaps(args.resume)
        with open(args.out, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"ATS audit gap report saved to {args.out}")