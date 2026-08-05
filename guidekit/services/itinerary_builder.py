from pathlib import Path

import yaml


def build_itineraries(
    directory: Path,
    output_file: Path,
) -> Path:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    content = ["# Cyprus 2026 Itineraries", ""]

    for path in sorted(directory.glob("*.yml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))

        content.append(f"## {data['name']}")
        content.append("")
        content.append(f"**Region:** {data['region']}")
        content.append("")
        content.append(f"**Duration:** {data['duration']}")
        content.append("")

        content.append("### Stops")
        for stop in data["stops"]:
            content.append(f"- {stop}")

        content.append("")

        content.append("### Activities")
        for activity in data["activities"]:
            content.append(f"- {activity}")

        content.append("")
        content.append("---")
        content.append("")

    output_file.write_text(
        "\n".join(content),
        encoding="utf-8",
    )

    return output_file
