from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape
from guidekit.models import Place

def stars(value: int) -> str:
    return "★" * value + "☆" * (5 - value)

def render_places(places: list[Place], template_dir: Path, output_file: Path) -> Path:
    env = Environment(loader=FileSystemLoader(template_dir), autoescape=select_autoescape(default=False), trim_blocks=True, lstrip_blocks=True)
    env.filters["stars"] = stars
    template = env.get_template("places.md.j2")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(template.render(places=places), encoding="utf-8")
    return output_file
