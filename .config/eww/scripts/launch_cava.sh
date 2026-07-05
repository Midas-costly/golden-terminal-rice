#!/bin/bash

killall -q cava
hyprctl dispatch closewindow "class:ghost-cava" 2>/dev/null
hyprctl dispatch closewindow "title:ghost-cava" 2>/dev/null

mkdir -p ~/.config/cava
cat <<EOF > ~/.config/cava/config_native
[general]
framerate = 60
bars = 24

[input]
method = pulse
source = auto

[output]
method = ncurses

[color]
gradient = 0
foreground = '#E5A91A'
EOF

hyprctl dispatch exec "[float;size 836 374;move 2 704;pin;noborder] kitty --class ghost-cava -T ghost-cava -o background_opacity=1 -o background=#050400 -o window_padding_width=15 -e cava -p ~/.config/cava/config_native"
