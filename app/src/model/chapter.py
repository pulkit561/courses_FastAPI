from pydantic import BaseModel, Field

class Chapter(BaseModel):
    _id: str = Field(..., alias='_id')
    name: str
    text: str
    rating: int = 0

    class Config:
        allow_population_by_field_name = True