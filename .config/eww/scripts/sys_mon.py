#!/usr/bin/env python3
import time
import sys
import os
import subprocess
import glob

MAX_DOWN_KBS = 1.5 
MAX_UP_KBS = 1.5    

def get_bar(percent, char_full, char_empty, length=24):
    filled = max(0, min(length, int(round((percent / 100.0) * length))))
    return (char_full * filled) + (char_empty * (length - filled))

def get_cpu():
    try:
        with open('/proc/stat', 'r') as f: line = f.readline().split()
        idle = float(line[4]) + float(line[5])
        total = sum(float(x) for x in line[1:])
        return idle, total
    except: return 0, 0

def get_ram():
    try:
        with open('/proc/meminfo', 'r') as f: lines = f.readlines()
        total = free = buffers = cached = 0
        for line in lines:
            if line.startswith('MemTotal:'): total = int(line.split()[1])
            elif line.startswith('MemFree:'): free = int(line.split()[1])
            elif line.startswith('Buffers:'): buffers = int(line.split()[1])
            elif line.startswith('Cached:'): cached = int(line.split()[1])
        used = total - free - buffers - cached
        return (used / total) * 100, used / (1024*1024)
    except: return 0, 0

def get_disk():
    try:
        st = os.statvfs('/')
        total = st.f_blocks * st.f_frsize
        free = st.f_bavail * st.f_frsize
        return ((total - free) / total) * 100
    except: return 0

def get_swap():
    try:
        with open('/proc/meminfo', 'r') as f: lines = f.readlines()
        total = free = 0
        for line in lines:
            if line.startswith('SwapTotal:'): total = int(line.split()[1])
            elif line.startswith('SwapFree:'): free = int(line.split()[1])
        if total == 0: return 0, 0
        used = total - free
        return (used / total) * 100, used / (1024*1024)
    except: return 0, 0

def get_net():
    try:
        with open('/proc/net/dev', 'r') as f: lines = f.readlines()[2:]
        rx = tx = 0
        for line in lines:
            parts = line.split()
            if parts[0].strip(':') != 'lo': 
                rx += int(parts[1])
                tx += int(parts[9])
        return rx, tx
    except: return 0, 0

def get_uptime():
    try:
        with open('/proc/uptime', 'r') as f: uptime_sec = float(f.readline().split()[0])
    except: return "-" * 24, "00H 00M 00S"
    h_total = int(uptime_sec // 3600)
    h_cycle = h_total % 24
    m = int((uptime_sec % 3600) // 60)
    s = int(uptime_sec % 60)
    bar = "█" * h_cycle
    if h_cycle < 24:
        if m < 20: bar += "-"
        elif m < 40: bar += "▄"
        else: bar += "▆"
    bar += "-" * (24 - len(bar))
    return bar, f"{h_total:02d}H {m:02d}M {s:02d}S"

def get_battery():
    try:
        bat_path = glob.glob('/sys/class/power_supply/BAT*')[0]
        with open(f"{bat_path}/capacity", 'r') as f: cap = int(f.read().strip())
        with open(f"{bat_path}/status", 'r') as f: stat = f.read().strip()
        icon = "▲" if stat == "Charging" else "▼" if stat == "Discharging" else "■"
        lbl = "CHG " if stat == "Charging" else "PWR " 
        return cap, icon, lbl
    except: return 100, "■", "PWR "

def get_brightness():
    try:
        path = glob.glob('/sys/class/backlight/*')[0]
        with open(f"{path}/brightness", 'r') as f: curr = float(f.read().strip())
        with open(f"{path}/max_brightness", 'r') as f: mx = float(f.read().strip())
        return (curr / mx) * 100
    except: return 100.0

def get_volume():
    try:
        out = subprocess.check_output(['wpctl', 'get-volume', '@DEFAULT_AUDIO_SINK@'], encoding='utf-8')
        vol = float(out.split()[1]) * 100
        is_muted = "MUTED" in out
        return 0 if is_muted else vol
    except: return 0

def get_procs():
    try:
        out = subprocess.check_output(['ps', '-eo', 'pid,comm,%cpu,%mem', '--sort=-%cpu'], encoding='utf-8')
        lines = out.strip().split('\n')[1:6] # Top 5
        procs = []
        for line in lines:
            parts = line.split(None, 3)
            if len(parts) == 4:
                pid, comm, cpu, mem = parts
                # Strict spacing for absolute alignment
                procs.append(f"{pid:<6} {comm[:10]:<11} {cpu:>5}% {mem:>5}%")
        return procs
    except: return ["PROCESS SCAN ERROR"] * 5

def get_logs():
    try:
        out = subprocess.check_output(['journalctl', '-k', '-q', '-n', '5', '--no-pager'], encoding='utf-8')
        logs = []
        for line in out.strip().split('\n'):
            log = line[line.find("]")+1:].strip() if "]" in line else line
            logs.append(log[:42]) 
        return logs
    except: return ["KERNEL LOG STREAM UNAVAILABLE"] * 5

def get_wifi_status():
    try:
        conn_state = subprocess.check_output(['nmcli', '-t', '-f', 'CONNECTIVITY', 'g'], encoding='utf-8').strip()
        
        if conn_state == 'none':
            return "[OFFL]"
            
        out = subprocess.check_output(['nmcli', '-t', '-f', 'active,signal', 'dev', 'wifi'], encoding='utf-8')
        for line in out.splitlines():
            if line.startswith('yes:'):
                signal = int(line.split(':')[1])
                
                if conn_state in ['limited', 'portal']:
                    return "[CNWI]"
                elif signal >= 50:
                    return "[STRG]"
                else:
                    return "[WEAK]"
                    
        return "[OFFL]"
    except:
        return "[ERR ]"

prev_idle, prev_total = get_cpu()
prev_rx, prev_tx = get_net()

while True:
    time.sleep(1)
    
    curr_idle, curr_total = get_cpu()
    diff_idle, diff_total = curr_idle - prev_idle, curr_total - prev_total
    cpu_pct = (1000 * (diff_total - diff_idle) / diff_total + 5) / 10 if diff_total > 0 else 0
    prev_idle, prev_total = curr_idle, curr_total
    
    ram_pct, ram_gb = get_ram()
    disk_pct = get_disk()
    swp_pct, swp_gb = get_swap()

    temp_c = 0.0
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f: temp_c = int(f.read()) / 1000.0
    except: pass
    temp_pct = min(100, max(0, (temp_c / 100.0) * 100))

    curr_rx, curr_tx = get_net()
    rx_kbs = (curr_rx - prev_rx) / 1024.0
    tx_kbs = (curr_tx - prev_tx) / 1024.0
    prev_rx, prev_tx = curr_rx, curr_tx

    rx_pct = min(100, (rx_kbs / MAX_DOWN_KBS) * 100)
    tx_pct = min(100, (tx_kbs / MAX_UP_KBS) * 100)
    
    uptm_bar, uptm_val = get_uptime()
    
    bat_pct, bat_icon, bat_lbl = get_battery()
    bri_pct = get_brightness()
    vol_pct = get_volume()
    procs = get_procs()
    logs = get_logs()
    wifi_stat = get_wifi_status()

    import json
    data = {
        "cpu_bar": get_bar(cpu_pct, "█", "░"), "cpu_val": f"{cpu_pct:04.1f}",
        "ram_bar": get_bar(ram_pct, "#", "-"), "ram_val": f"{ram_gb:04.1f}",
        "tmp_bar": get_bar(temp_pct, "*", "."), "tmp_val": f"{temp_c:04.1f}",
        "dsk_bar": get_bar(disk_pct, "=", "-"), "dsk_val": f"{disk_pct:04.1f}",
        "swp_bar": get_bar(swp_pct, "■", "-"), "swp_val": f"{swp_gb:04.1f}",
        "uptm_bar": uptm_bar, "uptm_val": uptm_val,
        "net_down_bar": get_bar(rx_pct, "▼", "-"), "net_down_val": f"{rx_kbs:07.1f}", 
        "net_up_bar": get_bar(tx_pct, "▲", "-"), "net_up_val": f"{tx_kbs:07.1f}",
        
        "bat_bar": get_bar(bat_pct, bat_icon, "-"), "bat_val": f"{bat_pct:03d}%", "bat_lbl": bat_lbl,
        "bri_bar": get_bar(bri_pct, "☀", "-"), "bri_val": f"{bri_pct:03.0f}%",
        "vol_bar": get_bar(vol_pct, "/", "-"), "vol_val": f"{vol_pct:03.0f}%",
        "wifi_stat":wifi_stat,
        "procs": procs,
        "logs": logs
    }
    print(json.dumps(data))
    sys.stdout.flush()
