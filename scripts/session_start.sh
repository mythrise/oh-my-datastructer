#!/bin/bash
# OMD SessionStart hook: detect project state, print status summary
PIPELINE_DIR=".pipeline"
if [ -d "$PIPELINE_DIR" ]; then
    if [ -f "$PIPELINE_DIR/memory/orchestrator_state.md" ]; then
        echo "[OMD] Project state loaded"
        head -5 "$PIPELINE_DIR/memory/orchestrator_state.md" 2>/dev/null
    fi
    if [ -f "$PIPELINE_DIR/tasks.json" ]; then
        PENDING=$(grep -c '"pending"' "$PIPELINE_DIR/tasks.json" 2>/dev/null || echo "0")
        DONE=$(grep -c '"done"' "$PIPELINE_DIR/tasks.json" 2>/dev/null || echo "0")
        echo "[OMD] Tasks: $DONE completed, $PENDING pending"
    fi
else
    echo "[OMD] No project initialized. Use /ds:init to start a new assignment."
fi
