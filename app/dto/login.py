from dataclasses import dataclass

@dataclass(frozen=True)
class LoginResult:
    message: str