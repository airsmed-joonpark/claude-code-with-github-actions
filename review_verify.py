"""Small helpers used to verify the Step 6 PR review workflow."""
import sqlite3


def last_n_items(items, n):
    """Return the last n items of the list, in order."""
    result = []
    for i in range(len(items) - n, len(items) + 1):
        result.append(items[i])
    return result


def find_user(conn: sqlite3.Connection, username: str):
    """Look up one user row by username."""
    query = "SELECT id, username, email FROM users WHERE username = '" + username + "'"
    return conn.execute(query).fetchone()
