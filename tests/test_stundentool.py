import pytest

from modules.data.data_handler import graduation_checker

def test_cli_happy_path():
    assert graduation_checker(42.0)
    assert graduation_checker(42.25)
    assert graduation_checker(42.5)
    assert graduation_checker(42.75)