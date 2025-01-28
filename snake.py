import pygame
import random
import time
#initialising and setting up display window
pygame.init()
xwindow = 1280
ywindow = 720
screen = pygame.display.set_mode((xwindow,ywindow))
clock = pygame.time.Clock()
running  = True
speed = 15
dt = 0
#initial positions and settings for the snake and the fruit
snake_pos = [xwindow/2,ywindow/2]
snake_body=[[xwindow/2,ywindow/2],[(xwindow/2)-20,(ywindow/2)-20],[(xwindow/2)-40,(ywindow/2)-40]]
fruit_pos = [random.randrange(25, (xwindow-25)),random.randrange(25,(ywindow-25))]
fruit_spawn = True
dir = "RIGHT"
change = dir
score = 0

def show_start_screen():
    screen.fill("black")  # Background color

    # Display the title
    title_font = pygame.font.SysFont('arial', 60)
    title_surface = title_font.render("Snake Game", True, "white")
    title_rect = title_surface.get_rect(center=(xwindow / 2, ywindow / 4))
    screen.blit(title_surface, title_rect)

    # Display the controls
    controls_font = pygame.font.SysFont('arial', 30)
    controls_text = [
        "Use arrow keys to move the snake",
        "Press SPACE to start the game",
        "Press ESC to quit",
    ]
    for i, text in enumerate(controls_text):
        controls_surface = controls_font.render(text, True, "white")
        controls_rect = controls_surface.get_rect(center=(xwindow / 2, ywindow / 2 + i * 40))
        screen.blit(controls_surface, controls_rect)

    # Display a prompt to start
    prompt_font = pygame.font.SysFont('arial', 25)
    prompt_surface = prompt_font.render("Press SPACE to Start!", True, "yellow")
    prompt_rect = prompt_surface.get_rect(center=(xwindow / 2, ywindow - 100))
    screen.blit(prompt_surface, prompt_rect)

    # Update the display
    pygame.display.flip()

    # Wait for user input to start the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:  # Start game
                return
            if keys[pygame.K_ESCAPE]:  # Quit game
                pygame.quit()
                quit()


def show_score(choice, color, font, size):
    #creates font of given type and size
    score_font = pygame.font.SysFont(font, size)
    #creates surface for text
    score_surf = score_font.render("Score: "+str(score), True, color)
    score_rect = score_surf.get_rect()
    #displays text by copying surface to given location
    screen.blit(score_surf, score_rect)

def reset_game():
    global snake_pos, snake_body, fruit_pos, fruit_spawn, dir, change, score, running
    snake_pos = [xwindow/2,ywindow/2]
    snake_body = [[xwindow/2,ywindow/2],[(xwindow/2)-20,(ywindow/2)-20],[(xwindow/2)-40,(ywindow/2)-40]]
    fruit_pos = [random.randrange(25, (xwindow-25)),random.randrange(25,(ywindow-25))]
    fruit_spawn = True
    dir = 'RIGHT'
    change = dir
    score = 0
    running = True

def game_over():
    #creates font of given type and size
    game_over_font = pygame.font.SysFont('arial', 80)
    #creates surface for text
    game_over_surf = game_over_font.render("GAME OVER", True, 'red')
    game_over_rect = game_over_surf.get_rect()
    #alligns the surface
    game_over_rect.midtop = (xwindow/2,ywindow/4)
    #displays the text by copying the surface to given location
    screen.blit(game_over_surf, game_over_rect)
    # Display the controls
    controls_font = pygame.font.SysFont('arial', 30)
    controls_text = [
        "Use arrow keys to move the snake",
        "Press SPACE to start the game",
        "Press ESC to quit",
    ]
    for i, text in enumerate(controls_text):
        controls_surface = controls_font.render(text, True, "white")
        controls_rect = controls_surface.get_rect(center=(xwindow / 2, ywindow / 2 + i * 40))
        screen.blit(controls_surface, controls_rect)

    #shows score
    show_score(1,'black','times new roman',20)
    pygame.display.flip()
    running = False
    #restart game
    replay_game()

#function to restart or exit game
def replay_game():
    global snake_pos, snake_body, fruit_pos, fruit_spawn, dir, change, score, running
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            
            #press spacebar to restart
            if keys[pygame.K_SPACE]:
                reset_game()
                return
            
            #press escape to quit
            if keys[pygame.K_ESCAPE]:
                pygame.quit()
                quit()

show_start_screen()
reset_game()
while running:
    #event handling loop
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running  = False
        #checks which key has been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            change = 'UP'
        if keys[pygame.K_DOWN]:
            change = 'DOWN'
        if keys[pygame.K_LEFT]:
            change = 'LEFT'
        if keys[pygame.K_RIGHT]:
            change = 'RIGHT'
    
    #makes sure the snake moves in one direction at a time
    if change=='UP' and dir!='DOWN':
        dir = 'UP'
    if change=='DOWN' and dir!='UP':
        dir = 'DOWN'
    if change=='LEFT' and dir!='RIGHT':
        dir = 'LEFT'
    if change=='RIGHT' and dir!='LEFT':
        dir = 'RIGHT'
    
    #moves the snake
    if dir=='UP':
        snake_pos[1] -=20
    if dir=='DOWN':
        snake_pos[1]+=20
    if dir=='LEFT':
        snake_pos[0]-=20
    if dir=='RIGHT':
        snake_pos[0]+=20
    
    #growing the snake
    snake_body.insert(0,list(snake_pos))
    if abs(snake_pos[0] - fruit_pos[0]) < 20 and abs(snake_pos[1] - fruit_pos[1]) < 20:
        #eat_sound.play()        
        score+=1
        fruit_spawn=False
    else:
        snake_body.pop()
    
    #spawning fruit at random location
    if not fruit_spawn:
        fruit_pos = [random.randrange(25, (xwindow-25)),random.randrange(25,(ywindow-25))]
    fruit_spawn = True
    
    screen.fill("green")
    
    #drawing the snake
    for pos in snake_body:
        pygame.draw.rect(screen, 'black', pygame.Rect(pos[0], pos[1], 20, 20))
    
    #drawing the fruit
    pygame.draw.rect(screen, 'red', pygame.Rect(fruit_pos[0], fruit_pos[1], 20, 20))
    
    #checks if snake collided with walls and ends the game if it has
    if not (20<snake_pos[0]<(xwindow-20)) or not (20<snake_pos[1]<(ywindow-20)):
        #game_over_sound.play()
        game_over()

    
    #checks if the snake collided with itself
    for block in snake_body[1:]:
        if abs(snake_pos[0] - block[0]) < 20 and abs(snake_pos[1] - block[1]) < 20:
            game_over()
    
    #shows score
    show_score(1,'black','times new roman',20)
    pygame.display.flip()
    dt = clock.tick(speed)
pygame.quit()
