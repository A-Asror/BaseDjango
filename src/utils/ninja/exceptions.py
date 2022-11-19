from ninja.errors import HttpError


class AuthenticationFailed(HttpError):
    def __init__(self, message: str = "Unauthorized", status_code: int = 401) -> None:
        super().__init__(status_code=status_code, message=message)


class PermissionFailed(HttpError):
    def __init__(self, message: str = "permission denied", status_code: int = 403) -> None:
        super().__init__(status_code=status_code, message=message)


class ValidationError(HttpError):
    def __init__(self, status_code: int = 400, message: str = "Bad Request") -> None:
        super().__init__(status_code=status_code, message=message)
