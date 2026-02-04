class AppException(Exception):
    """Базовое приложение исключение"""
    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundException(AppException):
    """Ресурс не найден"""
    pass


class AlreadyExistsException(AppException):
    """Ресурс уже существует"""
    pass


class ValidationException(AppException):
    """Ошибка валидации"""
    pass


class UnauthorizedException(AppException):
    """Не авторизован"""
    pass


class ForbiddenException(AppException):
    """Доступ запрещен"""
    pass
