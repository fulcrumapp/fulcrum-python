class InvalidAPIVersionException(Exception):
    """An invalid API version was passed."""


class NotFoundException(Exception):
    """The resource could not be found."""


class UnauthorizedException(Exception):
    """The API key supplied is not authorized to access this resource."""


class InternalServerErrorException(Exception):
    """There was an error while processing your request."""


class RateLimitExceededException(Exception):
    """The API key's rate limit was exceeded."""
