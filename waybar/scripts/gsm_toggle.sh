#!/bin/bash


if [[ "$(nmcli radio wwan)" = "enabled" && "$(nmcli d | grep Hotspot | awk '{print $3}')" != "connected" ]]; then
	nmcli radio wwan off
else 
	nmcli radio wwan on
fi
