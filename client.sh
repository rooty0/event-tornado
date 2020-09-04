#!/usr/bin/env bash
: "${RTLOG_IP:="10.72.1.9"}"
: "${RTLOG_PORT:="8888"}"

if ! command -v bftee >/dev/null
then
  echo "bftee is missing"
  exit 1
fi

[[ ! -p event_server ]] && mkfifo event_server
nc "${RTLOG_IP}" "${RTLOG_PORT}" <event_server &
ABSOLUTE_PIPE_PATH="$(readlink -e event_server)"
exec 1> >(bftee "${ABSOLUTE_PIPE_PATH}")
exec 2> >(bftee "${ABSOLUTE_PIPE_PATH}" >&2)

#
# To use this just add "source client.sh" line on top of your script
#
# I'm going to insert some code for the sake of the example below.
# Obviously, you want to delete it if you are going to include this file
echo "Doing something"

i=0
while [[ i -lt 12 ]]
do
  echo "This is STDOUT $(date)"
  echo "This is STDERR -------" >&2
  sleep 1
  i=$((i+1))
done
