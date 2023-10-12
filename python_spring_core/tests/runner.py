import pytest

class Runner:

    @staticmethod
    def start_tests(*args):
        pytest.main(*args)
if __name__ == "__main__":
    # can add arguments for pytest in the provided list
    Runner.start_tests(["-v","-s"])