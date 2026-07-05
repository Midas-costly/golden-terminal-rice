#!/bin/bash

DELAY=0.04
ASCII_DIR="$HOME/.config/fastfetch/frames"
CACHE_FILE="$HOME/.cache/midas_telemetry.txt"

fastfetch --logo none > "$CACHE_FILE"

clear
tput civis
trap 'tput cnorm; echo ""; exit' INT TERM

row=1
while IFS= read -r line; do
    tput cup $row 45
    echo -e "$line"
    ((row++))
done < "$CACHE_FILE"

while true; do
    for frame in "$ASCII_DIR"/*.txt; do
        tput cup 1 1
        cat "$frame"
        read -t $DELAY -n 1 key && { tput cnorm; echo ""; exit; }
    done
done
