#!/bin/bash
# OMD Stop hook: update orchestrator state with session end timestamp
PIPELINE_DIR=".pipeline"
if [ -d "$PIPELINE_DIR/memory" ]; then
    echo "" >> "$PIPELINE_DIR/memory/orchestrator_state.md"
    echo "## Session ended: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$PIPELINE_DIR/memory/orchestrator_state.md"
fi
