#!/bin/bash

status_=$(cat /sys/class/power_supply/bq27411-0/status)

capacity=$(cat /sys/class/power_supply/bq27411-0/capacity)

if [[ "$status_" == "Charging" ]]; then
	echo '{"percentage": '$capacity', "alt": "charging"}'
elif [[ capacity -le 20 ]]; then
	echo '{"percentage": '$capacity', "class": "critical"}'
else
	
	echo '{"percentage": '$capacity'}'
fi
