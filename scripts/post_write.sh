#!/bin/bash
# OMD PostToolUse hook: track file modifications, mark benchmarks stale
PIPELINE_DIR=".pipeline"
if [ -d "$PIPELINE_DIR/memory" ]; then
    echo "- File modified: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" >> "$PIPELINE_DIR/memory/orchestrator_state.md"
fi
