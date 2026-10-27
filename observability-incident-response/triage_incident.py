#!/usr/bin/env python3
"""Ask Groq to summarize a synthetic or user-supplied incident snapshot."""

import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
DEFAULT_SNAPSHOT = Path(__file__).with_name("incident_snapshot.json")


def load_snapshot(path):
    try:
        with path.open(encoding="utf-8") as snapshot_file:
            snapshot = json.load(snapshot_file)
    except OSError as error:
        raise RuntimeError(f"Could not read snapshot '{path}': {error}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Snapshot '{path}' is not valid JSON: {error}") from error

    if not isinstance(snapshot, dict):
        raise RuntimeError("Incident snapshot must contain a JSON object.")
    return snapshot


def analyze(snapshot, api_key, model):
    prompt = (
        "You are assisting with a cloud-native service incident. Analyze only "
        "the supplied snapshot. Summarize the observed impact and timeline; "
        "separate facts from hypotheses; identify evidence that may be related "
        "without claiming correlation proves causation; and suggest a short "
        "ordered list of safe, read-only checks. Do not provide commands that "
        "change system state or claim to have accessed a cluster. "
        "Incident snapshot JSON:\n"
        + json.dumps(snapshot, indent=2)
    )
    body = json.dumps(
        {
            "model": model,
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}],
        }
    ).encode("utf-8")
    request = Request(
        API_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Groq API returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach the Groq API: {error.reason}") from error
    except json.JSONDecodeError as error:
        raise RuntimeError("Groq API returned an invalid JSON response.") from error

    try:
        content = result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Groq API response did not contain assistant text.") from error
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("Groq API returned an empty assistant response.")
    return content


def main():
    if len(sys.argv) > 2:
        print(f"Usage: {Path(sys.argv[0]).name} [snapshot.json]", file=sys.stderr)
        return 2

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: set GROQ_API_KEY before running.", file=sys.stderr)
        return 2

    snapshot_path = Path(sys.argv[1]) if len(sys.argv) == 2 else DEFAULT_SNAPSHOT
    try:
        snapshot = load_snapshot(snapshot_path)
        summary = analyze(
            snapshot,
            api_key,
            os.environ.get("GROQ_MODEL", DEFAULT_MODEL),
        )
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("AI-assisted incident triage")
    print("===========================")
    print(summary)
    print("\nVerify these observations against your monitoring and incident process.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
