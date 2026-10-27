#!/usr/bin/env bash

set -euo pipefail

readonly DEFAULT_MODEL="llama-3.3-70b-versatile"
readonly API_URL="https://api.groq.com/openai/v1/chat/completions"

usage() {
  cat <<'EOF'
Usage: ai_health_check.sh [--service SERVICE_NAME] [--help]

Collect read-only Linux health metrics and ask Groq for an operational
summary. The script does not change system state.

Options:
  --service NAME  Include the active/inactive state of a systemd service
  --help          Show this help

Environment:
  GROQ_API_KEY    Required Groq API key
  GROQ_MODEL      Optional model override
EOF
}

service_name=""
while (($#)); do
  case "$1" in
    --service)
      if (($# < 2)) || [[ -z "$2" || "$2" == -* ]]; then
        echo "Error: --service requires a service name." >&2
        exit 2
      fi
      service_name="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Error: this example currently supports Linux only." >&2
  exit 2
fi

for command_name in awk curl df free getconf jq uptime; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Error: required command not found: $command_name" >&2
    exit 2
  fi
done

if [[ -z "${GROQ_API_KEY:-}" ]]; then
  echo "Error: set GROQ_API_KEY in your environment before running." >&2
  exit 2
fi

cpu_cores="$(getconf _NPROCESSORS_ONLN)"
load_average="$(awk '{print $1, $2, $3}' /proc/loadavg)"
memory_line="$(free -b | awk '$1 == "Mem:" {printf "{\"total_bytes\":%s,\"used_bytes\":%s,\"available_bytes\":%s}", $2, $3, $7}')"
root_disk_line="$(df -P -B1 / | awk 'NR == 2 {printf "{\"total_bytes\":%s,\"used_bytes\":%s,\"available_bytes\":%s,\"used_percent\":\"%s\"}", $2, $3, $4, $5}')"
uptime_text="$(uptime -p)"

if [[ -z "$memory_line" || -z "$root_disk_line" ]]; then
  echo "Error: could not collect memory or root filesystem metrics." >&2
  exit 1
fi

service_state="not_requested"
if [[ -n "$service_name" ]]; then
  if ! command -v systemctl >/dev/null 2>&1; then
    echo "Error: --service requires systemctl." >&2
    exit 2
  fi
  service_state="$(systemctl is-active "$service_name" 2>/dev/null || true)"
  service_state="${service_state:-unknown}"
fi

metrics="$(
  jq -n \
    --arg uptime "$uptime_text" \
    --arg load "$load_average" \
    --argjson cpu_cores "$cpu_cores" \
    --argjson memory "$memory_line" \
    --argjson root_filesystem "$root_disk_line" \
    --arg service_name "$service_name" \
    --arg service_state "$service_state" \
    '{
      uptime: $uptime,
      load_average_1_5_15_minutes: $load,
      cpu_cores: $cpu_cores,
      memory: $memory,
      root_filesystem: $root_filesystem,
      service: (if $service_name == "" then null else {name: $service_name, state: $service_state} end)
    }'
)"

prompt="You are assisting a DevOps engineer with a read-only Linux health check. Interpret only the supplied metrics. Give a concise summary, identify values that may warrant investigation, explain uncertainty, and suggest safe read-only follow-up checks. Do not claim a root cause from these metrics alone. Do not provide commands that change system state. Health data follows as JSON: $metrics"

request_body="$(
  jq -n \
    --arg model "${GROQ_MODEL:-$DEFAULT_MODEL}" \
    --arg content "$prompt" \
    '{
      model: $model,
      temperature: 0.2,
      messages: [{role: "user", content: $content}]
    }'
)"

echo "Collected health metrics (also sent to Groq for analysis):"
printf '%s\n\n' "$metrics" | jq .
echo "AI summary:"

response="$(
  curl --silent --show-error --fail-with-body \
    --connect-timeout 10 \
    --max-time 60 \
    "$API_URL" \
    -H "Authorization: Bearer ${GROQ_API_KEY}" \
    -H "Content-Type: application/json" \
    --data "$request_body"
)" || {
  echo "Error: Groq API request failed. Check connectivity, API key, and model." >&2
  exit 1
}

if ! jq -er '.choices[0].message.content | select(type == "string" and length > 0)' <<<"$response"; then
  echo "Error: Groq API response did not contain assistant text." >&2
  exit 1
fi
