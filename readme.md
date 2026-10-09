\# Automated Control-Evidence-Small-Auditor-Haiku-5.5-and-MCP-

Control \&amp; Evidence Small Audit Engine using Claude Haiku 5.5 and MCP framework

A Python tool utilizing the \*\*Claude API (Tool Use / Function Calling)\*\* to evaluate compliance evidence against control requirements, across security and AI governance frameworks (ISO 27001, ISO 42001, EU AI Act, NIST AI RMF).



\## main overview

Manual evidence validation in internal audits is time-consuming and exposed to human error. This project shows how Claude can be integrated into GRC automation processes to:

1\. Compare raw operational evidence (logs, PR reviews, policy docs) against formal control specifications.

2\. Determine compliance status (`COMPLIANT`, `NON\_COMPLIANT`, `INSUFFICIENT\_EVIDENCE`).

3\. Extract specific evidence gaps and generate remediation steps guide.

4\. Output deterministic, schema-compliant JSON via Anthropic Tool Use.



\## Features

\- \*\*Schema Enforcement:\*\* Uses Claude's tool-use parameter to guarantee strict JSON output without relying on un-reliable string parsing or regex.

\- \*\*Multi Frameworks Compliant:\*\* Works with ISO 27001, ISO 42001, NIST AI RMF, SOC 2, or custom internal controls.

\- \*\*Audit Traceability:\*\* Generates standardized gap analysis and remediation reports, ready for GRC platform use (e.g., Jira, ServiceNow, or Vanta).



\## Setup \& Usage

1\. clone the repository and set up a virtual environment:

&#x20;  ```bash

&#x20;  git clone \ [https://github.com/MY\_USERNAME/claude-compliance-auditor.git](https://github.com/YOUR\_USERNAME/claude-compliance-auditor.git)

&#x20;  cd claude-compliance-auditor

&#x20;  python3 -m venv venv

&#x20;  source venv/bin/activate

&#x20;  pip install -r requirements.txt

&#x20;  ```



2\. export my API key:

&#x20;  ```bash

&#x20;  export ANTHROPIC\_API\_KEY="your-api-key"

&#x20;  ```



3\. run the auditor:

&#x20;  ```bash

&#x20;  python auditor.py

&#x20;  ```



\## Why This Project Matters for Controls Engineering:

At scale, controls specialists need to automate the verification of continuous evidence streams. This project tries to illustrate practical Claude AI control for compliance workflows: treating LLMs not just as chatbots, but as structured, deterministic evaluation engines within security pipelines.



