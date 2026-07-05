#!/bin/bash

mkdir -p ~/.config/cava
cat <<EOF > ~/.config/cava/config_eww
[general]
framerate = 15
bars = 64
[input]
method = pipewire
source = auto
[output]
method = raw
raw_target = /dev/stdout
data_format = ascii
ascii_max_range = 60
EOF

cat << 'EOF' > ~/.config/eww/scripts/cava_to_json.py
import sys, json

HEIGHT = 12
CHARS = [" ", ".", ":", "·", "•", "•"]

for line in sys.stdin:
    try:
        vals = [int(x) for x in line.strip().split(';') if x]
        
        vals = vals[:64] + [0] * max(0, 64 - len(vals))
        
        matrix = []
        for y in range(HEIGHT - 1, -1, -1):
            row_str = ""
            for val in vals:
                cv = val - (y * 5)
                if cv <= 0: char = CHARS[0]
                elif cv >= 5: char = CHARS[5]
                else: char = CHARS[cv]
                row_str += char
            matrix.append(row_str)
            
        final_str = "\n".join(matrix)
        print(json.dumps({"matrix": final_str}), flush=True)
    except Exception:
        pass
EOF

killall -q cava
cava -p ~/.config/cava/config_eww 2>/dev/null | python3 ~/.config/eww/scripts/cava_to_json.py
