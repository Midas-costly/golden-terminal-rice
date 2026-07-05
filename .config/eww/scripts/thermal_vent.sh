#!/bin/bash

if eww windows | grep -q "*dashboard"; then
    killall -q cava
    sleep 0.5
    cava -p ~/.config/cava/config_eww > /dev/null 2>&1 &
fi
