from dataclasses import dataclass


@dataclass
class SignIn:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str
