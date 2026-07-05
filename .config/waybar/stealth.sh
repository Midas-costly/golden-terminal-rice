#!/bin/bash

for pid in $(pgrep -f stealth.sh); do
    if [ "$pid" != "$$" ]; then
        kill -9 "$pid"
    fi
done
killall -9 waybar 2>/dev/null

waybar &

sleep 1

STATE="visible"

function check_hud() {
    WINDOWS=$(hyprctl activeworkspace | grep "windows:" | awk '{print $2}')

    if [[ "$WINDOWS" == "0" && "$STATE" == "visible" ]]; then
        pkill -SIGUSR1 waybar
        STATE="hidden"
    elif [[ "$WINDOWS" != "0" && "$STATE" == "hidden" ]]; then
        pkill -SIGUSR1 waybar
        STATE="visible"
    fi
}

check_hud

socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do
    if [[ $line == *"openwindow"* ]] || [[ $line == *"closewindow"* ]] || [[ $line == *"workspace"* ]]; then
        check_hud
    fi
done
