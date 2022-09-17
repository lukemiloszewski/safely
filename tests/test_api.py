import pytest

from safely.api import SafeResult, safely


def test_with_function():
    def f(value=None):
        return value or 1

    with pytest.raises(TypeError):
        safely(f=f)

    result = safely(f)()
    assert isinstance(result, SafeResult)
    assert result.value == 1
    assert result.error is None

    result = safely(f)(value=123)
    assert isinstance(result, SafeResult)
    assert result.value == 123
    assert result.error is None

    result = safely()(f)()
    assert isinstance(result, SafeResult)
    assert result.value == 1
    assert result.error is None

    result = safely()(f)(value=123)
    assert isinstance(result, SafeResult)
    assert result.value == 123
    assert result.error is None


def test_with_logger(fixt_logger):
    def f(exc_value="Something went wrong"):
        raise Exception(exc_value)

    safely(f, logger=fixt_logger)()
    assert fixt_logger.call_count == 1
    assert fixt_logger.messages[0] == "Exception raised: Something went wrong"

    safely(f, logger=fixt_logger, message="OH NO: {exc_value}")(exc_value="!!!")
    assert fixt_logger.call_count == 2
    assert fixt_logger.messages[1] == "OH NO: !!!"


def test_without_logger(capsys):
    def f():
        ...

    safely(f)()

    stdout, stderr = capsys.readouterr()
    assert stdout == ""
    assert stderr == ""


def test_with_decorator():
    @safely
    def f(value=None):
        return value or 1

    result = f()
    assert isinstance(result, SafeResult)
    assert result.value == 1
    assert result.error is None

    result = f(value=123)
    assert isinstance(result, SafeResult)
    assert result.value == 123
    assert result.error is None


def test_with_decorator_arguments(fixt_logger):
    @safely(logger=fixt_logger)
    def f():
        raise Exception("Something went wrong")

    f()

    assert fixt_logger.call_count == 1
    assert fixt_logger.messages[0] == "Exception raised: Something went wrong"


def test_with_exception():
    @safely
    def f():
        raise Exception("Something went wrong")

    result = f()

    assert isinstance(result, SafeResult)
    assert result.value is None
    assert result.error is not None
    assert result.has_error
    assert isinstance(result.error, Exception)
    assert str(result.error) == "Something went wrong"
