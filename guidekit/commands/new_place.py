from pathlib import Path

from rich.console import Console

from guidekit.utils.slug import slugify
from guidekit.utils.yaml_io import write_yaml

console = Console()


def run() -> None:
    name = input("Name: ").strip()
    place_type = input("Type (beach, restaurant, viewpoint, village, museum): ").strip().lower()
    region = input("Region: ").strip()

    latitude = float(input("Latitude: ").strip())
    longitude = float(input("Longitude: ").strip())

    family = int(input("Family rating (0-5): ").strip())
    snorkeling = int(input("Snorkeling rating (0-5): ").strip())
    photography = int(input("Photography rating (0-5): ").strip())
    parking = int(input("Parking rating (0-5): ").strip())

    features_input = input("Features (comma separated): ").strip()
    features = {}
    if features_input:
        for feature in features_input.split(","):
            features[feature.strip()] = True

    data = {
        "name": name,
        "type": place_type,
        "region": region,
        "coordinates": {
            "latitude": latitude,
            "longitude": longitude,
        },
        "ratings": {
            "family": family,
            "snorkeling": snorkeling,
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
