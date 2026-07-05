#!/bin/bash

STATE_FILE="/tmp/ghost_dash_state"

if [ ! -f "$STATE_FILE" ] || [ "$(cat "$STATE_FILE")" == "OFF" ]; then
    echo "ON" > "$STATE_FILE"
else
    echo "OFF" > "$STATE_FILE"
fi

if [ "$(cat "$STATE_FILE")" == "ON" ]; then
    if ! eww ping &>/dev/null; then
        killall -9 eww 2>/dev/null
        eww daemon &
        sleep 0.5
    fi
    eww open midas-dash 2>/dev/null
    
    if ! pgrep -f "starfield.bin" > /dev/null; then
        ~/.config/eww/scripts/starfield.bin &
    fi
else
    eww close midas-dash 2>/dev/null
    killall -9 starfield.bin 2>/dev/null
    
    sleep 0.2
    if eww active-windows 2>/dev/null | grep -q "midas-dash"; then
        killall -9 eww 2>/dev/null
        eww daemon &
    fi
fi
