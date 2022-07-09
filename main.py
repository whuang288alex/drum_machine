from ast import In
from multiprocessing.dummy import active_children
from pydoc import cli
import click
from matplotlib import colors
from matplotlib.pyplot import draw
import pygame
from pygame import mixer

WIDTH = 1400
HEIGHT = 800

pygame.init()
screen  = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Beat Maker')
label_font = pygame.font.Font('freesansbold.ttf', 30)
medium_font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()


black = (0,0,0)
white = (255,255,255)
gray = (128,128,128) 
dark_gray = (100,100,100)
green = (0,255,0)
gold =(212, 175, 55)
blue = (0, 255,255)


fps = 60
beats = 8   
instruments = 6
boxes = []
clicked = [[-1 for i in range(beats)]for j in range(instruments)]
bpm = 240
playing = True
beat_changed  = True
active_beat = 0
active_length = 0

hi_hat = mixer.Sound('sounds\hi_hat.WAV')
snare = mixer.Sound('sounds\snare.WAV')
kick = mixer.Sound('sounds\kick.WAV')
crash = mixer.Sound('sounds\crash.WAV')
clap = mixer.Sound('sounds\clap.WAV')
tom = mixer.Sound('sounds\\tom.WAV')
pygame.mixer.set_num_channels(instruments*3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0 :
                hi_hat.play()
            if i == 1:
                snare.play()
            if i == 2 :
                kick.play()
            if i == 3 :
                crash.play()
            if i == 4 :
                clap.play()
            if i == 5 :
                tom.play()
        

def draw_grid(clicks, beat):
    
    boxes =[]
    colors = [gray, white, gray]
    left_box_width = 200
    bottom_box_height = 200
    
 
    left_box = pygame.draw.rect(screen, gray, [0, 0, left_box_width, HEIGHT - bottom_box_height], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - bottom_box_height, WIDTH, bottom_box_height], 5)  
   
    
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (30,30))
    
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (30,130))
    
    kick_text = label_font.render('Bass', True, white)
    screen.blit(kick_text, (30,230))
    
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (30,330))
    
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (30,430))
    
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (30,530))
    
    for i in range(1, instruments):
        pygame.draw.line(screen, gray, (0, i*100) , (left_box_width, i*100), 3)
        
    for i in range(instruments):
        for j in range(beats):
            if clicks[i][j] == -1:
                color = gray
            else:
                color = green
            rect = pygame.draw.rect(screen, color, 
            [j*((WIDTH -200)//beats)+205, i * 100 +5, (WIDTH -200)//beats - 10, (HEIGHT -200)//instruments - 10],
            0, 3)
            frame1 = pygame.draw.rect(screen, gold, 
            [j*((WIDTH -200)//beats)+200, i*100, (WIDTH -200)//beats, (HEIGHT -200)//instruments],
            5, 5)
            frame2 = pygame.draw.rect(screen, black, 
            [j*((WIDTH -200)//beats)+200, i*100, (WIDTH -200)//beats, (HEIGHT -200)//instruments],
            2, 5)
            boxes.append((rect, (i, j)))
    active = pygame.draw. rect(screen, blue, [beat* (WIDTH -200)//beats + 200, 0, (WIDTH -200)//beats, instruments * 100], 5, 3)
    return boxes

run = True

while run:
    
    timer.tick(fps)
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)
    
    # Play/Pause Button
    play_pause_button = pygame.draw.rect(screen, dark_gray, [50, HEIGHT - 150, 200, 100], 0, 5)
    play_pause_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_pause_text, (70, HEIGHT - 130))
    if playing:
        play_text = medium_font.render('Playing', True, black)
    else:
        play_text = medium_font.render('Paused', True, black) 
    screen.blit(play_text, (70, HEIGHT - 100))
     
    #Speed Adjustments
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT - 150, 200, 100], 5, 5)
    bpm_text1 = medium_font.render('Beats Per Minute', True, white)
    bpm_text2 = label_font.render(str(bpm), True, white)
    screen.blit(bpm_text1, (308, HEIGHT - 130))
    screen.blit(bpm_text2, (308, HEIGHT - 100))
    
    bpm_up = pygame.draw.polygon(screen, gray, [ (530, HEIGHT - 130),(510, HEIGHT - 110), (550, HEIGHT - 110) ], 0)
    bpm_down = pygame.draw.polygon(screen, gray, [(530, HEIGHT - 70),(510, HEIGHT - 90), (550, HEIGHT - 90) ], 0)
    
    # Beats Adjustments
    beats_rect = pygame.draw.rect(screen, gray, [600, HEIGHT - 150, 200, 100], 5, 5)
    beats_text1 = medium_font.render('Beats Number', True, white)
    beats_text2 = label_font.render(str(beats), True, white)
    screen.blit(beats_text1, (608, HEIGHT - 130))
    screen.blit(beats_text2, (608, HEIGHT - 100))
    beats_up = pygame.draw.polygon(screen, gray, [ (830, HEIGHT - 130),(810, HEIGHT - 110), (850, HEIGHT - 110) ], 0)
    beats_down = pygame.draw.polygon(screen, gray, [(830, HEIGHT - 70),(810, HEIGHT - 90), (850, HEIGHT - 90) ], 0)
    
    #Delete a certain column of beats
    delete_rect = pygame.draw.rect(screen, gray, [1100, HEIGHT - 150, 200, 100], 5, 5)
    delete_text1 = medium_font.render('Delete a Column', True, white)
    screen.blit(delete_text1, (1108, HEIGHT - 130))


    # Manage Sound   
    if beat_changed:
        play_notes()
        beat_changed = False
    
    # Manage Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                #event.pos is where the mouse was clicked
                if boxes[i][0].collidepoint(event.pos):
                    row,  column = boxes[i][1]
                    clicked[row][column] *= -1
        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause_button.collidepoint(event.pos): 
                if playing:
                    playing = False
                else:
                    playing = True
            if bpm_up.collidepoint(event.pos): 
                bpm += 5
            if bpm_down.collidepoint(event.pos):
                bpm -= 5
            if beats_up.collidepoint(event.pos): 
                beats += 1
                for i in range(instruments):
                    clicked[i].append(-1) 
            if beats_down.collidepoint(event.pos):
                beats -= 1
                for i in range(instruments):
                    del clicked[i][-1]
            
    
    # Manage Play                
    beat_length = (60 * fps) // bpm #how many time the loop should round before it switches to the next beat
    if playing:
       if active_length < beat_length: 
           active_length += 1
       else:
           active_length = 0
           if active_beat < beats -1:
               active_beat += 1
               beat_changed  = True
           else:
               active_beat = 0
               beat_changed = True
           
    #put everything on the screen
    pygame.display.flip()
    
pygame.quit()
