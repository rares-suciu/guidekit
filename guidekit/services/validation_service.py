from pathlib import Path

from guidekit.services.place_service import load_places


def validate_places(directory: Path) -> list[str]:
    warnings: list[str] = []

    places = load_places(directory)

    for place in places:
        prefix = f"{place.name}:"

        if place.type == "beach":
            if not place.best_time:
                warnings.append(f"{prefix} missing best_time")

            if not place.estimated_visit:
                warnings.append(f"{prefix} missing estimated_visit")

        if place.features.get("snorkeling") and place.ratings.snorkeling == 0:
            warnings.append(f"{prefix} snorkeling feature enabled but rating is 0")

        if place.features.get("sunrise") and place.coordinates.latitude == 0:
            warnings.append(f"{prefix} sunrise enabled but coordinates missing")

    return warnings
