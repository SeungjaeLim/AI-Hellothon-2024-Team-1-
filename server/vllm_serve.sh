#!/bin/bash

# Script to run two vllm servers in a tmux session

# Configuration
SESSION_NAME="Ssaem"
MODEL_1="meta-llama/Meta-Llama-3-70B-Instruct"
MODEL_2="BAAI/bge-multilingual-gemma2"
API_KEY_1="token-abc123"
API_KEY_2="token-def456"
DTYPE="auto"

# Check if tmux session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session '$SESSION_NAME' already exists. Attaching..."
  tmux attach -t "$SESSION_NAME"
else
  echo "Creating new tmux session: $SESSION_NAME"
  tmux new-session -d -s "$SESSION_NAME" -n "server1"

  # Start the first server in the first tmux pane
  tmux send-keys -t "$SESSION_NAME:0" "vllm serve $MODEL_1 --dtype $DTYPE --api-key $API_KEY_1" C-m
  
  # Create a new pane for the second server
  tmux split-window -h -t "$SESSION_NAME:0"

  # Start the second server in the new pane
  tmux send-keys -t "$SESSION_NAME:0.1" "vllm serve $MODEL_2 --dtype $DTYPE --api-key $API_KEY_2" C-m

  # Attach to the tmux session
  tmux attach -t "$SESSION_NAME"
fi
