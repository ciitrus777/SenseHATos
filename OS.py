from sense_emu import SenseHat
import random
from time import sleep
import pygame
import threading
import os
import subprocess

disk = 0
try:
    disk = open("s")
except:
    disk = open("s", "x")

ds = 100

ava = 0

pygame.init()

# Set up the game window
screen = pygame.display.set_mode((8*ds, 8*ds))
pygame.display.set_caption("OSense")
sense = SenseHat()

r = [255,0,0]
g = [0,255,0]
b = [0,0,255]
y = [255, 255, 0]
lb =[0,255,255]
m = [255, 0, 255]
w = [255, 255, 255]

running = True
oldmx = "s"
oldmy = "s"
oldcol = [0, 0, 0]

temp = disk.readlines()
if len(temp[0]) > 0:
    wallpaper = temp[0]
    print(wallpaper)
else:
    wallpaper = "bliss.png"

col = w

def bluescreen(cause):
    error = "0"
    if cause == "OOB":
        error = "1"
    sense.show_letter(error, text_colour = [255, 255, 255], back_colour = [0, 0, 255])
    sleep(2)
    print("dead")
    running = False
    pygame.quit()

from PIL import Image

noAction = True
Action = None

def showmsgthread(str, scr, ba):
    sense.show_message(str, scroll_speed=scr, back_colour=ba)

def Fillscreen(colour):
    oldcol = colour
    for o in range(8):
        for i in range(8):
            sense.set_pixel(i,o, colour)

def BootUp():
    delay = 0.1
    for i in range(1024):
        for o in range(8):
            randc = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            for i in range(8):
                    sense.set_pixel(i,o, randc)
            sleep(delay)
        delay = delay / 1.5

def ShowWallpaper():
    img = 0
    try:
        wallpaper2 = wallpaper.replace('\n', '').replace('\r', '')
        img = Image.open(str(wallpaper2))
    except:
        img = Image.open("bliss.png")
    res = img.resize((8, 8))
    resBG = res.convert('RGB')
    px = resBG.load()
    for o in range(8):
        for i in range(8):
            pxcol = px[i,o]
            #print(pxcol)
            if round(pygame.mouse.get_pos()[0]/ds) == i and round(pygame.mouse.get_pos()[1]/ds) == o:
                global oldcol
                oldcol = pxcol
            sense.set_pixel(i,o, pxcol)

def drawTaskbar():
     global oldcol
     for i in range(1):
          sense.set_pixel(i, 7, [255,204,170])
          if round(pygame.mouse.get_pos()[0]/ds) == i and round(pygame.mouse.get_pos()[1]/ds) == 7:
                oldcol = [255,204,170]
     for i in range(7):
          sense.set_pixel(i+1, 7, b)
          if round(pygame.mouse.get_pos()[0]/ds) == i and round(pygame.mouse.get_pos()[1]/ds) == 7:
                oldcol = b

def BackHome():
    global showCursor
    showCursor = 0
    ShowWallpaper()
    drawTaskbar()
    showCursor = 1

def WaitForKey():
    while True:
            key = pygame.key.get_pressed()
            if key[pygame.K_DOWN]:
                return "down"
            elif key[pygame.K_UP]:
                return "up"
            elif key[pygame.K_RETURN]:
                return "confirm"
            sleep(0.1)

def waitesc():
    while True:
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                return "esc"

def Store2disk(data, line):
    with open('s', 'r') as file:
        datas = file.readlines()


    datas[line-1] = str(data)

    # and write everything back
    with open('s', 'w') as file:
        file.writelines( datas )


def OpenCtx():
    close = 0
    optns = ["Change Wallpaper", "Close"]
    sel = 0
    while close == 0:
        #Fillscreen([100,100,100])
        #t = threading.Thread(target=showmsgthread, args=(optns[sel], 0.01, [100,100,100]))
        #t.start()
        sense.show_message(optns[sel], scroll_speed=0.02, back_colour=[100,100,100])
        Action = WaitForKey()
        sense.clear()
        print(Action)
        if Action == "down":
            if sel < 1:
                sel = sel + 1
        if Action == "up":
            if sel > 0:
                sel = sel - 1
        if Action == "confirm":
            if sel == 0:
                filenames = next(os.walk(os.getcwd()), (None, None, []))[2]
                print(filenames)
                sel2 = 0
                while close == 0:
                    #t = threading.Thread(target=showmsgthread, args=(filenames[sel2], 0.01, [100,100,100]))
                    #t.start()
                    sense.show_message(filenames[sel2], scroll_speed=0.02, back_colour=[100,100,100])
                    Action = WaitForKey()
                    sense.clear()
                    print(Action)
                    if Action == "down":
                        if sel2 < len(filenames)-1:
                            sel2 = sel2 + 1
                    if Action == "up":
                        if sel2 > 0:
                            sel2 = sel2 - 1
                    if Action == "confirm":
                        global wallpaper
                        wallpaper = filenames[sel2]
                        Store2disk(filenames[sel2], 1)
                        close = 1
            if sel == 1:
                close = 1
    global ava
    ava = 0
    BackHome()

def appMenu():
    close = 0
    filenames = next(os.walk(str(os.getcwd()) + "/apps/"), (None, None, []))[2]
    print(filenames)
    sel2 = 0
    global ava
    while close == 0:
        #t = threading.Thread(target=showmsgthread, args=(filenames[sel2], 0.01, [100,100,100]))
        #t.start()
        sense.show_message(filenames[sel2], scroll_speed=0.02, back_colour=[100,100,100])
        Action = WaitForKey()
        sense.clear()
        print(Action)
        if Action == "down":
            if sel2 < len(filenames)-1:
                sel2 = sel2 + 1
        if Action == "up":
            if sel2 > 0:
                sel2 = sel2 - 1
        if Action == "confirm":
            sense.clear()
            subprocess.run(["python", "apps/" + filenames[sel2]]) 
            waitesc()
            ava = 0
            BackHome()
            return
    ava = 0
    BackHome()

BootUp()
sense.show_message("Welcome!", scroll_speed=0.1, text_colour=[255,255,255], back_colour=[0,0,255])
BackHome()

showCursor = 1

appOpen = 0

while running:
    noAction = True
    for event in pygame.event.get():
        #print("x" + str(round(pygame.mouse.get_pos()[0]/ds)))
        #print("y" + str(round(pygame.mouse.get_pos()[1]/ds)))
        #print(pygame.mouse.get_pressed())
        try:
            #if sense.get_pixel(oldmx,oldmy) == [104,0,88]:
            if oldmx == "s":
                print("First")
            else:
                #print(sense.get_pixel(oldmx,oldmy))
                sense.set_pixel(oldmx, oldmy, oldcol)
            oldmx = round(pygame.mouse.get_pos()[0]/ds)
            oldmy = round(pygame.mouse.get_pos()[1]/ds)
            #if sense.get_pixel(oldmx,oldmy) == [0,0,0]:
            oldcol = sense.get_pixel(round(pygame.mouse.get_pos()[0]/ds),round(pygame.mouse.get_pos()[1]/ds))
            #print(oldcol)
            if showCursor == 1:
                sense.set_pixel(round(pygame.mouse.get_pos()[0]/ds),round(pygame.mouse.get_pos()[1]/ds), [255,255,255])
        except:
            #print("out of range")
            oldmx = 0
            oldmy = 0
            oldcol = sense.get_pixel(0,0)
            if showCursor == 1:
                sense.set_pixel(0,0, [255,255,255])
            #bluescreen("OOB")
        if pygame.mouse.get_pressed()[2]:
            if appOpen == 0 and ava == 0:
                print("ctx")
                t = threading.Thread(target=OpenCtx)
                t.start()
                ava = 1
                #OpenCtx()
        if pygame.mouse.get_pressed()[0]:
            if ava == 0:
                if round(pygame.mouse.get_pos()[0]/ds) == 0 and round(pygame.mouse.get_pos()[1]/ds) == 7:
                    print("apps")
                    t = threading.Thread(target=appMenu)
                    t.start()
                    #appMenu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if showCursor == 1:
                    showCursor = 0
                else:
                    showCursor = 1
            #if event.key == pygame.K_UP:
                #noAction = False
                #Action = "up"
            screen.fill(col)
            pygame.display.flip()
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
