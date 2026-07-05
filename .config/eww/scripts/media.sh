#!/bin/bash

ARTIST=$(playerctl metadata --format '{{artist}}' 2>/dev/null || echo "")
TITLE=$(playerctl metadata --format '{{title}}' 2>/dev/null || echo "")

if [ -z "$TITLE" ]; then
    ARTIST="OFFLINE"
    TITLE="Awaiting Signal"
else
    if [ ${#ARTIST} -gt 22 ]; then ARTIST="${ARTIST:0:21}…"; fi
    if [ ${#TITLE} -gt 25 ]; then TITLE="${TITLE:0:24}…"; fi
fi

jq -n --arg artist "$ARTIST" --arg title "$TITLE" '{"artist": $artist, "title": $title}'
