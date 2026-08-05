from pydantic import BaseModel, Field, field_validator


class Coordinates(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class Ratings(BaseModel):
    family: int = Field(default=0, ge=0, le=5)
    snorkeling: int = Field(default=0, ge=0, le=5)
    photography: int = Field(default=0, ge=0, le=5)
    parking: int = Field(default=0, ge=0, le=5)


class Place(BaseModel):
    name: str
    type: str
    region: str
    coordinates: Coordinates
    ratings: Ratings = Ratings()
    features: dict[str, bool] = {}
    best_time: str = ""
    estimated_visit: str = ""
    status: str = "draft"

    @field_validator("name", "type", "region")
    @classmethod
    def must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("must not be blank")
        return value
