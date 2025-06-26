#!/bin/bash

status=$(nmcli d | grep gsm | awk '{print $3}')

if [[ "$status" == "connected" ]]; then
  echo '{"text": "", "class": "connected"}'
else
  # echo "<span foreground=\"red\"><\span>"
  echo '{"text": "", "class": "disconnected"}'
fi

