from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    id: int | None = None
    user_name: str | None = None
    sex: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        """序列化为字典，字段名与 Java 保持一致（userName）。"""
        return {"id": self.id, "userName": self.user_name, "sex": self.sex}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(
            id=data.get("id"),
            user_name=data.get("userName"),
            sex=data.get("sex"),
        )

    def __str__(self) -> str:
        return f"User(id={self.id}, userName={self.user_name}, sex={self.sex})"

