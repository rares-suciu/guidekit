from pathlib import Path

from pydantic import ValidationError as PydanticValidationError

from guidekit.models import Place
from guidekit.utils.yaml_io import read_yaml


def load_places(directory: Path) -> list[Place]:
    places: list[Place] = []
    errors: list[str] = []
    if not directory.exists():
        return places
    for path in sorted(directory.glob("*.yml")):
        try:
            places.append(Place.model_validate(read_yaml(path)))
        except PydanticValidationError as exc:
            errors.append(f"{path}: {exc}")
    if errors:
        raise ValueError("\n\n".join(errors))
    return places
