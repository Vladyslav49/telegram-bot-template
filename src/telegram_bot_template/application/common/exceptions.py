from typing import final


class ApplicationError(Exception):
    pass


class UnexpectedError(ApplicationError):
    pass


@final
class CommitError(UnexpectedError):
    pass


@final
class RollbackError(UnexpectedError):
    pass


@final
class SaverError(UnexpectedError):
    pass
