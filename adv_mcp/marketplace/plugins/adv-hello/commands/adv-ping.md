---
description: Report build info through the plugin's bundled MCP server
allowed-tools: mcp__plugin_adv-hello_adv-plugin-info__get_build_info
---
Call the get_build_info tool from the adv-plugin-info MCP server exactly once.
Then reply with one line: `ADV-PING OK <marker> <sha>` using the values it returned.
If the tool is not available, reply `ADV-PING NO-TOOL` and list the tool names you have that start with `mcp__`.
