from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel


# if TYPE_CHECKING: pass
# SCHEMA_NAME = "contenidos"
# metadata = MetaData(schema=SCHEMA_NAME)

class User(SQLModel, table=True):  
    __tablename__ = "user"  
    # metadata = metadata  
    id_user: int = Field(default=None, primary_key=True)  
    nombre: str = Field(max_length=255, nullable=False)  