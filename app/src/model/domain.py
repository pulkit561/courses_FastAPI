from pydantic import BaseModel, Field

class Domain(BaseModel):
    _id: str = Field(..., alias='_id')
    name: str

    class Config:
        allow_population_by_field_name = True