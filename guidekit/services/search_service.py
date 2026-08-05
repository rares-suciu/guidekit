from pathlib import Path

from guidekit.services.place_service import load_places


def search_places(query: str, directory: Path) -> list:
    query = query.lower().strip()

    results = []

    for place in load_places(directory):
        searchable = " ".join(
            [
                place.name,
                place.type,
                place.region,
                " ".join(place.features.keys()),
            ]
        ).lower()

        if query in searchable:
            results.append(place)

    return results
