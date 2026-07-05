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
