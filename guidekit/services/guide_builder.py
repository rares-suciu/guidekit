from pathlib import Path

from guidekit.builders.markdown import render_places
from guidekit.services.place_service import load_places


def pluralize(value: str) -> str:
    irregular = {
        "beach": "beaches",
        "city": "cities",
        "activity": "activities",
    }

    if value in irregular:
        return irregular[value]

    if value.endswith("y"):
        return value[:-1] + "ies"

    if value.endswith(("s", "x", "z", "ch", "sh")):
        return value + "es"

    return value + "s"


def build_guide(
    places_dir: Path,
    output_dir: Path,
) -> list[Path]:
    places = load_places(places_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "places.md"

    render_places(
        places,
        Path("templates"),
        output_file,
    )

    return [
        output_dir / "places.md",
    ]
