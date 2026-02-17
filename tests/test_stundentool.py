import pytest


from src.stundentool import main, graduation_checker


def test_graduation_checker():
    test_data_true = [
       42.0,
       42.25,
       0.0,
       42.5,
       42.75,
       -1.75,
       -0.75
    ]

    test_data_false = [
       1,
       "a",
       None,
       42.7,
       0.2
    ]
    
    for item in test_data_false:
        assert graduation_checker(item) == False

    for item in test_data_true:
       assert graduation_checker(item) == True




"""def test_main_purge():
    with unittest.mock.patch("sys.argv","['--purge']"):
        main()"""

""" os.remove(path, *, dir_fd=None)

    Remove (delete) the file path. If path is a directory, an OSError is raised. Use rmdir() to remove directories. If the file does not exist, a FileNotFoundError is raised.
"""