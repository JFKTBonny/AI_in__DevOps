# AI-Assisted DevOps

A collection of learning notes and practical examples exploring how AI,
machine learning, and large language models can support DevOps work. The
examples cover prompt engineering, script generation, log analysis, incident
triage, read-only agents, documentation Q&A concepts, and a Kubernetes
capstone.

Some chapters are runnable demonstrations; others are notes or project
proposals. Each folder's README describes its own setup and limitations.
Generated advice and code are examples to review—not production instructions.

## Course map

| Day | Folder | What you'll find |
|---|---|---|
| 1 | [`introduction-to-ai-for-devops/`](introduction-to-ai-for-devops/) | Introductory notes on predictive and generative AI, LLMs, DevOps use cases, and responsible use. The folder is notes-focused. |
| 2 | [`prompt-engineering/`](prompt-engineering/) | Zero-shot, few-shot, multi-shot, and step-by-step troubleshooting examples for shell and Kubernetes tasks. Python examples send prompts to Groq; they print responses rather than executing generated commands. |
| 3 | [`llm-dockerfile-generation/`](llm-dockerfile-generation/) | Python generators that request Dockerfile drafts from a local Ollama model or the hosted Gemini API. Review and test generated output yourself. |
| 4 | [`ai-assisted-shell-scripting/`](ai-assisted-shell-scripting/) | A Bash health-check script that gathers read-only Linux metrics and asks Groq for a summary and suggested checks. |
| 5 | [`observability-incident-response/`](observability-incident-response/) | A Groq-powered incident summary based on a synthetic snapshot of deployment events, metrics, and logs. It suggests read-only follow-up checks. |
| 6 | [`aiops-log-analysis/`](aiops-log-analysis/) | Two analyses of synthetic logs: fixed 30-second ERROR-count thresholds and Isolation Forest anomaly detection. These examples use conventional Python/data-science methods, not an LLM. |
| 7 | [`ai-agents-for-devops/`](ai-agents-for-devops/) | A bounded Groq agent that investigates a local CI log using allowlisted, read-only summary and search tools. Includes a synthetic failed build. |
| 8 | [`internal-documentation-agent/`](internal-documentation-agent/) | Notes describing an internal documentation assistant built with retrieval-augmented generation (RAG), including citations and access-control considerations. This folder contains a concept, not a runnable RAG implementation. |
| 9 | [`security-and-finops/`](security-and-finops/) | Notes and a practical scenario for using AI to summarize dependency-scan and cloud-cost reports. This folder does not yet include a runnable analyzer. |
| 10 | [`devops-ai-capstone/`](devops-ai-capstone/) | A runnable, read-only incident-triage API with bounded tool use, synthetic input, tests, a Dockerfile, and Kubernetes deployment manifests. |

## Getting started

Choose a chapter and follow its README. Requirements vary: some examples use
Python's standard library, some need additional Python packages, and
Groq/Gemini examples require an API key and network access. The capstone also
documents local Docker and Kubernetes deployment options.

For examples that call a hosted model, keep API keys in environment variables
and send only data approved for that provider. Prefer synthetic or sanitized
inputs. Verify model output against source data, and keep human approval for
changes to systems or infrastructure.

## Safety and scope

- Treat generated explanations, commands, and configuration as unverified
  drafts.
- The incident-triage and CI-agent examples are designed to inspect supplied
  evidence; they do not make operational changes.
- Do not provide production access, secrets, customer data, or confidential
  logs unless your organization's policies explicitly allow it.
- Test generated code and configuration in a safe environment before use.
