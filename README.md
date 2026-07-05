# Golden Terminal // My Custom Arch + Hyprland Rice

<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/e08f5f8f-e73a-46e7-b0ae-8b3e8ad8a543" />


<img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/04671c58-85b8-4a07-9041-4522389e6e26" />





Hey! Welcome to my dotfiles repository.
This was HEAVILY inspired by Pewdiepie and I really tried to challenge myself every step of the way.
My idea of building this setup at first was to make a setup that was my own with my binds and an easy and enjoyable workflow that I try to create. So technically it's not meant for anybody else. 

But I just had to flex something that I put hundreds of hours into for the first time and I loved learning and doing this the entire way through. I am a changed man.

I spent WAY too much time fine-tuning this setup—building a custom hardware-accelerated OpenGL galaxy background in C++, overriding GTK themes by hand, and getting everything running as fast and lightweight as possible.

Like a space station terminal should be: this setup is very lightweight and runs on only 0.5 GB RAM on idle + dashboard and about 15% CPU overhead on an 11th gen intel i3. 


**A quick disclaimer before you start:** This setup was built and customized on *my* exact hardware (an Intel laptop running Arch Linux).
Wayland rices can sometimes be finicky when moved to another machine. Please, **backup your current `~/.config` folder before copying mine over!** 
I really don't want to accidentally overwrite your favorite keybinds or break your system panel.

The terminal has an animated ascii logo just like pewdiepie's but I added the python script that I made to generate the frames.
Because pewdiepie didnt include what he did to generate his, I figured it out and you can play around with the script and tweak it or whatever.
I even added shades to it just like pewds!! So the secret is finally out. (TBH I might've been the only one obsessing over it)

### The setup basically highlights two mode: 
1. Chill mode: Where you chill and listen to music and watch the visualizer and the galaxy animation.
2. Work mode: Where you got the waybar(activated with super+I once windows are actually on) and you work in a nice and organized environment. You can listen to music and I've binded media control(play/pause, skip/back).
So check out the hyprland.lua file in .config/hypr/hyprland.lua for the keybinds and whatever.

---

##  The Core Stack

Here are the primary packages powering this build (most can be grabbed via `pacman` or `yay`):

* **Window Manager:** `hyprland`
* **Widgets & HUD:** `eww` *(runs the main dashboard panel)*
* **Status Bar:** `waybar`
* **App Launcher:** `rofi-wayland` *(custom themed)*
* **Power Menu:** `wlogout`
* **Terminal & Shell:** `kitty` + `fastfetch` *(configured with a live hardware loop)*
* **System Monitors:** `btop` + `cava` *(audio visualizer)*
* **File Manager & GTK:** `thunar` *(uses strict dark mode overrides in `gtk-3.0`)*
* **Discord Alternative:** `vesktop` *(pre-configured with hardware acceleration flags, though not included in the dotfiles)*

### Quick Install Command (AUR + Pacman)
```bash
yay -S hyprland eww-wayland waybar rofi-wayland wlogout kitty fastfetch btop cava thunar vesktop
```
# CRITICAL BEFORE YOU LAUNCH (Please Read!)

**If you copy these configs over and certain things don't work out of the box, it is almost certainly due to one of these three hardware/path differences. Please check these first!**
**1. Battery & AC Adapter Names (Waybar / Lockscreen Fix)**

**Laptops name their power hardware differently depending on the motherboard. My configuration files hardcode my laptop's specific power identifiers: BAT1 (for the battery) and ACAD (for the charger).**

**If your battery widget shows up blank, reads 0%, or crashes your status bar, your laptop probably uses BAT0, ADP1, or something else entirely.**

How to check your hardware names:
Run this in your terminal right now:
```bash
ls /sys/class/power_supply/
```

Look at the output. If your battery says BAT0 instead of BAT1, open up the waybar and hyprlock configs and do a quick find-and-replace from BAT1 to BAT0.

Do the same for your AC adapter (ACAD vs ADP1 etc.).

## 2. The Wallpaper Path (normal.png)

The background daemon explicitly looks for a single file path to load the wallpaper into memory without relying on bulky GUI tools.

Inside the ~/.config/wallpapers/ folder, your primary wallpaper must be named exactly normal.png.
If you want to use your own wallpaper, don't edit the daemon scripts—just drop your PNG image into ~/.config/wallpapers/ and rename it to normal.png. If it's named anything else, you'll just get a black void on boot!

## 3. Compiling the C++ Starfield Background

The spinning galaxy widget on the dashboard isn't a heavy video or a GIF; it is a raw C++ binary rendering an OpenGL shader directly to your screen.
Because pre-compiled binaries often break when moved between different Linux kernel or library versions, you must compile the binary on your own machine.

Don't worry, I made a script for this in case you're the type to make your own figure and ever change the cpp code. Once you've placed the ~/.config folder in your home directory, run:
```bash
chmod +x ~/.config/eww/recompile.sh
~/.config/eww/recompile.sh
```
If it runs cleanly without outputting errors, the starfield.bin executable is built and ready to go!

##  Installation Steps

### 1.   Clone the repo:
```bash
git clone https://github.com/Midas-costly/golden-terminal-rice.git ~/golden-terminal-dotfiles
```
### 2.   Backup your existing configs (Seriously!):
```bash
mkdir -p ~/.config-backup
cp -r ~/.config/hypr ~/.config/waybar ~/.config/eww ~/.config-backup/ 2>/dev/null
```

### 3.   Copy the new configs over:
```bash
cp -r ~/ghost-dotfiles/.config/* ~/.config/
cp ~/ghost-dotfiles/.bashrc ~/
```

### 4.   Compile the galaxy engine:
```bash
~/.config/eww/recompile.sh
```

### 5.   Verify your battery identifiers using ```ls /sys/class/power_supply/``` and edit the configs if needed.

### 6.   Please read the terminal to check errors if any because I honestly forgot what else you have to be careful of in order to get it right.
     Sorry in advanced and you can document any problems and I'll be sure to fix those and add their details accordingly for the people that try the setup in the future.

### 7.   Log out of your desktop session and boot into Hyprland!

Good Luck and please contact in case of problems. I would love to sharpen this more. Please don't be afraid to nag over the small details!!
