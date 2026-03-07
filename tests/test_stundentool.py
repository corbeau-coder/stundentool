import pytest

from unittest.mock import Mock, patch

from src.modules.data.store_handler import store_handler

from src.stundentool import graduation_checker, purge, main

@pytest.mark.parametrize(
    "a,exp_return",         
    [
        (42.0, True),
        (42.25, True),
        (0.0, True),
        (42.5, True),
        (42.75, True),
        (-1.75, True),
        (-0.75, True),
        (1, False),
        ("a", False),
        (None, False),
        (42.7, False),
        (0.2, False),
    ]
)
def test_graduation_checker(a, exp_return):
    assert graduation_checker(a) == exp_return


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
            with (
                pytest.raises(SystemExit) as exc,
                pytest.raises(FileNotFoundError) as fexc,
                #TODO filenotfound testing
            ):
                purge(storage, "test.db")
            assert exc.value.code == 0
            logger_mock.info.assert_any_call(
                "Purging requested, starting routine deleting db"
            )
            logger_mock.info.assert_any_call(
                "done. Please use --init [hours.minutes] to re-initiate the program"
            )

@pytest.mark.parametrize(
    "args, exp_exit, exp_msg",
    [
        (["stundentool.py"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py","--add"], 1, "Error: empty hours.minutes argument, cannot add entry."),
        (["stundentool.py","--init", "--purge"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--init", "--status"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--purge", "--status"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--add", "--purge", "--status"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--add", "--init", "--status"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--add", "--init", "--purge"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
        (["stundentool.py", "--add", "--init", "--status", "--purge"], 1, "Error: check parameter set used - do not combine purge, init, status or add as parameters"),
    ]
)
def test_main_routing_parameterized(monkeypatch, args, exp_exit, exp_msg):
    monkeypatch.setattr("sys.exit", fake_exit)
    with (patch("src.stundentool.logger") as logger_mock,
          patch("src.stundentool.store_handler") as store_handler_mock):
        monkeypatch.setattr("sys.argv", args)
        storage_mock = Mock()
        storage_mock.db_status.return_value = True
        store_handler_mock.return_value = storage_mock

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")
        assert exc.value.code == exp_exit
        logger_mock.error.assert_any_call(exp_msg)
        

def test_main_routing(monkeypatch):
    monkeypatch.setattr("sys.exit", fake_exit)
     
    # routing 1, status
    with (
        patch("src.stundentool.logger") as logger_mock,
        patch("src.stundentool.store_handler") as store_handler_mock,
    ):
        monkeypatch.setattr("sys.argv", ["stundentool.py", "--verbose", "--status"])
        storage_mock = Mock()
        storage_mock.calc.return_value = (42, 13.75)
        store_handler_mock.return_value = storage_mock

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")

        assert exc.value.code == 0
        logger_mock.info.assert_any_call("TODO")
        logger_mock.debug.assert_any_call("Routing value is 1")

        monkeypatch.setattr("sys.argv", ["stundentool.py", "--status"])

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")

        assert exc.value.code == 0
        logger_mock.info.assert_any_call(
            "hours initial: 42\nhours reduced already: 13.75\n\nhours left: 28.25\n\nuse --verbose parameter additionally for more stats"
        )

    # routing 2, add
    with (
        patch("src.stundentool.logger") as logger_mock,
        patch("src.stundentool.store_handler") as store_handler_mock,
    ):
        monkeypatch.setattr("sys.argv", ["stundentool.py", "--verbose", "--add", "23.25"])
        storage_mock = Mock()
        store_handler_mock.return_value = storage_mock

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")

        assert exc.value.code == 0
        storage_mock.write_one.assert_called_once()
        logger_mock.debug.assert_any_call("Routing value is 2")

    # routing 4, init
    with (
        patch("src.stundentool.logger") as logger_mock,
        patch("src.stundentool.store_handler") as store_handler_mock,
    ):
        monkeypatch.setattr("sys.argv", ["stundentool.py", "--verbose", "--init", "42"])
        storage_mock = Mock()        
        store_handler_mock.return_value = storage_mock

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")

        assert exc.value.code == 0
        logger_mock.info.assert_any_call("Verbose logging configured")
        logger_mock.debug.assert_any_call("Routing value is 4")


    #routing 8, purge
    with (
        patch("src.stundentool.logger") as logger_mock,
        patch("src.stundentool.store_handler") as store_handler_mock,
    ):
        monkeypatch.setattr("sys.argv", ["stundentool.py", "--verbose", "--purge"])
        storage_mock = Mock()
        storage_mock.db_status = False
        storage_mock.purge.return_value = (True, "")
        store_handler_mock.return_value = storage_mock

        with pytest.raises(SystemExit) as exc:
            main("stundentool.db")

        assert exc.value.code == 0
        logger_mock.info.assert_any_call("Purging requested, starting routine deleting db")
        logger_mock.info.assert_any_call("done. Please use --init [hours.minutes] to re-initiate the program")
        logger_mock.debug.assert_any_call("Routing value is 8")
