import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .. import entities, models
from ..database import get_db

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/stations", tags=["Stations"])


@router.get("", response_model=list[models.Station])
async def get_stations(
    db: AsyncSession = Depends(get_db),
):
    stmt = select(entities.Station).options(
        joinedload(entities.Station.planet, innerjoin=True)
    )
    return (await db.execute(stmt)).scalars().all()


@router.get("/{station_id}", response_model=models.Station)
async def get_station(
    station_id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(entities.Station)
        .options(joinedload(entities.Station.planet, innerjoin=True))
        .filter(entities.Station.id == station_id)
        .limit(1)
    )
    station = (await db.execute(stmt)).scalar_one_or_none()
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return station


@router.post("", response_model=models.Station)
async def create_station(
    request: models.CreateStation, db: AsyncSession = Depends(get_db)
):
    planet = await db.get(entities.Planet, request.planet_id)
    if planet is None:
        raise HTTPException(status_code=404, detail="Planet not found")

    station = entities.Station()
    station.id = request.id
    station.name = request.name
    station.type = request.type
    station.planet_id = request.planet_id
    station.planet = planet
    station.population = request.population
    station.established_on = request.established_on

    db.add(station)
    await db.commit()

    return station


@router.delete("/{station_id}", response_model=models.Station)
async def delete_station(
    station_id: str,
    db: AsyncSession = Depends(get_db),
):
    stmt = (
        select(entities.Station)
        .options(joinedload(entities.Station.planet, innerjoin=True))
        .filter(entities.Station.id == station_id)
        .limit(1)
    )
    station = (await db.execute(stmt)).scalar_one_or_none()
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    logger.info(f"Deleting station {station.name}.")

    await db.delete(station)
    await db.commit()

    return station
