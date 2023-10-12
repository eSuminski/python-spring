

class Dependency:

    def __init__(self) -> None:
        print("Dependency object made")

class Reciever:

    def __init__(self, dependency: Dependency = None) -> None:
        self.dependency = dependency
        print("Receiver object made")

class MissingNoneDefault:

    def __init__(self, dependency: Dependency) -> None:
        self.dependency = dependency
        print("MissingNoneDefault created: this shouldn't happen")

