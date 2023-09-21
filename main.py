import pygame
import random
import sys
import cv2
from cvzone.HandTrackingModule import HandDetector

pygame.init()

clock = pygame.time.Clock()
fps = 30

#camera setup
cam = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=.8, maxHands=1)

HEIGHT  = 700#500
WIDTH = 400#300

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Wala FlAppY Bird")
pygame.display.update()

#welcome screen
background = pygame.image.load('background.png').convert()
welcome_screen = pygame.image.load('welcome.png').convert_alpha()
def welcome():
    screen.blit(welcome_screen,(0,0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        state, frame= cam.read()
        hands,img = detector.findHands(frame)
        if hands:
            lmList=hands[0]
            hey= detector.fingersUp(lmList)
            if hey ==[1,1,1,1,1]:
                game_loop()
        pygame.display.update()



def game_loop():
    #import image
    floor = pygame.image.load('ground.png').convert_alpha()
    bird = pygame.image.load('bird0.png').convert_alpha()
    bird_rect = bird.get_rect(center=(50,300))
    top_pipe=pygame.image.load('top_3.png').convert_alpha()
    bottom_pipe=pygame.image.load('bottom_3.png').convert_alpha()
    restart_img = pygame.image.load('over_final.png').convert()

    pipe_create = pygame.USEREVENT
    pygame.time.set_timer(pipe_create,1200)

    def gameover(pipes):
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                pygame.mixer.music.load('sounds\sfx_die.wav')
                pygame.mixer.music.play()
                return True
            if bird_rect.bottom >= 600 or bird_rect.top <= 0:
                pygame.mixer.music.load('sounds\sfx_die.wav')
                pygame.mixer.music.play()
                return True
        return False
        
    def game_floor():
        screen.blit(floor,(floor_x_pos,600))
        screen.blit(floor,(floor_x_pos + 336,600))

    def draw_bird(x,y):
        screen.blit(bird,(x,y))

    def draw_bg():
        screen.blit(background,(0,0))


    def random_pipes():
        random_height = random.choice(height_pipe)
        top_pipe_rect = top_pipe.get_rect(midbottom=(400,random_height))
        bottom_pipe_rect = bottom_pipe.get_rect(midtop=(400,random_height+150))
        return top_pipe_rect,bottom_pipe_rect

    def pipe_move(pipes):
        for pipe in pipes:
            pipe.centerx -= 7
        return pipes

    def pipe_draw(pipes):
        for pipe in pipes:
            if pipe.bottom >= 350:
                screen.blit(top_pipe,pipe)
            else:
                flip_pipe = pygame.transform.flip(top_pipe,False,True)
                screen.blit(flip_pipe,pipe)

    game_exit = False
    game_over = False
    #pipe_scroll_speed= 1
    floor_x_pos = 0    
    bird_x=10
    bird_y=300
    bird_y_change = 0
    pipe_list = []
    height_pipe= [150,200,250,300]
    while not game_exit:
        game_over = gameover(pipe_list)
        if game_over:
            pygame.mixer.music.load('sounds\sfx_hit.wav')
            pygame.mixer.music.play()           
            screen.blit(restart_img,(0,0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state, frame= cam.read()
                hands,img = detector.findHands(frame)
                #cv2.imshow("Frame",frame)
                k=cv2.waitKey(1)
                if hands:
                    lmList=hands[0]
                    finger_up= detector.fingersUp(lmList)
                    if finger_up ==[1,0,0,0,0]:
                        welcome()

        else:         
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                state, frame= cam.read()
                hands,img = detector.findHands(frame)
                #cv2.imshow("Frame",frame)
                k=cv2.waitKey(1)
                if hands:
                    lmList=hands[0]
                    finger_up= detector.fingersUp(lmList)
                    if finger_up ==[0,1,0,0,0]:
                        bird_y_change=-2
                        pygame.mixer.music.load('sounds\sfx_wing.wav')
                        pygame.mixer.music.play()
                        if bird_y <=0:
                            bird_y = 0
                    else:
                        bird_y_change =+2
                        if bird_y>=600:
                            bird_y = 600
                
                if k==ord('q'):
                    break        
                
                if event.type == pipe_create:
                    pipe_list.extend(random_pipes())
                    
            
            draw_bg()

            #pipe
            pipe_list = pipe_move(pipe_list)
            pipe_draw(pipe_list)
            
            #screen.blit(top_pipe,(300,-100))
            #bird
            bird_y +=bird_y_change
            draw_bird(bird_x,bird_y)
            
            #floor
            floor_x_pos -=.5
            game_floor()
            if floor_x_pos <= -280:
                floor_x_pos = 0
            


        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    exit()
welcome()



