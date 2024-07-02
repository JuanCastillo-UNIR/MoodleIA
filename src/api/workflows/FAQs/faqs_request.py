from pydantic import BaseModel

class FAQsRequest(BaseModel):
    pregunta: str
    FAQs: str