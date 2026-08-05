from guidekit.models import Place


def test_place_validation() -> None:
    place = Place.model_validate(
        {
            "name": "Green Bay",
            "type": "beach",
            "region": "Protaras",
            "coordinates": {"latitude": 34.9955, "longitude": 34.0734},
        }
    )
    assert place.name == "Green Bay"
