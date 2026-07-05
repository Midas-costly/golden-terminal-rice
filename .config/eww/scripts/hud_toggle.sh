#!/bin/bash

if eww active-windows | grep -q "midas-dash"; then
    eww close midas-dash
else
    eww open midas-dash
fi
sleep 0.1
~/.config/eww/scripts/wallpaper_engine.sh
