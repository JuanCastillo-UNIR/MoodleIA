from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel


# if TYPE_CHECKING: pass
# SCHEMA_NAME = "contenidos"
# metadata = MetaData(schema=SCHEMA_NAME)

class Debate(SQLModel, table=True):  
    __tablename__ = "debate"  
    # metadata = metadata  
    id_debate: int = Field(default=None, primary_key=True)  
    nombre_debate: str = Field(max_length=255, nullable=False)  
    id_foro: int = Field(default=None, foreign_key="foro.id_foro")
    id_curso: int = Field(default=None, foreign_key="curso.id_curso")