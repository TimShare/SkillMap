class AppException(Exception):
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(AppException):
    pass


class AlreadyExistsException(AppException):
    pass


class ValidationException(AppException):
    pass


class UnauthorizedException(AppException):
    pass


class ForbiddenException(AppException):
    pass
