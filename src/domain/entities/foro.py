from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel


# if TYPE_CHECKING: pass
# SCHEMA_NAME = "contenidos"
# metadata = MetaData(schema=SCHEMA_NAME)

class Foro(SQLModel, table=True):  
    __tablename__ = "foro"  
    # metadata = metadata  
    id_foro: int = Field(default=None, primary_key=True)  
    tema: str = Field(max_length=255, nullable=False)  
    descripcion: Optional[str] = Field(max_length=255, nullable=True)  
    id_curso: int = Field(default=None, foreign_key="curso.id_curso")