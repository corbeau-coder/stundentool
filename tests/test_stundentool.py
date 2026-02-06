import pytest


from src.stundentool import main, graduation_checker


def test_graduation_checker():
    with pytest.raises(TypeError):
        assert graduation_checker(1)
        assert graduation_checker("a")
        assert graduation_checker()

    with pytest.raises(ValueError):
        assert graduation_checker(42.7)

    assert graduation_checker(42.0) == None
    assert graduation_checker(42.25) == None
    assert graduation_checker(0) == None
    assert graduation_checker(42.5) == None
    assert graduation_checker(42.75) == None
    assert graduation_checker(-1.75) == None
    assert graduation_checker(-0.75) == None


"""def test_main():
    with unittest.mock.patch("sys.argv","['42']"):
        main()"""
