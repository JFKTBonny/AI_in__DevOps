# AI-Assisted Shell Scripting for DevOps

This example shows AI assisting during an operational health check—not merely
writing a script. The Bash script collects read-only Linux metrics, sends
those metrics to the Groq API, and displays an AI-generated summary with safe
follow-up checks.

The script does **not** execute recommendations or modify the machine.

## What it collects

- System uptime
- 1-, 5-, and 15-minute load averages and CPU core count
- Memory totals, usage, and available memory
- Root filesystem usage
- Optionally, whether a named systemd service is active

It does not collect logs, environment variables, or credentials. The collected
metrics are sent to Groq for analysis, so use this only where your
organization's data policy permits sending this operational information to an
external service.

## Requirements

- Linux with Bash
- `curl`, `jq`, `awk`, `df`, `free`, `getconf`, and `uptime`
- For `--service`, `systemctl`
- A Groq API key

## Run

Set the API key without putting it in the script:

```bash
export GROQ_API_KEY="your-api-key"
```

Make the script executable and run it:

```bash
chmod +x ai_health_check.sh
./ai_health_check.sh
```

To include a systemd service state:

```bash
./ai_health_check.sh --service nginx
```

The default model is `llama-3.3-70b-versatile`. Override it with a model
available to your Groq account:

```bash
export GROQ_MODEL="your-available-model"
```

Use `./ai_health_check.sh --help` for command usage.

## How AI helps in this workflow

Traditional checks can report raw measurements or alert on fixed thresholds.
Here, the model receives a small structured snapshot and explains which
signals may deserve attention, while noting uncertainty and suggesting
read-only checks. This can help an operator orient more quickly, but the
response is not a diagnosis: verify it against monitoring, logs, and the
machine's actual state.

Review the script before use. Never pipe AI-generated suggestions directly
into a shell or grant an AI model unattended production access.
