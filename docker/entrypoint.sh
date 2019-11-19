#!/bin/bash

set -e

COMMAND="$1"

case "$COMMAND" in
  web)
    exec python runserver.py
    ;;
  test)
    python -m pytest ${*:2}
    ;;
  *)
    exec bash -c "$*"
    ;;
esac
