from pydantic import BaseModel

class SchemaRequest(BaseModel):
    asignatura: str
    descripcion: str
    requisitos: str