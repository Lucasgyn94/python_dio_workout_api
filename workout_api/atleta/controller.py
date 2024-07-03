from typing import Optional
from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException,  status
from fastapi_pagination import Page, paginate
from datetime import datetime

from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from workout_api.contrib.dependencies import DataBaseDependency
from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaOutCustomizado, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

router = APIRouter()

@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DataBaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        db_session.add(atleta_model)
        await db_session.commit()
    except IntegrityError as e:
        if "atletas_cpf_key" in str(e):  # Verifica se o erro é de chave única do CPF
            raise HTTPException(
                status_code=status.HTTP_303_SEE_OTHER,
                detail=f"Já existe um atleta cadastrado com o cpf: {atleta_in.cpf}"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Ocorreu um erro ao inserir os dados no banco'
            )

    await db_session.refresh(atleta_model)  # Atualiza o modelo para incluir as relações
    return AtletaOut.from_orm(atleta_model)  # Inclui as relações na resposta


@router.get(
    '/',
    summary='Consultar todos os Atletas',
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DataBaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()

    return [AtletaOut.model_validate(atleta) for atleta in atletas]

@router.get(
    '/filter', 
    summary='Consultar Atletas com filtros',
    status_code=status.HTTP_200_OK,
    response_model=Page[AtletaOutCustomizado],
)
async def query_with_filters(
    db_session: DataBaseDependency,
    nome: Optional[str] = None,
    cpf: Optional[str] = None,
) -> Page[AtletaOutCustomizado]:
    query = select(AtletaModel)
    if nome:
        query = query.filter(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter_by(cpf=cpf)
    atletas = (await db_session.execute(query)).scalars().all()

    return paginate(atletas)


@router.get(
    '/{id}', 
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DataBaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    return atleta

@router.patch(
    '/{id}', 
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DataBaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


@router.delete(
    '/{id}', 
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DataBaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Atleta não encontrado no id: {id}'
        )
    
    await db_session.delete(atleta)
    await db_session.commit()

