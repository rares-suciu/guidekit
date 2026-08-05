import shutil
import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from guidekit.builders.markdown import render_places
from guidekit.builders.pandoc import build_with_pandoc
from guidekit.commands import new_content, new_place
from guidekit.services.chapter_service import create_chapter
from guidekit.services.guide_builder import build_guide
from guidekit.services.place_service import load_places
from guidekit.services.search_service import search_places
from guidekit.services.stats_service import calculate_stats

app = typer.Typer(no_args_is_help=True, help="Build static guides from Markdown and YAML.")
console = Console()


@app.command("new-place")
def new_place_command() -> None:
    """Create a new place YAML record."""
    new_place.run()


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
def new_chapter(
    number: int,
    title: str,
    chapters_dir: Path = Path("book/chapters"),
    template: Path = Path("templates/chapter.md"),
) -> None:
    path = create_chapter(number, title, chapters_dir, template)
    console.print(f"[green]Created:[/green] {path}")


@app.command("build-markdown")
def build_markdown(
    places_dir: Path = Path("data/places"),
    template_dir: Path = Path("templates"),
    output: Path = Path("build/places.md"),
) -> None:
    path = render_places(load_places(places_dir), template_dir, output)
    console.print(f"[green]Created:[/green] {path}")


@app.command("build-docx")
def build_docx(
    chapters_dir: Path = Path("book/chapters"), output: Path = Path("docx/GuideKit_Book.docx")
) -> None:
    console.print(f"[green]Created:[/green] {build_with_pandoc(chapters_dir, output)}")


@app.command("build-pdf")
def build_pdf(
    chapters_dir: Path = Path("book/chapters"),
    output: Path = Path("pdf/GuideKit_Book.pdf"),
    pdf_engine: str = "xelatex",
) -> None:
    console.print(f"[green]Created:[/green] {build_with_pandoc(chapters_dir, output, pdf_engine)}")


@app.command("serve")
def serve() -> None:
    mkdocs = shutil.which("mkdocs")
    if not mkdocs:
        raise typer.BadParameter("MkDocs is not installed or not on PATH.")
    subprocess.run([mkdocs, "serve"], check=True)


@app.command("new")
def new_content_command(
    content_type: str = typer.Argument(
        ...,
        help="Content type: beach, restaurant, viewpoint, village, museum",
    ),
) -> None:
    """Create a new content item."""
    new_content.run(content_type)


@app.command("search")
def search(
    query: str = typer.Argument(..., help="Search text"),
    places_dir: Path = Path("data/places"),
) -> None:
    """Search places."""
    results = search_places(query, places_dir)

    if not results:
        console.print("[yellow]No results found.[/yellow]")
        return

    for place in results:
        console.print(f"[green]{place.name}[/green] ({place.type}) - {place.region}")


@app.command("stats")
def stats(
    places_dir: Path = Path("data/places"),
) -> None:
    """Show guide statistics."""
    result = calculate_stats(places_dir)

    console.print("[bold]GuideKit Statistics[/bold]")
    console.print(f"Places: {result['total']}")

    console.print("\n[bold]By type:[/bold]")
    for key, value in result["types"].items():
        console.print(f"  {key}: {value}")

    console.print("\n[bold]Features:[/bold]")
    for key, value in result["features"].items():
        console.print(f"  {key}: {value}")

    console.print("\n[bold]Top rated:[/bold]")
    for place in result["top_rated"]:
        console.print(f"  {place.name}")


@app.command("build")
def build(
    places_dir: Path = Path("data/places"),
    output_dir: Path = Path("build"),
) -> None:
    """Generate guide pages from content data."""
    files = build_guide(places_dir, output_dir)

    console.print("[green]Generated:[/green]")
    for file in files:
        console.print(f"  {file}")
