"""Summarize a Claude Code execution file as GitHub step-summary markdown.

Usage: python3 summarize.py <execution_file> [label]

Reads the stream of messages the CLI writes (a JSON array, JSON lines, or a single
result object from `claude -p --output-format json`) and prints: model(s) actually
used, turns, cost, stop reason, MCP servers, tools Claude called, and permission denials.
"""
import json
import sys
from collections import Counter


def load(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    if not text:
        return []
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def main():
    path = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else "claude"
    msgs = load(path)
    init = next((m for m in msgs if m.get("type") == "system" and m.get("subtype") == "init"), {})
    res = next((m for m in reversed(msgs) if m.get("type") == "result"), {})

    calls = Counter()
    for m in msgs:
        if m.get("type") != "assistant":
            continue
        for c in (m.get("message") or {}).get("content") or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                name = c.get("name", "?")
                if name in ("Skill", "Agent", "Task"):
                    inp = c.get("input") or {}
                    name = f"{name}:{inp.get('skill') or inp.get('subagent_type') or ''}"
                calls[name] += 1

    # modelUsage lists the models that really answered. init.model only echoes the request,
    # and a typo'd --model silently falls back when --fallback-model is set.
    models = ", ".join(sorted((res.get("modelUsage") or {}).keys())) or init.get("model", "?")
    cost = res.get("total_cost_usd")
    denials = res.get("permission_denials") or []
    stop = res.get("subtype", "?")
    flag = "" if stop == "success" and not res.get("is_error") else " ⚠️"

    out = [f"### Claude run report: {label}", ""]
    out.append("| item | value |")
    out.append("|---|---|")
    out.append(f"| stop reason | `{stop}`{flag} |")
    out.append(f"| models used | {models} |")
    out.append(f"| turns | {res.get('num_turns', '?')} |")
    out.append(f"| cost (USD) | {cost if cost is not None else '?'} |")
    dur = res.get("duration_ms")
    out.append(f"| duration | {round(dur / 1000, 1) if dur else '?'} s |")
    servers = init.get("mcp_servers") or []
    if servers:
        out.append("| MCP servers | " + ", ".join(f"{s.get('name')}={s.get('status')}" for s in servers if isinstance(s, dict)) + " |")
    out.append(f"| permission denials | {len(denials)} |")
    out.append("")
    out.append("**Tools called**: " + (", ".join(f"`{k}`×{v}" for k, v in calls.most_common()) or "none"))
    if denials:
        out.append("")
        out.append("**Denied**:")
        for d in denials[:10]:
            inp = json.dumps(d.get("tool_input", {}), ensure_ascii=False)[:150]
            out.append(f"- `{d.get('tool_name')}` {inp}")
    if stop in ("error_max_turns", "error_max_budget_usd"):
        out.append("")
        out.append(f"> Stopped by a cost guard ({stop}). Raise --max-turns / --max-budget-usd if this task needs more.")
    out.append("")
    print("\n".join(out))


if __name__ == "__main__":
    main()
