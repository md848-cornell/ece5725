# jfs9
# pa394/md848 - added framerate cap
# 2/28 quit button

import RPi.GPIO as GPIO
import pygame # Import pygame graphics library
import os # for OS calls
import time

if False:
    os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
    os.putenv('SDL_FBDEV', '/dev/fb1') 
    os.putenv('SDL_MOUSEDRV', 'TSLIB') # Track mouse clicks on piTFT
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')
  
  

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

timeoutlimit = 30

pygame.init()
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

startTime = time.time()

# render quit button
my_font = pygame.font.Font(None, 50)
quit_surf = my_font.render('QUIT', True, (255,255,255))
quit_rect = quit_surf.get_rect(right=width-5,bottom=height)


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type is pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos() 
            if quit_rect.collidepoint(pos):
                print('on screen quit pressed')
                exit()

    screen.fill(black) # Erase the Work space
    screen.blit(quit_surf, quit_rect)
    # Combine Ball surface with workspace surface
    pygame.display.flip() # display workspace on screen
    clock.tick(30)


    if (not GPIO.input(27)):
        exit()

    timeElapsed = time.time()-startTime
    if timeElapsed >= timeoutlimit:
        exit()
