#!/bin/bash

# Default values
AGENT_PERSONA=${AGENT_PERSONA:-developer}
SLEEP_INTERVAL=${SLEEP_INTERVAL:-3600} # 1 hour
TASK_ID=${TASK_ID:-}

echo "--- Docker Agent Entrypoint ---"
echo "Starting agent execution loop..."
echo "Agent Persona: ${AGENT_PERSONA}"
echo "Sleep Interval: ${SLEEP_INTERVAL} seconds"
if [ -n "$TASK_ID" ]; then
    echo "Target Task ID: ${TASK_ID}"
fi
echo "------------------------------"


while true; do
  echo "[$(date)] Running agent..."
  
  CMD_ARGS=("--agent" "${AGENT_PERSONA}")
  if [ -n "$TASK_ID" ]; then
      CMD_ARGS+=("--task" "${TASK_ID}")
  fi
  
  python3 run.py "${CMD_ARGS[@]}"
  
  echo "[$(date)] Agent run finished. Sleeping for ${SLEEP_INTERVAL} seconds..."
  sleep "${SLEEP_INTERVAL}"
done
