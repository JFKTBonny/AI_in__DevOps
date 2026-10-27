# AI Agents for DevOps: CI Failure Triage

This practical example is a read-only AI agent that investigates a local CI
log. The Groq model can choose between two limited tools—summarize the job or
search the log for a term—then use the results to prepare an evidence-based
triage report.

The agent can inspect logs only. It does not access GitHub, execute shell
commands, edit files, retry builds, or deploy changes.

## Files

- `ci_triage_agent.py` — agent loop and read-only log tools.
- `sample_ci.txt` — synthetic failed CI job for trying the example.
- `notes.txt` — agent concepts, workflow, and safety details.

## Requirements

- Python 3.9 or newer; no third-party Python packages are required.
- A Groq API key and internet access.

Set your API key in the environment:

```bash
export GROQ_API_KEY="your-api-key"
```

Run the sample:

```bash
python3 ci_triage_agent.py
```

Or provide a local log file:

```bash
python3 ci_triage_agent.py path/to/ci.log
```

The default model is `llama-3.3-70b-versatile`. To choose another model
available to your Groq account:

```bash
export GROQ_MODEL="your-available-model"
```

The selected log content is sent to the Groq API. Do not submit secrets,
customer data, or confidential build output unless your organization's policy
permits it. Treat the report as a hypothesis: verify it against the CI job
and source code before acting.
