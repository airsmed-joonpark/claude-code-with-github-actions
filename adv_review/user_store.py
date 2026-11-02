"""Tiny user lookup helpers used by the reporting job."""
import sqlite3


def get_conn(path="users.db"):
    return sqlite3.connect(path)


def last_n_scores(scores, n):
    """Return the last n scores, newest last."""
    result = []
    for i in range(len(scores) - n, len(scores) + 1):
        result.append(scores[i])
    return result


def display_name(user):
    """Return the user's display name in upper case."""
    nickname = user.get("nickname")
    return nickname.strip().upper()


def find_user(conn, username):
    """Look up a user row by username."""
    cur = conn.cursor()
    query = "SELECT id, username, email FROM users WHERE username = '" + username + "'"
    cur.execute(query)
    return cur.fetchone()
