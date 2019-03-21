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
isStartPressed = 0

pygame.init()
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()


size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

startTime = time.time()

#initialize two_collide.py stuff

speed1 = [4,4]
ball1 = pygame.image.load("baby_emoji.png")
ballrect1 = ball1.get_rect()


speed2 = [2,2]
ball2 = pygame.image.load("face.png")
ballrect2 = ball2.get_rect()
ballrect2 = ballrect2.move(0,202)


# render start button
my_font = pygame.font.Font(None, 40)
start_surf = my_font.render('START', True, (255,255,255))
start_rect = start_surf.get_rect(left=5,bottom=height)

# render quit button
my_font = pygame.font.Font(None, 40)
quit_surf = my_font.render('QUIT', True, (255,255,255))
quit_rect = quit_surf.get_rect(right=width-5,bottom=height)

# render touch indicator
my_font = pygame.font.Font(None, 30)
touch_surf = my_font.render('', True, (255,255,255))
touch_rect = touch_surf.get_rect(center=(width/2,height/2))

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type is pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            touch_string = ''
            if quit_rect.collidepoint(pos):
                print('on screen quit pressed')
                exit()
                
            elif start_rect.collidepoint(pos):
                print('on screen start pressed')
                isStartPressed = 1
    
            else:
                touch_string = "TOUCH AT " + repr(pos)
                print(touch_string)
            touch_surf = my_font.render(touch_string, True, (255,255,255))
            touch_rect = touch_surf.get_rect(center=(width/2,height/2))
                
    screen.fill(black) # Erase the Work space
    
    #two_collide.py body
    if (isStartPressed):
        ballrect1 = ballrect1.move(speed1)

        if ballrect1.left < 0 or ballrect1.right > width:
            speed1[0] = -speed1[0]
            while ballrect1.left < 0 or ballrect1.right > width:
                ballrect1 = ballrect1.move(speed1)

        if ballrect1.top < 0 or ballrect1.bottom > height:
             speed1[1] = -speed1[1]
             while ballrect1.top < 0 or ballrect1.bottom > height:
                ballrect1 = ballrect1.move(speed1)


        ballrect2 = ballrect2.move(speed2)

        if ballrect2.left < 0 or ballrect2.right > width:
            speed2[0] = -speed2[0]
            while ballrect2.left < 0 or ballrect2.right > width:
                ballrect2 = ballrect2.move(speed2)
        if ballrect2.top < 0 or ballrect2.bottom > height:
            speed2[1] = -speed2[1]
            while ballrect2.top < 0 or ballrect2.bottom > height:
                ballrect2 = ballrect2.move(speed2)

        if ballrect1.colliderect(ballrect2):
            if abs(ballrect1.centerx-ballrect2.centerx) >= abs(ballrect1.centery-ballrect2.centery):
                speed1[0] = -speed1[0]
                speed2[0] = -speed2[0]
            else:
                speed1[1] = -speed1[1]
                speed2[1] = -speed2[1]
            while ballrect1.colliderect(ballrect2):
                ballrect1 = ballrect1.move(speed1)
                ballrect2 = ballrect2.move(speed2)
        screen.blit(ball1, ballrect1) 
        screen.blit(ball2, ballrect2)
                

    
    screen.blit(touch_surf, touch_rect)
    screen.blit(quit_surf, quit_rect)
    screen.blit(start_surf, start_rect)

    # Combine Ball surface with workspace surface
    pygame.display.flip() # display workspace on screen
    clock.tick(30)


    if (not GPIO.input(27)):
        exit()

    timeElapsed = time.time()-startTime
    if timeElapsed >= timeoutlimit:
        exit()
