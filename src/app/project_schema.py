from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, Any
from fastapi import Response
import orjson

T = TypeVar("T")


@dataclass
class ApiResponse(Response, Generic[T]):
    status_code: int
    message: str
    status: str
    data: Optional[T] = None
    media_type: str = field(default="application/json", init=False)

    def __post_init__(self):
        body = self.render(None)
        super().__init__(
            content=body,
            status_code=self.status_code,
            media_type=self.media_type,
        )

    @classmethod
    def success(cls, message="Success", data: Optional[T] = None, code: int = 200):
        obj = cls(status_code=code, message=message, status="success", data=data)
        return obj

    @classmethod
    def error(cls, message="Error", data: Optional[T] = None, code: int = 200):
        obj = cls(status_code=code, message=message, status="error", data=data)
        return obj

    def render(self, content: Any) -> bytes:
        return orjson.dumps({
            "code": self.status_code,
            "message": self.message,
            "status": self.status,
            "data": self.data,
        })