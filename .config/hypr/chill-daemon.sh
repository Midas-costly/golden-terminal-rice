#!/bin/bash

STATE_FILE="/tmp/ghost_dash_state"

echo "OFF" > "$STATE_FILE"

if ! eww ping &> /dev/null; then
    eww daemon &
fi

killall -9 hyprpaper 2>/dev/null
sleep 0.5
hyprpaper &
sleep 0.5

hyprctl hyprpaper preload "/home/midas/.config/wallpapers/normal.png" &> /dev/null
hyprctl hyprpaper wallpaper ",/home/midas/.config/wallpapers/normal.png" &> /dev/null

eww close midas-dash 2>/dev/null
killall -9 starfield.bin 2>/dev/null

evaluate_state() {
    INTENT=$(cat "$STATE_FILE" 2>/dev/null || echo "OFF")
    
    ACTIVE_WS=$(hyprctl activeworkspace -j | jq '.id')
    WIN_COUNT=$(hyprctl workspaces -j | jq ".[] | select(.id == $ACTIVE_WS) | .windows")
    if [ -z "$WIN_COUNT" ]; then WIN_COUNT=0; fi

    if [ "$INTENT" == "ON" ] && [ "$WIN_COUNT" -eq 0 ]; then
        if ! eww active-windows | grep -q "midas-dash"; then
            eww open midas-dash &> /dev/null
        fi
        if ! pgrep -f "starfield.bin" > /dev/null; then
            ~/.config/eww/scripts/starfield.bin &
        fi
    else
        if eww active-windows | grep -q "midas-dash"; then
            eww close midas-dash &> /dev/null
        fi
        if pgrep -f "starfield.bin" > /dev/null; then
            killall -9 starfield.bin 2>/dev/null
        fi
    fi
}

socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do
    case "${line%%>>*}" in
        "workspace"|"openwindow"|"closewindow"|"movewindow")
            evaluate_state
            ;;
    esac
done
