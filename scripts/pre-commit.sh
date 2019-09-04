#!/bin/bash
set -e

[ -n "$NO_HOOK" ] && exit 0

[ -n "$INNER_PRE_HOOK" ] && {
  # http://stackoverflow.com/a/21334985/1123955
  exit 0
}

autopep8 --verbose --in-place --recursive .

