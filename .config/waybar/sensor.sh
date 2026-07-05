#!/bin/bash

FILE="/tmp/workspace_sensor.txt"

active=$(hyprctl activeworkspace -j | grep '"name"' | head -n 1 | awk -F'"' '{print $4}')
echo "$active" > "$FILE"

socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do
    if [[ $line == "workspace>>"* ]]; then
        echo "${line#workspace>>}" > "$FILE"
        pkill -RTMIN+5 waybar
    fi
done
