import pytest


class FakeLogger:
    def __init__(self):
        self.call_count = 0
        self.messages = []

    def __call__(self, message):
        self.call_count += 1
        self.messages.append(message)


@pytest.fixture(scope="function")
def fixt_logger() -> FakeLogger:
    return FakeLogger()
