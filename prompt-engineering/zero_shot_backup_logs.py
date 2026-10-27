from groq_client import generate


PROMPT = """
Write a Bash script to back up regular files from /var/logs to /backup.
Requirements:
- Return a script draft only; do not execute it.
- Use dry-run mode by default and require an explicit --apply option to copy.
- Create the destination if needed, report failures, and never delete source
  files.
- Briefly state assumptions in comments.
Return only the Bash script in a fenced code block.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
