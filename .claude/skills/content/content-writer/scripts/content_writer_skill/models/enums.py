"""
Enumeration types for content writer skill.
"""

from enum import Enum


class Goal(str, Enum):
    """Primary goal of a content piece."""
    EDUCATE = "educate"
    PERSUADE = "persuade"
    INFORM = "inform"
    ENTERTAIN = "entertain"
    CONVERT = "convert"
    NURTURE = "nurture"
    REASSURE = "reassure"
    WARN = "warn"


class Format(str, Enum):
    """Content format/type."""
    BLOG = "blog"
    LANDING_PAGE = "landing-page"
    EMAIL = "email"
    SOCIAL = "social"
    CASE_STUDY = "case-study"
    WHITEPAPER = "whitepaper"
    PRESS_RELEASE = "press-release"
    VIDEO_SCRIPT = "video-script"
    PODCAST_OUTLINE = "podcast-outline"
    TECHNICAL_DOC = "technical-doc"
    FAQ = "faq"
    COMPARISON_PAGE = "comparison-page"


class Tone(str, Enum):
    """Tone/voice descriptors (not exhaustive - free text allowed in brief)."""
    PROFESSIONAL_WARM = "professional, warm, conversational"
    CONFIDENT_PRACTICAL = "confident, practical, slightly conversational"
    AUTHORITATIVE = "authoritative, evidence-based"
    WARM_PERSONAL = "warm, personal, conversational"
    PUNCHY_INSIGHTFUL = "punchy, insightful, conversational"
    CREDIBLE_SPECIFIC = "credible, specific, customer-voice-forward"
    OBJECTIVE_NEWSWORTHY = "objective, newsworthy, quote-rich, factual"
    ENERGETIC_HOOK_DRIVEN = "energetic, clear, hook-driven"
    TECHNICAL_PRECISE = "precise, technical, peer-to-peer"
    CRISP_RESULTS_FIRST = "crisp, results-first, scannable"
    RELATABLE_STORY = "relatable, story-driven, empathetic"
    CALM_ACTION_FIRST = "calm, brief, action-first"


class HookType(str, Enum):
    """Hook types from content-frameworks.md."""
    QUESTION = "question"
    BOLD_CLAIM = "bold-claim"
    STORY = "story"
    STATISTIC = "statistic"
    CONTRARIAN = "contrarian"
    PAIN_POINT = "pain-point"
    CURIOSITY_GAP = "curiosity-gap"
    DIRECT_BENEFIT = "direct-benefit"


class StructurePattern(str, Enum):
    """Structural patterns from content-frameworks.md."""
    PROBLEM_SOLUTION = "problem-solution"
    BEFORE_AFTER_BRIDGE = "before-after-bridge"
    ATTENTION_INTEREST_DESIRE_ACTION = "attention-interest-desire-action"
    FEATURE_ADVANTAGE_BENEFIT = "feature-advantage-benefit"
    STORYBRAND = "storybrand"
    PICTURE_PROMISE_PROVE_PUSH = "picture-promise-prove-push"
    STAR_STORY_SOLUTION = "star-story-solution"
    COMPARISON = "comparison"
    LISTICLE = "listicle"
    HOW_TO = "how-to"
    CASE_STUDY = "case-study"
    THOUGHT_LEADERSHIP = "thought-leadership"


class PersuasionFramework(str, Enum):
    """Persuasion frameworks from persuasion-frameworks.md."""
    PAS = "PAS"
    BAB = "BAB"
    AIDA = "AIDA"
    FAB = "FAB"
    STORYBRAND = "StoryBrand"
    FOUR_PS = "4Ps"
    FOUR_U = "4U"
    SSA = "SSA"
    NONE = "none"


class CTAType(str, Enum):
    """Call-to-action types by commitment level."""
    READ_NEXT = "read-next"
    SUBSCRIBE = "subscribe"
    DOWNLOAD = "download"
    SIGN_UP = "sign-up"
    CONTACT = "contact"
    BUY = "buy"
    SHARE = "share"
    COMMENT = "comment"
    REFLECT = "reflect"


class CTACommitmentLevel(str, Enum):
    """CTA commitment levels from conversion-copywriting.md."""
    LOW = "low"      # read next, subscribe
    MEDIUM = "medium"  # download, sign up
    HIGH = "high"     # buy, contact sales


class GateStatus(str, Enum):
    """Validation gate status."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    WARNING = "warning"


class LintSeverity(str, Enum):
    """Lint issue severity."""
    WARNING = "warning"
    ALERT = "alert"


class OutputFormat(str, Enum):
    """Output format for CLI/Agent modes."""
    TEXT = "text"
    JSON = "json"
    YAML = "yaml"
    MARKDOWN = "markdown"
    TABLE = "table"
    CLI = "cli"
    AGENT = "agent"