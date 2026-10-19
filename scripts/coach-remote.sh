#!/bin/bash
# Launcher for the Remote Control server (run by the coach-remote systemd user service; see
# coach-remote.service). Lets Ricky chat with Coach from the Claude mobile app. Default
# permission mode, so every write (memory, calendar) prompts for approval on the phone.
# The server asks a one-time "Enable Remote Control? (y/n)" on stdin, so answer it and keep
# stdin open. claude is exec'd as the service's main process (stdin from a process
# substitution, not a pipe) so that when it exits systemd sees it and restarts the service.
export PATH="$HOME/.local/bin:$PATH"
cd "$(dirname "$0")/.." || exit 1
exec claude remote-control --name Coach --capacity 2 \
  --permission-mode default --spawn same-dir < <(echo y; exec sleep infinity)
