#!/bin/bash
cd "$(cd "$(dirname "$0")" && pwd)"
# TODO: also stop the polling watcher task itself here, not just long-task.sh
# Kills the background long-task.sh job if it's still running.
# The polling watcher itself is a harness-tracked task and is stopped
# separately via TaskStop, not by this script.
if [ -f long-task.pid ]; then
  pid="$(cat long-task.pid)"
  if kill "$pid" 2>/dev/null; then
    echo "Stopped long-task.sh (pid $pid)"
  else
    echo "No running process for pid $pid (already finished?)"
  fi
  rm -f long-task.pid
else
  echo "No long-task.pid file found — nothing to stop"
fi
