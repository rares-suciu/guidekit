from pathlib import Path

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

    generated = []

    index = output_dir / "index.md"
    index.write_text(
        f"# GuideKit Generated Guide\n\nTotal places: {len(places)}\n",
        encoding="utf-8",
    )
    generated.append(index)

    by_type: dict[str, list] = {}

    for place in places:
        by_type.setdefault(place.type, []).append(place)

    for place_type, items in by_type.items():
        filename = output_dir / f"{pluralize(place_type)}.md"

        content = [
            f"# {place_type.title()}s\n",
            "",
        ]

        for place in items:
            content.extend(
                [
                    f"## {place.name}",
                    "",
                    f"Region: {place.region}",
                    "",
                    f"Coordinates: {place.coordinates.latitude}, {place.coordinates.longitude}",
                    "",
                    "---",
                    "",
                ]
            )

        filename.write_text(
            "\n".join(content),
            encoding="utf-8",
        )

        generated.append(filename)

    return generated
