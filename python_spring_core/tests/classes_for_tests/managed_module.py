"""this is just here for the find managed modules test"""
from python_spring_core.core.manager import manage


@manage
class IsManaged:
    def __init__(self) -> None:
        pass

class NotManaged:
    def __init__(self) -> None:
        pass