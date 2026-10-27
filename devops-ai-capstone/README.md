# DevOps AI Incident-Triage Capstone

Build and deploy a small AI agent that investigates a supplied incident
snapshot and produces an evidence-based triage report. The example uses
synthetic data and a Groq-hosted language model.

## What it does

The HTTP service accepts an incident snapshot containing an incident summary,
timeline, metrics, and log samples. The model can choose from three allowlisted
read-only tools to inspect that snapshot:

- `get_incident_overview` reads incident metadata and the timeline.
- `get_metric_trend` reads points for one supported metric.
- `search_log_samples` searches the supplied log lines.

The agent loop is capped at six tool calls. It cannot run shell commands,
query Kubernetes, access other files, or change infrastructure. The response
includes the report and an empty `actions_taken` list. All tool results come
only from the request body; the sample incident is synthetic.

## Run locally

Requirements: Python 3.9+ and a Groq API key. The service sends the submitted
incident snapshot and tool results to the Groq API. Use only synthetic or
sanitized data unless your organization's policy explicitly permits external
processing.

From this directory:

```bash
export GROQ_API_KEY="your-api-key"
python3 app.py
```

In another terminal, check health and submit the included sample:

```bash
curl http://localhost:8080/healthz
curl -X POST http://localhost:8080/triage \
  -H 'Content-Type: application/json' \
  --data-binary @incident_snapshot.json
```

The triage response is JSON with `incident_id`, `triage`, and `actions_taken`.
Set `GROQ_MODEL` to select another model supported by your Groq account.

## Tests

The test suite uses only Python's standard library and does not make API calls:

```bash
python3 -m unittest discover -s tests -v
```

## Build and run with Docker

```bash
docker build -t devops-ai-capstone:local .
docker run --rm -p 8080:8080 \
  -e GROQ_API_KEY \
  devops-ai-capstone:local
```

Then use the same `curl` requests above.

## Deploy to Kubernetes

Create the API key as a Kubernetes Secret (use your organization's approved
secret-management process for anything beyond a local demo):

```bash
kubectl create secret generic groq-api \
  --from-literal=api-key="$GROQ_API_KEY"
```

Build the image and make it available to your cluster. For example, with
Kind:

```bash
docker build -t devops-ai-capstone:local .
kind load docker-image devops-ai-capstone:local
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/devops-ai-capstone
kubectl port-forward service/devops-ai-capstone 8080:8080
```

For Minikube, use `minikube image load devops-ai-capstone:local` instead.
Other clusters need the image pushed to a registry they can access; update
the image in `k8s/deployment.yaml` accordingly. The service is `ClusterIP`
only and is not exposed publicly. The pod runs as a non-root user with a
read-only root filesystem and restricted Linux capabilities.

## Limitations and safe use

- The model can misread evidence or produce unsupported recommendations.
  Verify findings against the original monitoring data and incident process.
- The timeline may correlate with a deployment without proving it caused the
  incident.
- Do not submit production logs, customer data, credentials, or internal
  infrastructure details unless approved for the configured model provider.
- This demo has no user authentication or authorization. Keep it internal;
  add appropriate identity controls before exposing it beyond a trusted
  environment.
- The Kubernetes Secret is only a demo mechanism. Base64-encoded Secret data
  is not encryption by itself; configure cluster encryption and access
  controls or use an approved external secret manager.
- The agent is advisory and does not mitigate incidents or execute
  recommendations.
