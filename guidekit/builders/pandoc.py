from pathlib import Path
import shutil, subprocess

def build_with_pandoc(chapters_dir: Path, output_file: Path, pdf_engine: str | None = None) -> Path:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        raise RuntimeError("Pandoc is not installed or not available on PATH.")
    chapters = sorted(chapters_dir.glob("*.md"))
    if not chapters:
        raise RuntimeError(f"No Markdown chapters found in {chapters_dir}")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    command = [pandoc, *(str(path) for path in chapters), "--toc", "-o", str(output_file)]
    if pdf_engine:
        command.extend(["--pdf-engine", pdf_engine])
    subprocess.run(command, check=True)
    return output_file
