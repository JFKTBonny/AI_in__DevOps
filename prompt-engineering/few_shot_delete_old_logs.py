from groq_client import generate


PROMPT = """
Use these examples as context for shell conventions.

Example 1 - create a log file:
  touch /var/logs/app.log
  printf '%s\\n' 'Application started' > /var/logs/app.log

Example 2 - archive log files:
  tar -czf /backup/app_logs.tar.gz /var/logs/*

Now draft a Bash script to find regular files older than seven days in
/var/logs. Do not run it. Preview matching paths by default and require an
explicit --apply option before deleting anything. Avoid following symlinks,
handle an empty match set clearly, and state that the target directory must
be reviewed before use. Return only the script in a fenced code block.
"""


if __name__ == "__main__":
    print(generate(PROMPT))
