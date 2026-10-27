from groq_client import generate


PROMPT = """
Help diagnose this Bash script's "permission denied" error:

#!/usr/bin/env bash
mkdir -p /backup
cp /var/logs/* /backup/

Give a concise, numbered diagnostic checklist. Start with read-only checks
that identify the failing path and inspect source/destination ownership,
permissions, and relevant ACL or mount details. Explain what evidence to
look for. Recommend least-privilege fixes only after diagnosis. Do not
default to sudo, change security labels, or execute commands. Separate any
potentially mutating command into an optional remediation section and explain
its impact.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
