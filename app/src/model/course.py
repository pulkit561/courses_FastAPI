from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Course(BaseModel):
    id: str = Field(..., alias='_id')
    name: str
    date: datetime
    description: str
    domain: List[str] = Field(default_factory=list)
    chapters: List[str] = Field(default_factory=list)
    courseRating: int = 0

    class Config:
        allow_population_by_field_name = True


    