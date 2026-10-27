# AIOps: Observability and Incident Response

This practical example simulates a cloud-native incident: after a deployment,
an API's latency and error rate increase, and logs show database timeouts. A
Python script sends the synthetic incident snapshot to Groq and asks an LLM
to summarize the evidence and suggest safe, read-only checks.

It demonstrates three connected ideas:

- **Observability provides evidence:** metrics, logs, and deployment events.
- **AIOps helps interpret it:** the model summarizes signals and highlights
  possible relationships.
- **Incident response uses verified evidence:** a human responder investigates
  and decides what to do.

The example uses fabricated data. It does not connect to Kubernetes or any
monitoring system, and it does not make production changes.

## Files

- `incident_snapshot.json` — synthetic metrics, logs, and deployment timeline.
- `triage_incident.py` — sends the snapshot to Groq and prints the response.

## Requirements

- Python 3.9 or newer; no additional Python packages are required.
- A Groq API key and internet access.

Set the API key as an environment variable:

```bash
export GROQ_API_KEY="your-api-key"
```

Optionally choose a model available to your Groq account:

```bash
export GROQ_MODEL="your-available-model"
```

Run from this directory:

```bash
python3 triage_incident.py
```

The script uses `incident_snapshot.json` by default. To analyze a different
JSON snapshot:

```bash
python3 triage_incident.py path/to/incident.json
```

## What to look for in the response

For the included scenario, compare the deployment time with the rise in
latency and errors. Check whether the database timeout logs support a
dependency-related hypothesis. The model should distinguish observed facts
from possible explanations and propose read-only follow-up checks.

Correlation is not proof of cause. Confirm the timeline in your monitoring
system, inspect traces and relevant service/dependency health, and follow your
team's incident process before deciding on mitigation.

## Safety and privacy

The script only reads a local JSON file and sends its contents to the Groq
API. Do not submit real logs, customer data, credentials, or internal
infrastructure details unless your organization's policy permits it. Keep
production access and consequential actions under approved human control.
