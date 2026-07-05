#!/bin/bash

if [[ "$1" == "discord" ]]; then
    if pgrep -i "discord" > /dev/null || pgrep -i "vesktop" > /dev/null; then
        echo "[ ᚦ ]"
    else
        echo ""
    fi

elif [[ "$1" == "steam" ]]; then
    if pgrep -i "steam" > /dev/null; then
        echo "[ ᛋ ]"
    else
        echo ""
    fi
fi
