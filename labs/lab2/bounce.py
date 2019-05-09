# jfs9
# pa394/md848 - added framerate cap

import RPi.GPIO as GPIO
import pygame # Import pygame graphics library
import os # for OS calls
import time

os.putenv('SDL_VIDEODRIVER', 'fbcon') # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1') 
#os.putenv('SDL_FBDEV', '/dev/fb0') 

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

pygame.init()

clock = pygame.time.Clock()


size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

speed = [2,2]
ball = pygame.image.load("baby_emoji.png")
ballrect = ball.get_rect()

startTime = time.time()

while True:
    ballrect = ballrect.move(speed)

    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black) # Erase the Work space
    screen.blit(ball, ballrect) # Combine Ball surface with workspace surface
    pygame.display.flip() # display workspace on screen
    clock.tick(30)


    if (not GPIO.input(27)):
        exit()

    timeElapsed = time.time()-startTime
    if timeElapsed >= 30:
        exit()
