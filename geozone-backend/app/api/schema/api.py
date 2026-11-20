from pydantic import BaseModel

class ApiResponse[T](BaseModel):
    status: int
    error: str | None
    data: T
