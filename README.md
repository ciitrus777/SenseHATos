# SenseHATos
A small low-functionality program that allows you to run a small desktop on the Sense HAT.

Current features include:
- Desktop
- Ability to change wallpaper
- Run apps

I probably won't do a lot with this as I don't think this is useful for anybody.

## To use:
Add wallpapers to the same directory as OS.py
Put applications in the apps folder.
Folders are not supported yet.
If apps open a new window in your main OS, there must be a way to close this window.
### Paint instructions
Number keys correlate to changing colours, the colour is shown in the pygame window.
Left click to paint, right click to erase, and middle click to erase all.
Q to fill the entire canvas, and E to disable the cursor.

Press Escape in any of the two built-in apps to quit, Paint requires pressing Escape twice.

Up, down, and enter to navigate menus.

Text must finish scrolling before you confirm.

Text may bug out, I can't seem to fix this.

## Error codes
1: Mouse moved out of bounds (the mouse must stay inside of the window)
