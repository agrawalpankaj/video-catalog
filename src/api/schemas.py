from typing import List

from pydantic import BaseModel


class Video(BaseModel):
    id: int
    title: str
    description: str
    duration: int

    class Config:
        orm_mode = True


class Error(BaseModel):
    data: None
    status_code: int
    message: str
    error: str


class ErrorResponse(BaseModel):
    detail: List[Error]
