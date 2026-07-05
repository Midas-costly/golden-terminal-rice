#!/bin/bash

print_workspaces() {
    ACTIVE=$(hyprctl activeworkspace -j 2>/dev/null | jq '.id' 2>/dev/null || echo 0)
    [[ -z "$ACTIVE" || "$ACTIVE" == "null" ]] && ACTIVE=0
    
    OCCUPIED=$(hyprctl workspaces -j 2>/dev/null | jq -c '[.[] | select(.windows > 0) | .id]' 2>/dev/null || echo "[]")
    
    JSON="["
    ROMANS=("I" "II" "III" "IV" "V" "VI" "VII" "VIII" "IX" "X")
    for i in {1..10}; do
        ROMAN="${ROMANS[$((i-1))]}"
        STATE="clear"
        if [ "$i" -eq "$ACTIVE" ]; then
            STATE="active"
        elif echo "$OCCUPIED" | grep -q "\b$i\b"; then
            STATE="danger"
        fi
        JSON+="{\"id\":$i, \"roman\":\"$ROMAN\", \"state\":\"$STATE\"}"
        [ $i -lt 10 ] && JSON+=","
    done
    JSON+="]"
    echo "$JSON"
}

print_workspaces

socat -U - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock 2>/dev/null | while read -r line; do
    case "${line%%>>*}" in
        workspace|openwindow|closewindow|movewindow)
            print_workspaces
            ;;
    esac
done
