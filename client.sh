#!/usr/bin/env bash
#
# This is just an example in bash
#
[[ ! -p event_server ]] && mkfifo event_server

nc localhost 8888 <event_server &

ABSOLUTE_PIPE_PATH="$(readlink -e event_server)"

exec 1> >(tee "${ABSOLUTE_PIPE_PATH}") 2>&1

#
# Insert your code below
#

echo "Doing something"

i=0
while [[ i -lt 12 ]]
do
  echo "This is STDOUT $(date)"
  echo "This is STDERR -------" >&2
  sleep 1
  i=$((i+1))
done

