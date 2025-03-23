from fastapi import APIRouter, status, Body
from workout_api.atleta.schemas import AtletaIn

from workout_api.contrib.dependencias import DatabaseDependency

router = APIRouter()

@router.post(
    path='/', 
    summary="Criar novo atleta",
    status_code=status.HTTP_201_CREATED
)
async def post(db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)):
    pass