#!/bin/bash
cd "$(cd "$(dirname "$0")" && pwd)"
sleep 300
echo "TASK COMPLETE - $(date)" > done.txt
