"""
Phases Package
==============
5-phase content creation pipeline.
"""

from content_writer_skill.phases.phase1_discover import (
    DiscoverAlignPhase,
    Phase1Result,
    run_discover_align,
    load_brief_from_file,
    load_brief_from_json,
)

from content_writer_skill.phases.phase2_outline import (
    OutlinePhase,
    Phase2Result,
    run_outline,
)

from content_writer_skill.phases.phase3_draft import (
    DraftPhase,
    Phase3Result,
    run_draft,
)

from content_writer_skill.phases.phase4_revise import (
    RevisePhase,
    Phase4Result,
    run_revise,
)

from content_writer_skill.phases.phase5_pre_output import (
    PreOutputPhase,
    Phase5Result,
    run_pre_output,
)

__all__ = [
    # Phase 1
    "DiscoverAlignPhase",
    "Phase1Result",
    "run_discover_align",
    "load_brief_from_file",
    "load_brief_from_json",
    # Phase 2
    "OutlinePhase",
    "Phase2Result",
    "run_outline",
    # Phase 3
    "DraftPhase",
    "Phase3Result",
    "run_draft",
    # Phase 4
    "RevisePhase",
    "Phase4Result",
    "run_revise",
    # Phase 5
    "PreOutputPhase",
    "Phase5Result",
    "run_pre_output",
]