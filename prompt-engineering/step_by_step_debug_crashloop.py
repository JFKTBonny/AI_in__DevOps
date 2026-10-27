from groq_client import generate


PROMPT = """
Help troubleshoot a Kubernetes pod reported as CrashLoopBackOff.
Give a concise, numbered, evidence-based diagnostic checklist. Begin with
read-only checks such as `kubectl get pod`, `kubectl describe pod`, and
`kubectl logs` (including `--previous` when relevant). Explain what to
inspect: events, exit code, container logs, image, command, probes, resources,
mounted configuration, and recent changes. Ask for namespace and container
if unknown. Do not propose or run mutating commands in the initial checklist;
put possible remediation behind a separate human-review step and connect it
to evidence.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
