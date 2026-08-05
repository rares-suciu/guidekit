from pathlib import Path
from guidekit.utils.slug import slugify

DEFAULT_TEMPLATE = "# {{TITLE}}\n\n> **Status:** Draft\n\n## Overview\n"

def create_chapter(number: int, title: str, chapters_dir: Path, template_path: Path | None) -> Path:
    chapters_dir.mkdir(parents=True, exist_ok=True)
    destination = chapters_dir / f"{number:02d}-{slugify(title)}.md"
    if destination.exists():
        raise FileExistsError(f"Chapter already exists: {destination}")
    template = template_path.read_text(encoding="utf-8") if template_path and template_path.exists() else DEFAULT_TEMPLATE
    destination.write_text(template.replace("{{TITLE}}", title), encoding="utf-8")
    return destination
