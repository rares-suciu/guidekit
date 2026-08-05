from pathlib import Path
import shutil, subprocess
import typer
from rich.console import Console
from rich.table import Table
from guidekit.builders.markdown import render_places
from guidekit.builders.pandoc import build_with_pandoc
from guidekit.services.chapter_service import create_chapter
from guidekit.services.place_service import load_places

app = typer.Typer(no_args_is_help=True, help="Build static guides from Markdown and YAML.")
console = Console()

@app.command("doctor")
def doctor() -> None:
    table = Table(title="GuideKit Doctor")
    table.add_column("Check")
    table.add_column("Status")
    for command in ("python", "pandoc", "mkdocs"):
        table.add_row(command, "OK" if shutil.which(command) else "MISSING")
    console.print(table)

@app.command("validate")
def validate(places_dir: Path = Path("data/places")) -> None:
    places = load_places(places_dir)
    console.print(f"[green]Validated {len(places)} place file(s).[/green]")

@app.command("new-chapter")
def new_chapter(number: int, title: str, chapters_dir: Path = Path("book/chapters"), template: Path = Path("templates/chapter.md")) -> None:
    path = create_chapter(number, title, chapters_dir, template)
    console.print(f"[green]Created:[/green] {path}")

@app.command("build-markdown")
def build_markdown(places_dir: Path = Path("data/places"), template_dir: Path = Path("templates"), output: Path = Path("build/places.md")) -> None:
    path = render_places(load_places(places_dir), template_dir, output)
    console.print(f"[green]Created:[/green] {path}")

@app.command("build-docx")
def build_docx(chapters_dir: Path = Path("book/chapters"), output: Path = Path("docx/GuideKit_Book.docx")) -> None:
    console.print(f"[green]Created:[/green] {build_with_pandoc(chapters_dir, output)}")

@app.command("build-pdf")
def build_pdf(chapters_dir: Path = Path("book/chapters"), output: Path = Path("pdf/GuideKit_Book.pdf"), pdf_engine: str = "xelatex") -> None:
    console.print(f"[green]Created:[/green] {build_with_pandoc(chapters_dir, output, pdf_engine)}")

@app.command("serve")
def serve() -> None:
    mkdocs = shutil.which("mkdocs")
    if not mkdocs:
        raise typer.BadParameter("MkDocs is not installed or not on PATH.")
    subprocess.run([mkdocs, "serve"], check=True)
