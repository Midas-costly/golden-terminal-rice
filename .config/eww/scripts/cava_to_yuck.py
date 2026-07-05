import sys

HEIGHT = 12
CHARS = [" ", ".", ":", "·", "•", "•"]

for line in sys.stdin:
    try:
        vals = [int(x) for x in line.strip().split(';') if x]
        if not vals: continue
        
        yuck_str = '(box :orientation "h" :space-evenly true :halign "fill" :valign "end" '
        
        for val in vals:
            col_str = ""
            for y in range(HEIGHT - 1, -1, -1):
                cv = val - (y * 5)
                if cv <= 0: char = CHARS[0]
                elif cv >= 5: char = CHARS[5]
                else: char = CHARS[cv]
                col_str += char + "\\n"
            
            yuck_str += f'(label :class "cava-col" :text "{col_str.strip()}") '
            
        yuck_str += ')'
        
        print(yuck_str, flush=True)
    except Exception:
        pass
