# pylint> disable=line-too-long
"""
This function tests the behavior of assigning a dictionary
to a variable and then comparing it to another dictionary with the same content.

**Raises:**

- AssertionError: If the actual and expected results are not equal.
"""


def test_main():
    """
    Tests assigning a dictionary to a variable and comparing it to another dictionary .
    """

    result = {"key": 10}
    actual_result = result

    expected_result = {"key": 10}
    assert actual_result == expected_result, f"Expected {expected_result}, got {actual_result}"
