"""
Output Format Renderers — Base classes and registry.

All renderers convert ResumeData to their target format.
"""
from abc import ABC, abstractmethod
from typing import Dict, Type, Optional, Any
from pathlib import Path

from resume_doctor.models.resume_data import ResumeData, OutputFormat


class BaseRenderer(ABC):
    """Abstract base class for all format renderers."""

    format: OutputFormat
    extension: str

    @abstractmethod
    def render(self, resume: ResumeData) -> str:
        """Convert ResumeData to formatted string."""
        pass

    @abstractmethod
    def get_instructions(self, resume: ResumeData) -> str:
        """Return usage instructions for this format."""
        pass

    def save(self, resume: ResumeData, output_path: Path) -> Path:
        """Render and save to file."""
        content = self.render(resume)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")
        return output_path


class RendererRegistry:
    """Registry mapping format -> renderer class."""

    _renderers: Dict[OutputFormat, Type[BaseRenderer]] = {}

    @classmethod
    def register(cls, format: OutputFormat, renderer_class: Type[BaseRenderer]):
        cls._renderers[format] = renderer_class

    @classmethod
    def get(cls, format: OutputFormat) -> Optional[Type[BaseRenderer]]:
        return cls._renderers.get(format)

    @classmethod
    def get_instance(cls, format: OutputFormat) -> Optional[BaseRenderer]:
        renderer_class = cls.get(format)
        if renderer_class:
            return renderer_class()
        return None

    @classmethod
    def available_formats(cls) -> list:
        return list(cls._renderers.keys())


# Import and register renderers
def _register_all():
    """Import all renderers and register them."""
    try:
        from .latex_renderer import LaTeXRenderer
        RendererRegistry.register(OutputFormat.LATEX, LaTeXRenderer)
    except ImportError:
        pass

    try:
        from .markdown_renderer import MarkdownRenderer
        RendererRegistry.register(OutputFormat.MARKDOWN, MarkdownRenderer)
    except ImportError:
        pass

    try:
        from .html_renderer import HTMLRenderer
        RendererRegistry.register(OutputFormat.HTML, HTMLRenderer)
    except ImportError:
        pass

    try:
        from .json_renderer import JSONRenderer
        RendererRegistry.register(OutputFormat.JSON, JSONRenderer)
    except ImportError:
        pass

    try:
        from .docx_renderer import DocxRenderer
        RendererRegistry.register(OutputFormat.DOCX, DocxRenderer)
    except ImportError:
        pass

    try:
        from .pdf_renderer import PDFRenderer
        RendererRegistry.register(OutputFormat.PDF, PDFRenderer)
    except ImportError:
        pass


# Auto-register on module load
_register_all()


def get_renderer(format: OutputFormat) -> Optional[BaseRenderer]:
    """Get renderer instance for format."""
    return RendererRegistry.get_instance(format)


def render_resume(resume: ResumeData, format: OutputFormat) -> str:
    """Convenience function to render resume in any format."""
    renderer = get_renderer(format)
    if not renderer:
        raise ValueError(f"No renderer available for format: {format}")
    return renderer.render(resume)


def get_format_instructions(format: OutputFormat, resume: ResumeData) -> str:
    """Get usage instructions for a format."""
    renderer = get_renderer(format)
    if not renderer:
        return f"No instructions available for {format.value}"
    return renderer.get_instructions(resume)