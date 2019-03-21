# jfs9
# pa394/md848 - added framerate cap

import RPi.GPIO as GPIO
import pygame # Import pygame graphics library
import os # for OS calls
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
# os.putenv('SDL_FBDEV', '/dev/fb0') 

pygame.init()

clock = pygame.time.Clock()


size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

speed1 = [2,2]
ball1 = pygame.image.load("baby_emoji.png")
ballrect1 = ball1.get_rect()


speed2 = [1,1]
ball2 = pygame.image.load("face.png")
ballrect2 = ball2.get_rect()

startTime = time.time()

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    ballrect1 = ballrect1.move(speed1)

    if ballrect1.left < 0 or ballrect1.right > width:
        speed1[0] = -speed1[0]
    if ballrect1.top < 0 or ballrect1.bottom > height:
        speed1[1] = -speed1[1]


    ballrect2 = ballrect2.move(speed2)

    if ballrect2.left < 0 or ballrect2.right > width:
        speed2[0] = -speed2[0]
    if ballrect2.top < 0 or ballrect2.bottom > height:
        speed2[1] = -speed2[1]


    screen.fill(black) # Erase the Work space
    screen.blit(ball1, ballrect1) 
    screen.blit(ball2, ballrect2)
    # Combine Ball surface with workspace surface
    pygame.display.flip() # display workspace on screen
    clock.tick(30)


    if (not GPIO.input(27)):
        exit()

    timeElapsed = time.time()-startTime
    if timeElapsed >= 30:
        exit()
