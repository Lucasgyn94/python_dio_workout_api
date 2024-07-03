from pydantic import Field, PositiveFloat
from typing import Annotated, Optional

from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.categorias.schemas import CategoriaIn, CategoriaOut
from workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta, CentroTreinamentoOut

class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do Atleta', example='Lucas', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do Atleta', example='12345678900', max_length=11)]
    idade: Annotated[int, Field(description='Idade do Atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do Atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do Atleta', example=1.80)]
    sexo: Annotated[str, Field(description='Sexo do Atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de Treinamento do  Atleta')]

class AtletaIn(Atleta):
    categoria_id: Annotated[int, Field(description='ID da Categoria do Atleta')]
    centro_treinamento_id: Annotated[int, Field(description='ID do Centro de Treinamento do Atleta')]

class AtletaOut(AtletaIn, OutMixin):
    categoria: Optional[CategoriaOut] = None
    centro_treinamento: Optional[CentroTreinamentoOut] = None

class AtletaOutCustomizado(OutMixin):
    nome: str
    centro_treinamento: Optional[CentroTreinamentoOut] = None
    categoria: Optional[CategoriaOut] = None

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example='Lucas', max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=30)]