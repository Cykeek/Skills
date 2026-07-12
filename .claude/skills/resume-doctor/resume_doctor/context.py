"""
Resume Doctor — Shared context, configuration, and path utilities.
Provides consistent output paths, session management, and defaults.
"""
import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class RunContext:
    """Execution context for a single resume-doctor run."""
    resume_path: str
    job_path: Optional[str] = None
    mode: str = "designer-polish"
    out_dir: str = "output"
    base_name: Optional[str] = None
    portfolio_path: Optional[str] = None
    phase_stop: Optional[int] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        # Store as string, resolve to Path when needed
        self.out_dir = str(self.out_dir)

    @property
    def out_dir_path(self) -> Path:
        """Get out_dir as Path object."""
        return Path(self.out_dir)

    @property
    def name(self) -> str:
        """Derive base name from resume file if not provided."""
        if self.base_name:
            return self.base_name
        stem = Path(self.resume_path).stem
        return stem.replace(".", "_")

    @property
    def paths(self) -> "OutputPaths":
        """All output paths for this run."""
        return OutputPaths(self)


@dataclass
class OutputPaths:
    """All output file paths for a run."""
    ctx: RunContext

    @property
    def tailored_tex(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_tailored.tex"

    @property
    def tailored_pdf(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_tailored.pdf"

    @property
    def tailored_txt(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_tailored.txt"

    @property
    def normalized_txt(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_normalized.txt"

    @property
    def gap_report_md(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_gap_report.md"

    @property
    def injection_map_json(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_injection_map.json"

    @property
    def audit_report_json(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_audit.json"

    @property
    def validation_report_json(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_validation.json"

    @property
    def profile_yaml(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_profile.yaml"

    @property
    def job_analysis_json(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_job_analysis.json"

    @property
    def run_context_json(self) -> Path:
        return self.ctx.out_dir_path / f"{self.ctx.name}_run_context.json"


def create_context(
    resume_path: str,
    job_path: Optional[str] = None,
    mode: str = "designer-polish",
    out_dir: str = "output",
    base_name: Optional[str] = None,
    portfolio_path: Optional[str] = None,
    phase_stop: Optional[int] = None,
) -> RunContext:
    """Create a run context with auto-generated output paths."""
    return RunContext(
        resume_path=resume_path,
        job_path=job_path,
        mode=mode,
        out_dir=out_dir,
        base_name=base_name,
        portfolio_path=portfolio_path,
        phase_stop=phase_stop,
    )


def save_context(ctx: RunContext, path: Optional[Path] = None) -> Path:
    """Persist run context to JSON for traceability."""
    if path is None:
        path = ctx.paths.run_context_json
    path.parent.mkdir(parents=True, exist_ok=True)
    data = asdict(ctx)
    # Convert Path objects to strings for serialization
    data["paths"] = {k: str(v) for k, v in asdict(ctx.paths).items()}
    # Ensure out_dir is a string
    data["out_dir"] = ctx.out_dir
    path.write_text(json.dumps(data, indent=2))
    return path


def load_context(path: Path) -> RunContext:
    """Load run context from JSON."""
    data = json.loads(path.read_text())
    # Reconstruct context (paths will be recomputed)
    ctx = RunContext(
        resume_path=data["resume_path"],
        job_path=data.get("job_path"),
        mode=data.get("mode", "designer-polish"),
        out_dir=data.get("out_dir", "output"),
        base_name=data.get("base_name"),
        portfolio_path=data.get("portfolio_path"),
        phase_stop=data.get("phase_stop"),
        created_at=data.get("created_at", datetime.now().isoformat()),
    )
    return ctx


def resolve_output_path(
    ctx: RunContext,
    path_arg: Optional[str],
    default_suffix: str,
    default_dir: Optional[Path] = None,
) -> Path:
    """
    Resolve an output path from CLI argument or auto-generate.

    Args:
        ctx: Run context
        path_arg: Explicit path from CLI (--out, --out-dir, etc.)
        default_suffix: Suffix for auto-generated filename (e.g., "_audit.json")
        default_dir: Directory to use if path_arg is a bare filename

    Returns:
        Resolved absolute Path
    """
    if path_arg:
        p = Path(path_arg)
        if p.is_absolute() or p.parent != Path("."):
            return p
        # Relative path - put in context out_dir
        return ctx.out_dir_path / p

    # Auto-generate
    target_dir = default_dir or ctx.out_dir_path
    return target_dir / f"{ctx.name}{default_suffix}"


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists, return path."""
    path.mkdir(parents=True, exist_ok=True)
    return path