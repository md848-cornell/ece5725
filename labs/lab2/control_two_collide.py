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

speedFactor = 20
framerate = 30
timeoutlimit = 120
currentLevel = 1
isPaused = 1

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
ballrect2.move(0,202)


# START BUTTON
my_font = pygame.font.Font(None, 40)
start_surf = my_font.render('START', True, (255,255,255))
start_rect = start_surf.get_rect(centerx=int(2.0/8*320),bottom=height-5)

# QUIT BUTTON
my_font = pygame.font.Font(None, 40)
quit_surf = my_font.render('QUIT', True, (255,255,255))
quit_rect = quit_surf.get_rect(centerx=int(6.0/8*width),bottom=height-5)

# TOUCH TEXT
my_font = pygame.font.Font(None, 20)
touch_surf = my_font.render('', True, (255,255,255))
touch_rect = touch_surf.get_rect(center=(width/2,height/2))

# PAUSE/RESTART BUTTON
my_font = pygame.font.Font(None, 25)
pause_surf = my_font.render('PAUSE', True, (255,255,255))
pause_rect = pause_surf.get_rect(centerx=int(1.0/8*width),bottom=height-5)

# FASTER BUTTON
my_font = pygame.font.Font(None, 25)
fast_surf = my_font.render('FASTER', True, (255,255,255))
fast_rect = fast_surf.get_rect(centerx=int(3.0/8*width),bottom=height-5)

# SLOWER BUTTON
my_font = pygame.font.Font(None, 25)
slow_surf = my_font.render('SLOWER', True, (255,255,255))
slow_rect = slow_surf.get_rect(centerx=int(5.0/8*width),bottom=height-5)


# BACK BUTTON
my_font = pygame.font.Font(None, 25)
back_surf = my_font.render('BACK', True, (255,255,255))
back_rect = back_surf.get_rect(centerx=int(7.0/8*width),bottom=height-5)


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
        if event.type is pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            if currentLevel == 1:
                touch_string = ''
                if quit_rect.collidepoint(pos):
                    print('on screen quit pressed')
                    exit()
                    
                elif start_rect.collidepoint(pos):
                    print('on screen start pressed')
                    currentLevel = 2
        
                else:
                    touch_string = "TOUCH AT " + repr(pos)
                    print(touch_string)
                    
                touch_surf = my_font.render(touch_string, True, (255,255,255))
                touch_rect = touch_surf.get_rect(center=(width/2,height/2))
                
            elif currentLevel == 2:
                if pause_rect.collidepoint(pos):
                    print('on screen pause/restart pressed')
                    if isPaused:
                        pause_surf = my_font.render('RESTART', True, (255,255,255))
                        pause_rect = pause_surf.get_rect(centerx=int(1.0/8*width),bottom=height-5)
                   
                    # IF RESTART IS PRESSED
                    else:
                        pause_surf = my_font.render('PAUSE', True, (255,255,255))
                        pause_rect = pause_surf.get_rect(centerx=int(1.0/8*width),bottom=height-5)
                        
                        #speed1 = [4,4]
                        #speed2 = [2,2]
                        #ballrect1.move_ip(0,0)
                        #ballrect2.move_ip(0,202)

                        
                    isPaused = not isPaused
                        
                elif fast_rect.collidepoint(pos):
                    print('on screen faster pressed')
                    #speed1[0] *= speedFactor
                    #speed1[1] *= speedFactor
                    #speed2[0] *= speedFactor
                    #speed2[1] *= speedFactor
                    framerate += speedFactor
                    
                elif slow_rect.collidepoint(pos): 
                    print('on screen slower pressed')
                    #speed1[0] /= speedFactor
                    #speed1[1] /= speedFactor
                    #speed2[0] /= speedFactor
                    #speed2[1] /= speedFactor
                    if framerate > speedFactor:
                        framerate -= speedFactor
                    
                elif back_rect.collidepoint(pos):
                    print('on screen back pressed')
                    currentLevel = 1
                    
                    
                
                
    screen.fill(black) # Erase the Work space
    
    #two_collide.py body
    if isPaused and currentLevel == 2:
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
        
            
    if currentLevel == 1:
        screen.blit(touch_surf, touch_rect)
        screen.blit(quit_surf, quit_rect)
        screen.blit(start_surf, start_rect)
        
    elif currentLevel == 2:
        screen.blit(ball1, ballrect1) 
        screen.blit(ball2, ballrect2)

        screen.blit(pause_surf, pause_rect)
        screen.blit(fast_surf, fast_rect)
        screen.blit(slow_surf, slow_rect)
        screen.blit(back_surf, back_rect)

    # Combine Ball surface with workspace surface
    pygame.display.flip() # display workspace on screen
    clock.tick(framerate)


    if (not GPIO.input(27)):
        exit()

    timeElapsed = time.time()-startTime
    if timeElapsed >= timeoutlimit:
        exit()
