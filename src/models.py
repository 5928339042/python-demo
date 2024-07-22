from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PastDatetime

from .entities import StationType


class CreatePlanet(BaseModel):
    id: str
    name: str = Field(strict=True)


class UpdatePlanet(BaseModel):
    name: str = Field(strict=True)
    population_millions: NonNegativeInt = Field(strict=True)


class Planet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CreateStation(BaseModel):
    id: str
    name: str = Field(strict=True)
    population: NonNegativeInt = Field(strict=True)
    established_on: PastDatetime
    type: StationType
    planet_id: str


class Station(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    population: int
    established_on: PastDatetime
    type: StationType
    planet_id: str
    planet: Planet
