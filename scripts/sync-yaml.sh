#!/bin/sh
set -eu

cd "$(dirname "$0")/.."

for base in ai ben capcut mmc mmcdirect twitter ziniao; do
  tmp_file=$(mktemp)
  {
    printf '%s\n' 'payload:'
    awk '!/^($|#)/ { print "  - " $0 }' "$base.list"
  } >"$tmp_file"
  mv "$tmp_file" "$base.yaml"
done
