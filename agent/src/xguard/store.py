"""Local SQLite store: findings, baselines and an audit log of every action."""

from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from .models import Action, Finding

SCHEMA = """
CREATE TABLE IF NOT EXISTS findings (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    fingerprint  TEXT UNIQUE NOT NULL,
    monitor      TEXT NOT NULL,
    key          TEXT NOT NULL,
    severity     TEXT NOT NULL,
    title        TEXT NOT NULL,
    detail       TEXT NOT NULL,
    evidence     TEXT NOT NULL,
    actions      TEXT NOT NULL,
    status       TEXT NOT NULL DEFAULT 'open',   -- open | resolved | dismissed | acted
    triage       TEXT,                            -- JSON from the triage step, if any
    first_seen   REAL NOT NULL,
    last_seen    REAL NOT NULL,
    notified     INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS audit (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    at          REAL NOT NULL,
    finding_id  INTEGER,
    event       TEXT NOT NULL,
    data        TEXT NOT NULL
);
"""


@dataclass
class StoredFinding:
    id: int
    fingerprint: str
    monitor: str
    key: str
    severity: str
    title: str
    detail: str
    evidence: dict[str, Any]
    actions: list[Action]
    status: str
    triage: dict[str, Any] | None
    first_seen: float
    last_seen: float
    notified: bool

    def action(self, action_id: str) -> Action | None:
        return next((a for a in self.actions if a.id == action_id), None)


def _actions_to_json(actions: tuple[Action, ...] | list[Action]) -> str:
    return json.dumps([a.__dict__ for a in actions])


def _actions_from_json(raw: str) -> list[Action]:
    return [Action(**a) for a in json.loads(raw)]


class Store:
    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    # ---- state (baselines) -------------------------------------------------
    def get_state(self, key: str, default: Any = None) -> Any:
        row = self.db.execute("SELECT value FROM state WHERE key = ?", (key,)).fetchone()
        return json.loads(row["value"]) if row else default

    def set_state(self, key: str, value: Any) -> None:
        self.db.execute(
            "INSERT INTO state(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, json.dumps(value)),
        )
        self.db.commit()

    # ---- findings ----------------------------------------------------------
    def upsert(self, f: Finding, now: float | None = None) -> tuple[StoredFinding, bool]:
        """Insert a new finding or refresh a known one. Returns (finding, is_new).

        A finding the user dismissed stays dismissed. A resolved finding that
        comes back is reopened and counts as new.
        """
        now = now or time.time()
        row = self.db.execute("SELECT * FROM findings WHERE fingerprint = ?", (f.fingerprint,)).fetchone()
        if row is None:
            cur = self.db.execute(
                "INSERT INTO findings(fingerprint, monitor, key, severity, title, detail, evidence, actions,"
                " first_seen, last_seen) VALUES(?,?,?,?,?,?,?,?,?,?)",
                (f.fingerprint, f.monitor, f.key, f.severity, f.title, f.detail,
                 json.dumps(f.evidence, sort_keys=True), _actions_to_json(f.actions), now, now),
            )
            self.db.commit()
            self.log(cur.lastrowid, "detected", {"severity": f.severity, "title": f.title})
            return self.get(cur.lastrowid), True  # type: ignore[arg-type]

        reopened = row["status"] in ("resolved", "acted")
        status = "open" if reopened else row["status"]
        self.db.execute(
            "UPDATE findings SET severity=?, detail=?, evidence=?, actions=?, last_seen=?, status=?,"
            " notified = CASE WHEN ? THEN 0 ELSE notified END WHERE id=?",
            (f.severity, f.detail, json.dumps(f.evidence, sort_keys=True), _actions_to_json(f.actions),
             now, status, int(reopened), row["id"]),
        )
        self.db.commit()
        if reopened:
            self.log(row["id"], "reopened", {})
        return self.get(row["id"]), reopened  # type: ignore[arg-type]

    def resolve_missing(self, monitor: str, seen: set[str]) -> list[int]:
        """Open findings of `monitor` that were not seen this scan are resolved."""
        rows = self.db.execute(
            "SELECT id, fingerprint FROM findings WHERE monitor = ? AND status = 'open'", (monitor,)
        ).fetchall()
        gone = [r["id"] for r in rows if r["fingerprint"] not in seen]
        for fid in gone:
            self.set_status(fid, "resolved", event="resolved")
        return gone

    def get(self, fid: int) -> StoredFinding | None:
        row = self.db.execute("SELECT * FROM findings WHERE id = ?", (fid,)).fetchone()
        return self._row(row) if row else None

    def list(self, statuses: tuple[str, ...] = ("open",)) -> list[StoredFinding]:
        marks = ",".join("?" * len(statuses))
        rows = self.db.execute(
            f"SELECT * FROM findings WHERE status IN ({marks}) ORDER BY last_seen DESC", statuses
        ).fetchall()
        return [self._row(r) for r in rows]

    def set_status(self, fid: int, status: str, event: str, data: dict[str, Any] | None = None) -> None:
        self.db.execute("UPDATE findings SET status = ? WHERE id = ?", (status, fid))
        self.db.commit()
        self.log(fid, event, data or {})

    def set_triage(self, fid: int, triage: dict[str, Any]) -> None:
        self.db.execute("UPDATE findings SET triage = ? WHERE id = ?", (json.dumps(triage), fid))
        self.db.commit()

    def mark_notified(self, fid: int) -> None:
        self.db.execute("UPDATE findings SET notified = 1 WHERE id = ?", (fid,))
        self.db.commit()

    # ---- audit -------------------------------------------------------------
    def log(self, fid: int | None, event: str, data: dict[str, Any]) -> None:
        self.db.execute(
            "INSERT INTO audit(at, finding_id, event, data) VALUES(?,?,?,?)",
            (time.time(), fid, event, json.dumps(data)),
        )
        self.db.commit()

    def audit(self, fid: int | None = None) -> Iterator[sqlite3.Row]:
        if fid is None:
            yield from self.db.execute("SELECT * FROM audit ORDER BY id")
        else:
            yield from self.db.execute("SELECT * FROM audit WHERE finding_id = ? ORDER BY id", (fid,))

    @staticmethod
    def _row(r: sqlite3.Row) -> StoredFinding:
        return StoredFinding(
            id=r["id"], fingerprint=r["fingerprint"], monitor=r["monitor"], key=r["key"],
            severity=r["severity"], title=r["title"], detail=r["detail"],
            evidence=json.loads(r["evidence"]), actions=_actions_from_json(r["actions"]),
            status=r["status"], triage=json.loads(r["triage"]) if r["triage"] else None,
            first_seen=r["first_seen"], last_seen=r["last_seen"], notified=bool(r["notified"]),
        )
