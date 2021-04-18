from fastapi import APIRouter, Depends

from ..app import is_connected

from ..schemas import Horaire


router = APIRouter(
    prefix="/horaire",
    tags=["horaire"],
)


@router.get("", response_model=Horaire)
async def get_horaire():
    """Provides information about the timetable."""

    horaire = await Horaire.get()

    return horaire


@router.put("", response_model=Horaire, dependencies=[Depends(is_connected)])
async def update_horaire(horaire: Horaire):
    """Updates the timetable."""

    response = await Horaire.edit(horaire)

    return response
