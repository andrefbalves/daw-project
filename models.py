from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    full_name: str | None = None
    email: str | None = None

    @classmethod
    def from_row(cls, row):
        if row is None:
            return None

        return cls(
            id=row["id"],
            username=row["username"],
            password_hash=row["password_hash"],
            full_name=row["full_name"],
            email=row["email"],
        )
