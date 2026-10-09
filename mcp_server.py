# -------------------------------------------------------------------------------
# AI generated script (Claude code - HITL control)
# -------------------------------------------------------------------------------


import os
from fastmcp import FastMCP
from auditor import audit_control_evidence, get_anthropic_api_key

# ---------------------------------------------------------------------------
# FastMCP Server Initialization
# ---------------------------------------------------------------------------
mcp = FastMCP("Compliance & AI Governance Auditor")

# Local Control Framework Library
CONTROL_LIBRARY = {
    "ISO-42001-A.8.2": "AI System Risk Treatment: The organization shall perform automated security scanning, prompt-injection vulnerability analysis, and mandatory peer code review for production AI pipeline components.",
    "ISO-27001-A.8.25": "Secure Development Lifecycle: All code changes must undergo automated vulnerability scanning and documented peer review prior to deployment to production."
}

# Ensure API key accessibility on server boot
try:
    _key = get_anthropic_api_key()
    os.environ["ANTHROPIC_API_KEY"] = _key
except Exception as err:
    print(f"[MCP SERVER WARNING] Failed to resolve API Key on startup: {err}")

# ---------------------------------------------------------------------------
# 1. MCP RESOURCE: Expose Framework Controls to Claude Desktop / Code
# ---------------------------------------------------------------------------
@mcp.resource("compliance://controls/{control_id}")
def get_control_definition(control_id: str) -> str:
    """
    Retrieves standard control requirement definitions by Control ID 
    (e.g., ISO-42001-A.8.2 or ISO-27001-A.8.25).
    """
    return CONTROL_LIBRARY.get(
        control_id,
        f"Control ID '{control_id}' not found in standard compliance library."
    )

# ---------------------------------------------------------------------------
# 2. MCP TOOL: Expose Compliance Audit Engine
# ---------------------------------------------------------------------------
@mcp.tool()
def evaluate_compliance_evidence(control_text: str, evidence_text: str) -> dict:
    """
    Evaluates operational evidence (logs, PRs, CI/CD output) against a formal control requirement.
    Returns a structured audit report containing compliance status, gaps, and recommendations.
    """
    return audit_control_evidence(control_text, evidence_text)

# ---------------------------------------------------------------------------
# Execution Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()