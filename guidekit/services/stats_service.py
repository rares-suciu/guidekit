from collections import Counter
from pathlib import Path

from guidekit.services.place_service import load_places


def calculate_stats(directory: Path) -> dict:
    places = load_places(directory)

    types = Counter(place.type for place in places)

    features = Counter()

    for place in places:
        for feature, enabled in place.features.items():
            if enabled:
                features[feature] += 1

    top_rated = sorted(
        places,
        key=lambda place: (
            place.ratings.family
            + place.ratings.snorkeling
            + place.ratings.photography
            + place.ratings.parking
        ),
        reverse=True,
    )

    return {
        "total": len(places),
        "types": dict(types),
        "features": dict(features),
        "top_rated": top_rated[:5],
    }
