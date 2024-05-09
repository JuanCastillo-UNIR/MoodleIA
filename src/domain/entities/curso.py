from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel


# if TYPE_CHECKING: pass
# SCHEMA_NAME = "contenidos"
# metadata = MetaData(schema=SCHEMA_NAME)

class Curso(SQLModel, table=True):  
    __tablename__ = "curso"  
    # metadata = metadata  
    id_curso: Optional[int] = Field(default=None, primary_key=True)  
    nombre_curso: str = Field(max_length=255, nullable=False)  