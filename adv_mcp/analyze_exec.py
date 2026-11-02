"""Summarise a claude-code-action execution file into GitHub step-summary markdown.

Usage: python3 adv_mcp/analyze_exec.py <execution_file> [label]
Prints: MCP servers + status, MCP tool names, plugins, slash commands,
tool_use calls (name + short input), permission denials, cost, final result.
"""
import json
import sys


def load(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read().strip()
    try:
        data = json.loads(text)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def main():
    path = sys.argv[1]
    label = sys.argv[2] if len(sys.argv) > 2 else ""
    msgs = load(path)
    out = [f"## Execution analysis {label}".rstrip()]
    init = next((m for m in msgs if m.get("type") == "system" and m.get("subtype") == "init"), {})
    out.append("### MCP servers")
    for s in init.get("mcp_servers", []) or ["(none)"]:
        out.append(f"- {s.get('name')}: {s.get('status')}" if isinstance(s, dict) else f"- {s}")
    mcp_tools = [t for t in init.get("tools", []) if str(t).startswith("mcp__")]
    out.append(f"### MCP tools ({len(mcp_tools)})")
    out.append(", ".join(mcp_tools) or "(none)")
    out.append("### Plugins")
    for p in init.get("plugins", []) or ["(none)"]:
        out.append(f"- {p.get('name')} ({p.get('path','')})" if isinstance(p, dict) else f"- {p}")
    cmds = init.get("slash_commands", [])
    out.append(f"### Slash commands ({len(cmds)})")
    out.append(", ".join(cmds) or "(none)")
    agents = init.get("agents", [])
    if agents:
        out.append(f"### Agents: {', '.join(map(str, agents))}")
    skills = init.get("skills", [])
    if skills:
        out.append(f"### Skills: {', '.join(map(str, skills))}")
    out.append("### tool_use calls")
    n = 0
    for m in msgs:
        if m.get("type") != "assistant":
            continue
        sub = " (subagent)" if m.get("parent_tool_use_id") else ""
        for c in (m.get("message", {}) or {}).get("content", []) or []:
            if isinstance(c, dict) and c.get("type") == "tool_use":
                n += 1
                inp = json.dumps(c.get("input", {}), ensure_ascii=False)[:160]
                out.append(f"- `{c.get('name')}`{sub} {inp}")
    if n == 0:
        out.append("(none)")
    res = next((m for m in reversed(msgs) if m.get("type") == "result"), {})
    den = res.get("permission_denials") or []
    out.append(f"### Permission denials ({len(den)})")
    for d in den:
        out.append(f"- `{d.get('tool_name')}` {json.dumps(d.get('tool_input', {}), ensure_ascii=False)[:160]}")
    out.append("### Result")
    out.append(f"- subtype: {res.get('subtype')}, is_error: {res.get('is_error')}, num_turns: {res.get('num_turns')}")
    out.append(f"- total_cost_usd: {res.get('total_cost_usd')}")
    out.append("")
    out.append(str(res.get("result", ""))[:3000])
    print("\n".join(out))


if __name__ == "__main__":
    main()
