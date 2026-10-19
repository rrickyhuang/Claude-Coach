#!/bin/bash
# Launcher for the Remote Control server (run by the coach-remote systemd user service).
# Lets Ricky chat with Coach from the Claude mobile app. Default permission mode, so every
# write (memory, calendar) prompts for approval on the phone. The server asks a one-time
# "Enable Remote Control? (y/n)" question on stdin, so answer it and keep stdin open.
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.." || exit 1
(echo y; exec sleep infinity) | exec claude remote-control --name Coach --capacity 2 \
  --permission-mode default --spawn same-dir
