import pytest
import sqlite3
import itertools

from unittest.mock import patch

from src.stundentool import main
from src.modules.sqlite import db



@pytest.mark.parametrize("sql_query, response_first_column",
                         [
                             ("SELECT * FROM HEADER", ["value"]),
                             ("SELECT * FROM BODY", ["date", "hours"])
                         ]
                         )
def test_init_db(tmp_path, monkeypatch, sql_query, response_first_column):
    path = tmp_path / "test.db"
    with (patch("src.modules.sqlite.db.logger") as logger_mock):
        monkeypatch.setattr("sys.argv", ["stundentool.py","--init", "1337.0"])
        with pytest.raises(SystemExit) as exc:
            main(path)

        assert exc.value.code == 0
        logger_mock.info.assert_any_call("Initating database ...")
        logger_mock.info.assert_any_call(" done.")
        

        with sqlite3.connect(path) as conn:
            cur = conn.cursor()
            resp = cur.execute(sql_query)                
            for index, col in enumerate(response_first_column):
                assert resp.description[index][0] == col


    return