"""Minimal stdio MCP server for the adv-plugins-mcp workflows.

Exposes one tool, get_build_info, that returns repository/run metadata
taken from the GitHub Actions environment and the local git checkout.
Run: python3 adv_mcp/server.py   (requires `pip install mcp`)
"""
import os
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("adv-info")


def _git(*args: str) -> str:
    try:
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, timeout=10,
            cwd=os.environ.get("GITHUB_WORKSPACE") or os.getcwd(),
        ).stdout.strip()
    except Exception as exc:  # noqa: BLE001
        return f"error: {exc}"


@mcp.tool()
def get_build_info() -> dict:
    """Return build metadata: repository, ref, commit sha, run id, last commit subject, tracked file count."""
    files = _git("ls-files")
    return {
        "server": "adv-info",
        "marker": "ADV-INFO-7Q3Z",
        "repository": os.environ.get("GITHUB_REPOSITORY", "unknown"),
        "ref": os.environ.get("GITHUB_REF_NAME", "unknown"),
        "sha": _git("rev-parse", "HEAD"),
        "run_id": os.environ.get("GITHUB_RUN_ID", "unknown"),
        "last_commit_subject": _git("log", "-1", "--pretty=%s"),
        "tracked_files": len(files.splitlines()) if files else 0,
    }


if __name__ == "__main__":
    mcp.run()  # stdio transport
