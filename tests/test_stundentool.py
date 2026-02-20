import pytest

from unittest.mock import Mock, patch

from src.modules.data.store_handler import store_handler

from src.stundentool import graduation_checker, purge, main


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

def fake_exit(code):
    raise SystemExit(code)

def test_purge(monkeypatch):
    storage = store_handler("test.db")
    with patch("os.path.isfile") as mock_isfile, patch("os.remove") as mock_remove:
        mock_isfile.return_value = True
        mock_remove.side_effect = FileNotFoundError
        monkeypatch.setattr("builtins.input", lambda _: "y")
        monkeypatch.setattr("sys.exit", fake_exit)
        with patch("src.stundentool.logger") as logger_mock:
            with pytest.raises(SystemExit) as exc, pytest.raises(FileNotFoundError) as fexc:
                purge(storage, "test.db")
            assert exc.value.code == 0                 # Korrektes Beenden
            #storage.purge.assert_called_once_with("test.db") # Wurde einmal aufgerufen             
            logger_mock.info.assert_any_call(
                "Purging requested, starting routine deleting db"
            )
            logger_mock.info.assert_any_call(
                "done. Please use --init [hours.minutes] to re-initiate the program"
            )

def test_main_routing(monkeypatch):
    monkeypatch.setattr("sys", "argv", ["--init 42"])
    monkeypatch.setattr("sys.exit", fake_exit)
    main.storage = Mock




"""def test_main_purge():
    with unittest.mock.patch("sys.argv","['--purge']"):
        main()"""

""" os.remove(path, *, dir_fd=None)

    Remove (delete) the file path. If path is a directory, an OSError is raised. Use rmdir() to remove directories. If the file does not exist, a FileNotFoundError is raised.
"""