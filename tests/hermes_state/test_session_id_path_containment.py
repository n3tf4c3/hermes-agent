"""A session id is a file name under the sessions dir, so it must not leave that dir.

``import_sessions`` accepted any non-empty id, and delete/prune swept ``sessions_dir / f"{id}.json"``
(and ``.jsonl``) with no containment check: an imported ``../x`` made a later delete remove ``x.json``
beside the sessions dir. Import now refuses such ids, and the sweep leaves files alone for one already
stored.
"""

from __future__ import annotations

import pytest

from hermes_state import SessionDB


@pytest.fixture()
def db(tmp_path):
    d = SessionDB(db_path=tmp_path / "state.db")
    yield d
    d.close()


def _payload(session_id: str) -> dict:
    return {"id": session_id, "messages": [{"role": "user", "content": "hello"}]}


@pytest.mark.parametrize("session_id", ["../outside", "..\\outside", "nested/inner", "/abs/olute", "C:outside", "a\x00b"])
def test_import_refuses_an_id_that_is_not_a_plain_file_name(db, session_id):
    result = db.import_sessions([_payload(session_id)])

    assert result["ok"] is False and result["imported"] == 0, result
    assert "plain name" in result["errors"][0]["error"]
    assert db.get_session(session_id) is None


def test_import_keeps_accepting_ordinary_ids(db):
    ids = ["20261107_120000_abc123", "cron_job-1.daily_20261107_120000", "api-0123456789abcdef", "my session"]

    result = db.import_sessions([_payload(sid) for sid in ids])

    assert result["ok"] is True and result["imported"] == len(ids), result


def test_deleting_a_stored_traversal_id_leaves_files_outside_the_sessions_dir(db, tmp_path):
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("{}", encoding="utf-8")
    # A row stored before the import check existed.
    db.create_session("../outside", source="import")

    assert db.delete_session("../outside", sessions_dir=sessions_dir) is True

    assert db.get_session("../outside") is None
    assert outside.exists(), "the sweep followed the id out of the sessions dir"


def test_deleting_an_ordinary_session_still_removes_its_files(db, tmp_path):
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    sid = "20261107_120000_abc123"
    for name in (f"{sid}.json", f"{sid}.jsonl"):
        (sessions_dir / name).write_text("{}", encoding="utf-8")
    db.create_session(sid, source="cli")

    assert db.delete_session(sid, sessions_dir=sessions_dir) is True

    assert not any(sessions_dir.iterdir())
