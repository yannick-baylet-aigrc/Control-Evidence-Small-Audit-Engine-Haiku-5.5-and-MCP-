# --------------------------------------------------------------------------------------------
# AI generated ("vibe-coding" - HITL control) script
# --------------------------------------------------------------------------------------------

import os
import json
import sys
from pathlib import Path
from typing import List, Literal
from pydantic import BaseModel, Field
import anthropic

# Model configuration with fallback default
MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-haiku-5-5")

# ------------------------------------------------------------------------------
# Security & Key Management Control 
# ------------------------------------------------------------------------------

def get_anthropic_api_key() -> str:
    """
    Retrieves the Anthropic API key from:
    1. Environment variable 'ANTHROPIC_API_KEY' (if set in session)
    2. Fallback: External secure file path outside the Git working tree
    """
    key = os.getenv("ANTHROPIC_API_KEY")
    if key and key.strip():
        return key.strip()

    # External boundary path on Windows 11
    external_key_path = Path(r"D:\DATA\ProjetsIA\APIs\Haiku55API.txt")
    if external_key_path.exists():
        key_content = external_key_path.read_text(encoding="utf-8").strip()
        if key_content:
            return key_content

    raise RuntimeError(
        "API Key Error: ANTHROPIC_API_KEY environment variable is missing and "
        f"no valid key was found at '{external_key_path}'."
    )

# ---------------------------------------------------------------------------
# Output Schema Definition
# ---------------------------------------------------------------------------
class AuditReport(BaseModel):
    control_id: str = Field(description="Identifier for the control being audited (e.g. ISO-42001-A.8.2)")
    compliance_status: Literal["COMPLIANT", "NON_COMPLIANT", "INSUFFICIENT_EVIDENCE"]
    findings_summary: str = Field(description="2-3 sentence summary of the audit finding")
    evidence_gaps: List[str] = Field(description="List of missing evidence items or compliance gaps")
    recommendations: List[str] = Field(description="Actionable remediation steps")

# ---------------------------------------------------------------------------
# Core Evaluation Function
# ---------------------------------------------------------------------------
def audit_control_evidence(control_text: str, evidence_text: str) -> dict:
    """
    Evaluates operational evidence against a control requirement using 
    Claude Tool Use for structured output.
    """
    api_key = get_anthropic_api_key()
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are an expert IT GRC and AI Governance auditor evaluating evidence against compliance controls "
        "(e.g., ISO 27001, ISO 42001, NIST AI RMF, EU AI Act).\n"
        "Analyze the provided control requirement and evidence artifact objectively.\n"
        "You MUST invoke the 'submit_audit_report' tool to return your structured evaluation."
    )

    user_prompt = f"""
    === CONTROL REQUIREMENT ===
    {control_text}

    === EVIDENCE ARTIFACT ===
    {evidence_text}

    Evaluate whether the evidence satisfies the control requirement.
    """

    tool_definition = {
        "name": "submit_audit_report",
        "description": "Submits the structured audit report after evaluating control evidence.",
        "input_schema": {
            "type": "object",
            "properties": {
                "control_id": {"type": "string", "description": "Control identifier (e.g., ISO-42001-A.8.2)"},
                "compliance_status": {
                    "type": "string",
                    "enum": ["COMPLIANT", "NON_COMPLIANT", "INSUFFICIENT_EVIDENCE"],
                    "description": "Overall audit determination"
                },
                "findings_summary": {"type": "string", "description": "Concise summary of audit findings"},
                "evidence_gaps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Identified gaps or missing elements"
                },
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Remediation recommendations"
                }
            },
            "required": ["control_id", "compliance_status", "findings_summary", "evidence_gaps", "recommendations"]
        }
    }

    response = client.messages.create(
        model=MODEL_NAME,  # Using the global MODEL_NAME variable
        max_tokens=1024,
        system=system_prompt,
        tools=[tool_definition],
        tool_choice={"type": "tool", "name": "submit_audit_report"},
        messages=[{"role": "user", "content": user_prompt}]
    )

    for content in response.content:
        if content.type == "tool_use" and content.name == "submit_audit_report":
            return content.input

    raise ValueError("Claude failed to return a structured tool invocation.")

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main():
    base_dir = Path(__file__).parent
    control_file = base_dir / "samples" / "control_sample.txt"
    evidence_file = base_dir / "samples" / "evidence_sample.txt"

    if not control_file.exists() or not evidence_file.exists():
        print(f"[ERROR] Missing sample files in '{base_dir / 'samples'}'.")
        print("Please create 'control_sample.txt' and 'evidence_sample.txt'.")
        sys.exit(1)

    control_text = control_file.read_text(encoding="utf-8")
    evidence_text = evidence_file.read_text(encoding="utf-8")

    print(f"Executing Compliance Audit via Claude API ({MODEL_NAME})...")
    print(f"Project Directory: {base_dir}\n")

    try:
        report = audit_control_evidence(control_text, evidence_text)
        print("--- AUDIT REPORT OUTPUT (JSON) ---")
        print(json.dumps(report, indent=2))
    except Exception as e:
        print(f"\n[EXECUTION ERROR]: {e}")

if __name__ == "__main__":
    main()