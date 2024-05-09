from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, MetaData, Relationship, SQLModel


# if TYPE_CHECKING: pass
# SCHEMA_NAME = "contenidos"
# metadata = MetaData(schema=SCHEMA_NAME)

class Post(SQLModel, table=True):  
    __tablename__ = "post"  
    # metadata = metadata  
    id_post: int = Field(default=None, primary_key=True)  
    descripcion: str = Field(max_length=255, nullable=False)  
    id_user: int = Field(default=None, foreign_key="user.id_user")
    id_debate: int = Field(default=None, foreign_key="debate.id_debate")