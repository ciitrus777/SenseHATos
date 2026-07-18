from sense_emu import SenseHat
import random
from time import sleep
import pygame

ds = 100

pygame.init()

# Set up the game window
screen = pygame.display.set_mode((8*ds, 8*ds))
pygame.display.set_caption("draw")

sense =  SenseHat()

for o in range(8):
        for i in range(8):
            sense.set_pixel(i,o, [0,0,0])

#sense.show_message("hello", scroll_speed=0.1, text_colour=[0,255,0], back_colour=[0,0,0])
r = [255,0,0]
g = [0,255,0]
b = [0,0,255]
y = [255, 255, 0]
lb =[0,255,255]
m = [255, 0, 255]
w = [255, 255, 255]
m1 = [255,204,170]
m2 = [174,82,59]

running = True
oldmx = 0
oldmy = 0
oldcol = [0, 0, 0]

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

#testx = 0
#testy = 0

showCursor = 1

while running:
    for event in pygame.event.get():
        #print("x" + str(round(pygame.mouse.get_pos()[0]/ds)))
        #print("y" + str(round(pygame.mouse.get_pos()[1]/ds)))
        #print(pygame.mouse.get_pressed())
        try:
            print(sense.get_pixel(oldmx,oldmy))
            #if sense.get_pixel(oldmx,oldmy) == [104,0,88]:
            sense.set_pixel(oldmx, oldmy, oldcol)
            oldmx = round(pygame.mouse.get_pos()[0]/ds)
            oldmy = round(pygame.mouse.get_pos()[1]/ds)
            #if sense.get_pixel(oldmx,oldmy) == [0,0,0]:
            oldcol = sense.get_pixel(round(pygame.mouse.get_pos()[0]/ds),round(pygame.mouse.get_pos()[1]/ds))
            print(oldcol)
            if showCursor == 1:
                sense.set_pixel(round(pygame.mouse.get_pos()[0]/ds),round(pygame.mouse.get_pos()[1]/ds), [107,0, 94])
        except:
            print("out of range")
            bluescreen("OOB")

        try:
            if pygame.mouse.get_pressed()[0] == True:
                oldcol = col
                #sense.set_pixel(round(pygame.mouse.get_pos()[0]/ds),round(pygame.mouse.get_pos()[1]/ds), col)
        except:
            print("out of range")
            bluescreen("OOB")
        if pygame.mouse.get_pressed()[1] == True:
            oldcol = [0, 0, 0]
            for o in range(8):
                for i in range(8):
                    if i != oldmx and o != oldmy:
                        sense.set_pixel(i,o, [0,0,0])
        
        if pygame.mouse.get_pressed()[2] == True:
            try:
                #sense.set_pixel(round(pygame.mouse.get_pos()[0]/ds), round(pygame.mouse.get_pos()[1]/ds), [0, 0, 0])
                oldcol = [0, 0, 0]
            except:
                print("out of range")
                bluescreen("OOB")
        if event.type == pygame.KEYDOWN:
              
            # checking if key "A" was pressed
            if event.key == pygame.K_1:
                col = w
            elif event.key == pygame.K_2:
                col = r
            elif event.key == pygame.K_3:
                col = g
            elif event.key == pygame.K_4:
                col = b
            elif event.key == pygame.K_5:
                col = y
            elif event.key == pygame.K_6:
                col = lb
            elif event.key == pygame.K_7:
                col = m
            elif event.key == pygame.K_8:
                col = m1
            elif event.key == pygame.K_9:
                col = m2
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_q:
                oldcol = col
                for o in range(8):
                    for i in range(8):
                        sense.set_pixel(i,o, col)
            elif event.key == pygame.K_e:
                if showCursor == 1:
                    showCursor = 0
                else:
                    showCursor = 1
            screen.fill(col)
            pygame.display.flip()
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()


"""
while True:
    for o in range(8):
        for i in range(8):
            rand = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
            sense.set_pixel(i,o, rand)
    sleep(0.1)
"""

