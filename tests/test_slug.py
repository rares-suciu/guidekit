from guidekit.utils.slug import slugify

def test_slugify() -> None:
    assert slugify("Cape Greco & Blue Lagoon") == "cape-greco-blue-lagoon"
