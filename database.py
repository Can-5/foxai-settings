"""Veritabanı katmanı: hesaplar, profiller ve ayarlar (SQLite)."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

DB_PATH = Path.home() / ".local" / "share" / "foxai-settings" / "settings.db"


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Tabloları oluşturur (idempotent)."""
    conn = _connect()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1
            );

            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                avatar_color TEXT NOT NULL DEFAULT '#409eff',
                is_default INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY(account_id) REFERENCES accounts(id)
            );

            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(profile_id, key),
                FOREIGN KEY(profile_id) REFERENCES profiles(id)
            );

            CREATE INDEX IF NOT EXISTS idx_settings_profile_key
                ON settings(profile_id, key);
            """
        )
        conn.commit()
    finally:
        conn.close()


def hash_password(password: str) -> str:
    import hashlib

    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_account(username: str, email: str, password: str) -> int:
    conn = _connect()
    try:
        cur = conn.execute(
            "INSERT INTO accounts (username, email, password_hash, created_at, is_active) "
            "VALUES (?, ?, ?, ?, 1)",
            (username, email, hash_password(password), datetime.utcnow().isoformat()),
        )
        account_id = cur.lastrowid
        # Varsayılan profil oluştur
        conn.execute(
            "INSERT INTO profiles (account_id, name, avatar_color, is_default, created_at) "
            "VALUES (?, ?, ?, 1, ?)",
            (account_id, "Bana Özel", "#409eff", datetime.utcnow().isoformat()),
        )
        conn.commit()
        return account_id
    finally:
        conn.close()


def verify_account(username: str, password: str) -> int | None:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT id, password_hash FROM accounts WHERE username = ? AND is_active = 1",
            (username,),
        ).fetchone()
        if row and row["password_hash"] == hash_password(password):
            return row["id"]
        return None
    finally:
        conn.close()


def account_exists(username: str, email: str) -> bool:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT 1 FROM accounts WHERE username = ? OR email = ?",
            (username, email),
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def get_profiles(account_id: int) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT * FROM profiles WHERE account_id = ? ORDER BY is_default DESC, name",
            (account_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_profile(account_id: int, name: str, avatar_color: str) -> int:
    conn = _connect()
    try:
        # Eski varsayılanı kaldır
        conn.execute(
            "UPDATE profiles SET is_default = 0 WHERE account_id = ?", (account_id,)
        )
        cur = conn.execute(
            "INSERT INTO profiles (account_id, name, avatar_color, is_default, created_at) "
            "VALUES (?, ?, ?, 1, ?)",
            (account_id, name, avatar_color, datetime.utcnow().isoformat()),
        )
        pid = cur.lastrowid
        conn.commit()
        return pid
    finally:
        conn.close()


def set_default_profile(profile_id: int) -> None:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT account_id FROM profiles WHERE id = ?", (profile_id,)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE profiles SET is_default = 0 WHERE account_id = ?",
                (row["account_id"],),
            )
            conn.execute(
                "UPDATE profiles SET is_default = 1 WHERE id = ?", (profile_id,)
            )
            conn.commit()
    finally:
        conn.close()


def delete_profile(profile_id: int) -> None:
    conn = _connect()
    try:
        conn.execute("DELETE FROM profiles WHERE id = ?", (profile_id,))
        conn.commit()
    finally:
        conn.close()


def get_setting(profile_id: int, key: str, default: Any = None) -> Any:
    conn = _connect()
    try:
        row = conn.execute(
            "SELECT value FROM settings WHERE profile_id = ? AND key = ?",
            (profile_id, key),
        ).fetchone()
        if row is None:
            return default
        try:
            return json.loads(row["value"])
        except (json.JSONDecodeError, TypeError):
            return row["value"]
    finally:
        conn.close()


def set_setting(profile_id: int, key: str, value: Any) -> None:
    conn = _connect()
    try:
        payload = json.dumps(value, ensure_ascii=False)
        now = datetime.utcnow().isoformat()
        conn.execute(
            "INSERT INTO settings (profile_id, key, value, updated_at) "
            "VALUES (?, ?, ?, ?) "
            "ON CONFLICT(profile_id, key) DO UPDATE SET value = excluded.value, updated_at = excluded.updated_at",
            (profile_id, key, payload, now),
        )
        conn.commit()
    finally:
        conn.close()


def load_all_settings(profile_id: int) -> dict[str, Any]:
    conn = _connect()
    try:
        rows = conn.execute(
            "SELECT key, value FROM settings WHERE profile_id = ?", (profile_id,)
        ).fetchall()
        out: dict[str, Any] = {}
        for r in rows:
            try:
                out[r["key"]] = json.loads(r["value"])
            except (json.JSONDecodeError, TypeError):
                out[r["key"]] = r["value"]
        return out
    finally:
        conn.close()
