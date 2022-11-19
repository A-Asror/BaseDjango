from ninja.errors import HttpError


class AuthenticationFailed(HttpError):
    def __init__(self, message: str = "Unauthorized", status_code: int = 401) -> None:
        super().__init__(status_code=status_code, message=message)


class PermissionFailed(HttpError):
    def __init__(self, message: str = "permission denied", status_code: int = 403) -> None:
        super().__init__(status_code=status_code, message=message)


class ValidationError(HttpError):
    def __init__(self, message: str = "Bad Request", status_code: int = 400) -> None:
        super().__init__(message=message, status_code=status_code)
