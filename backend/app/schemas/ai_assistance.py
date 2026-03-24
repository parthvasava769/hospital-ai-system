from pydantic import BaseModel
from typing import List, Optional


class SymptomRequest(BaseModel):
    symptoms: str


class AICommand(BaseModel):
    command: str


class AIResponse(BaseModel):
    possible_conditions: list[str]
    recommended_tests: list[str]

    class Config:
        from_attributes = True

class AIMessageResponse(BaseModel):
    message: str