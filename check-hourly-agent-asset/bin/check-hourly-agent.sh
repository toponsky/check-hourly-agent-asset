#!/bin/sh
scriptDir="$(dirname $(dirname $(realpath $0)) )/bin"

# echo "$scriptDir"

/usr/bin/python "$scriptDir/check-hourly-agent.py"