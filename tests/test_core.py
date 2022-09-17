from safely.core import SafeResult


def test_safe_result():
    result = SafeResult()
    assert result.value is None
    assert result.error is None
    assert result.has_error is False

    result = SafeResult(value=123)
    assert result.value == 123
    assert result.error is None
    assert result.has_error is False

    result = SafeResult(error=Exception("Something went wrong"))
    assert result.value is None
    assert result.error is not None
    assert result.has_error is True
    assert isinstance(result.error, Exception)
    assert str(result.error) == "Something went wrong"
