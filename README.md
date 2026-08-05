# GuideKit

GuideKit is a static guide generator that combines Markdown chapters and YAML place data into generated Markdown, DOCX, PDF, and an MkDocs website.

## Install

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## Commands

```powershell
guidekit doctor
guidekit validate
guidekit new-chapter 6 "Cape Greco"
guidekit build-markdown
guidekit build-docx
guidekit build-pdf
guidekit serve
```
