from pathlib import Path

from rich.console import Console

from guidekit.utils.slug import slugify
from guidekit.utils.yaml_io import write_yaml

console = Console()

CONTENT_TYPES = {
    "beach": {
        "features": [
            "snorkeling",
            "turtles",
            "cliff_views",
            "underwater_sculptures",
            "sunrise",
        ]
    },
    "restaurant": {
        "features": [
            "sea_view",
            "outdoor_seating",
            "family_friendly",
        ]
    },
    "viewpoint": {
        "features": [
            "sunrise",
            "sunset",
            "photography",
        ]
    },
    "village": {
        "features": [
            "traditional_food",
            "walking_routes",
            "local_crafts",
        ]
    },
    "museum": {
        "features": [
            "indoor",
            "family_friendly",
        ]
    },
}


def run(content_type: str) -> None:
    if content_type not in CONTENT_TYPES:
        available = ", ".join(CONTENT_TYPES.keys())
        raise ValueError(f"Unknown type '{content_type}'. Available: {available}")

    print(f"Creating new {content_type}")

    name = input("Name: ").strip()
    region = input("Region: ").strip()

    latitude = float(input("Latitude: ").strip())
    longitude = float(input("Longitude: ").strip())

    family = int(input("Family rating (0-5): ").strip())
    photography = int(input("Photography rating (0-5): ").strip())
    parking = int(input("Parking rating (0-5): ").strip())

    features = {}

    print("Available features:")
    for feature in CONTENT_TYPES[content_type]["features"]:
        answer = input(f"{feature}? (y/n): ").lower()
        features[feature] = answer == "y"

    data = {
        "name": name,
        "type": content_type,
        "region": region,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "ratings": {
            "family": family,
            "snorkeling": (5 if features.get("snorkeling") else 0),
            "photography": photography,
            "parking": parking,
        },
        "features": features,
        "best_time": "",
        "estimated_visit": "",
        "status": "draft",
    }

    output = Path("data/places") / f"{slugify(name)}.yml"

    write_yaml(output, data)

    console.print(f"[green]Created:[/green] {output}")
