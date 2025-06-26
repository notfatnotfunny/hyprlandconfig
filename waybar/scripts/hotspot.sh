#!/bin/bash

status=$(nmcli d | grep Hotspot | awk '{print $3}') 

if [[ "$status" == "connected" ]]; then
	echo ""
else
	echo ""
fi
