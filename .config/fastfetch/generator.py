import math
import os

out_dir = os.path.expanduser("~/.config/fastfetch/frames")
os.makedirs(out_dir, exist_ok=True)

for f in os.listdir(out_dir):
    if f.endswith(".txt"):
        os.remove(os.path.join(out_dir, f))

width = 42
height = 21
cx = width / 2.0
cy = height / 2.0
tilt_factor = 0.50

print("[>] Forging Absolute Color-Controlled Matrix...")

speed_outer = 360.0 / 60.0   
speed_inner = -180.0 / 60.0  

def rgb(r, g, b): return f"\033[38;2;{r};{g};{b}m"

# outer Disc
c_crimson_void = rgb(40, 0, 7)      # F1: Dark as night crimson
c_dk_crimson   = rgb(50, 0, 10)     # F2: x
c_red_amber    = rgb(90, 20, 0)     # F2 "", F3 '
c_amber_gold   = rgb(200, 120, 0)   # F3 :%:
c_gold         = rgb(229, 169, 26)  # F3 lower :::
c_white_gold   = rgb(253, 208, 23) # F4 ,,, and %%
c_ashen        = rgb(255, 224, 0) # F4 :::

# Inner Disc
c_tox_purp   = rgb(35, 15, 55)      # F1: Toxic purple
c_purp_yell  = rgb(105, 80, 80)     # F2: u (purple/yellow hint)
c_purp_gold  = rgb(85, 60, 90)      # F2: ; (purple/gold hint)
c_dk_ox      = rgb(20, 60, 50)      # F3: ! (dark ox copper)
c_lt_ox      = rgb(45, 130, 110)    # F3: @ (lighter ox copper)
c_leaf_grn   = rgb(80, 160, 40)     # F4: ; (leaf green)
c_pure_ox    = rgb(67, 141, 128)    # F4: @ (pure ox copper)

# the Hub
c_dk_amber   = rgb(120, 50, 0)      # L1, L3 outer :
c_dkest_gold = rgb(140, 90, 10)     # L2 outer runes
c_dker_gold  = rgb(180, 120, 15)    # L2 inner runes, L3 outer %
c_pure_gold  = rgb(229, 169, 26)    # L2 innermost rune
c_amber      = rgb(210, 100, 0)     # L3 innermost %

def apply_color(string_list, color):
    return [[(char, color) for char in line] for line in string_list]

def get_outer_sprite(angle):
    dist = min(abs(angle - 90), 360 - abs(angle - 90))
    if dist > 135: 
        return apply_color([" # "], c_crimson_void)
    elif dist > 80: 
        return [[(' ', ''), ('x', c_dk_crimson), (' ', '')],
                [('"', c_red_amber), ('"', c_red_amber), (' ', '')]]
    elif dist > 35: 
        return [[(' ', ''), ("'", c_red_amber), (' ', '')],
                [(':', c_amber_gold), ('%', c_amber_gold), (':', c_amber_gold)],
                [(':', c_gold), (':', c_gold), (':', c_gold)]]
    else: 
        # left-offset %% block for correct front alignment
        return [[(',', c_white_gold), (',', c_white_gold), (',', c_white_gold)],
                [('%', c_white_gold), ('%', c_white_gold), (' ', '')],
                [(':', c_ashen), (':', c_ashen), (':', c_ashen)]]

def get_inner_sprite(angle):
    dist = min(abs(angle - 90), 360 - abs(angle - 90))
    if dist > 135: 
        return apply_color([" * "], c_tox_purp)
    elif dist > 80: 
        if 90 < angle < 270: 
            return [[(' ', ''), ('u', c_purp_yell), (';', c_purp_gold), (' ', '')]]
        else: 
            return [[(' ', ''), (';', c_purp_gold), ('u', c_purp_yell), (' ', '')]]
    elif dist > 35: 
        if 90 < angle < 270: 
            return [[(' ', ''), ('!', c_dk_ox), ('@', c_lt_ox), (' ', '')]]
        else: 
            return [[(' ', ''), ('@', c_lt_ox), ('!', c_dk_ox), (' ', '')]]
    else: 
        return [[(' ', ''), (';', c_leaf_grn), ('@', c_pure_ox), ('@', c_pure_ox), (';', c_leaf_grn), (' ', '')]]

def get_hub_sprite():
    #  color gradients mapped directly to coordinates
    l1 = [(' ', ''), (' ', ''), (',', c_dk_amber), (':', c_dk_amber), (':', c_dk_amber), (':', c_dk_amber), (',', c_dk_amber), (' ', ''), (' ', '')]
    l2 = [(' ', ''), (' ', ''), ('ᛖ', c_dkest_gold), ('ᛖ', c_dker_gold), ('ᛖ', c_pure_gold), ('ᛖ', c_dker_gold), ('ᛖ', c_dkest_gold), (' ', ''), (' ', '')]
    l3 = [(' ', ''), (' ', ''), (':', c_dk_amber), ('%', c_dker_gold), ('%', c_amber), ('%', c_dker_gold), (':', c_dk_amber), (' ', ''), (' ', '')]
    return [l1, l2, l3]

for frame in range(60):
    grid = [[(" ", "")] * width for _ in range(height)]
    render_queue = []

    #queue outer 
    for i in range(9):
        angle = (i * (360.0 / 9) + (frame * speed_outer)) % 360
        x_3d = 10.0 * math.cos(math.radians(angle))
        y_3d = 10.0 * math.sin(math.radians(angle))
        render_queue.append((y_3d, x_3d, get_outer_sprite(angle)))

    #queue inner 
    for i in range(4):
        angle = (i * (360.0 / 4) + (frame * speed_inner)) % 360
        x_3d = 5.0 * math.cos(math.radians(angle))
        y_3d = 5.0 * math.sin(math.radians(angle))
        render_queue.append((y_3d, x_3d, get_inner_sprite(angle)))

    #hub 
    render_queue.append((0.0, 0.0, get_hub_sprite()))

    render_queue.sort(key=lambda item: item[0])

    for z, x_3d, sprite_data in render_queue:
        cy2d = int(cy + z * tilt_factor)
        cx2d = int(cx + x_3d * 2.0)
        
        sy_start = cy2d - len(sprite_data) // 2
        for idx, line_data in enumerate(sprite_data):
            sy = sy_start + idx
            sx_start = cx2d - len(line_data) // 2 
            for j, (char, color) in enumerate(line_data):
                sx = sx_start + j
                if 0 <= sx < width and 0 <= sy < height:
                    if char != " ": 
                        grid[sy][sx] = (char, color)

    out_lines = []
    for row in grid:
        row_str = ""
        curr_color = ""
        for char, color in row:
            if char == " ":
                if curr_color != "":
                    row_str += "\033[0m"
                    curr_color = ""
                row_str += " "
            else:
                if color != curr_color:
                    row_str += color
                    curr_color = color
                row_str += char
        if curr_color != "": row_str += "\033[0m"
        out_lines.append(row_str)

    with open(f"{out_dir}/{frame+1:02d}.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

print("[>] SUCCESS: Multi-layered absolute color injection locked in.")
