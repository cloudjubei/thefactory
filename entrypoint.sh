#!/bin/sh

set -e

if [ ! -z "$TEST_MODE" ]; then
    while true; do
        echo "Test run at $(date)"
        sleep ${SLEEP_INTERVAL:-3600}
    done
else
    while true; do
        echo "Starting agent run at $(date)"
        python scripts/autonomous_agent.py --agent developer --model gpt-4-turbo-preview
        sleep ${SLEEP_INTERVAL:-3600}
    done
fi