class GuardEventKey:
    def __init__(self, id) -> None:
        self.id = id

    def __hash__(self):
        return self.id.__hash__()

    def __eq__(self, other: object) -> bool:
        if type(self) != type(other):
            return False

        return self.id == other.id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}('{self.id}')"


class _RunEvent(GuardEventKey):
    def __init__(self) -> None:
        super().__init__("")

    def __str__(self) -> str:
        return "RUN"


RUN_EVENT = _RunEvent()


class _CloseEvent(GuardEventKey):
    def __init__(self) -> None:
        super().__init__("")

    def __str__(self) -> str:
        return "CLOSE"


CLOSE_EVENT = _CloseEvent()
