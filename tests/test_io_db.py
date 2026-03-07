import pytest
import sqlite3

from unittest.mock import patch

#from src.modules.sqlite.IO_db import db_object
from src.stundentool import main


def test_init_db(tmp_path, monkeypatch):
    path = tmp_path / "test.db"
    with (patch("src.stundentool.logger") as logger_mock,):
        monkeypatch.setattr("sys.argv", ["stundentool.py","--init", "1337.0"])
        with pytest.raises(SystemExit) as exc:
            main(path)

        assert exc.value.code == 0
        logger_mock.info.assert_any_call("Initating database ...")
        logger_mock.info.assert_any_call(" done")
        

        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            sql_tests = [
                "SELECT * FROM HEADER", # check colums header
                "SELECT * FROM HEADER", # check initial input header
                "SELECT * FROM BODY", #check columns
            ]
            asserts = [
                "1337.0",
                "1337.0",
                None
            ]
            for item, exp_res in sql_tests, asserts:
                resp = cur.execute(item).fetchone()
                print(f"SQL-String {item} response {resp}\n")
                assert resp == exp_res

    return