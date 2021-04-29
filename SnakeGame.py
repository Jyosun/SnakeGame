import random
import pygame
import sys
from pygame.locals import *

windows_width=800
windows_height=600

cell_size=20 

white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)

BG_COLOR = (137,119,173)

map_width = int(windows_width / cell_size)
map_height = int(windows_height / cell_size)

snake_speed=15

UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def main_game():
    pygame.init()
    screen=pygame.display.set_mode((windows_width,windows_height))
    pygame.display.set_caption("요순이가 만든 지렁이게임")
    snake_speed_clock = pygame.time.Clock()
    screen.fill(white)

    while True:
        run_game(screen,snake_speed_clock)
        gameover(screen)              

def run_game(screen,snake_speed_clock):
    start_x=random.randint(3,map_width-8)
    start_y=random.randint(3,map_width-8)
    snake_coords=[{'x':start_x,'y':start_y},{'x':start_x-1,'y':start_y},{'x':start_x-2,'y':start_y}]
    direction = RIGHT
    food=get_random_location()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if (event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:
                    direction=LEFT
                elif (event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        snake_move(direction,snake_coords)

        alive=snake_is_alive(snake_coords)
        if not alive:                       
            break
        snake_eat_foods(snake_coords,food)   
        screen.fill(BG_COLOR)                

        draw_snake(screen, snake_coords)
        draw_food(screen,food)
        draw_score(screen, len(snake_coords) - 3)
        pygame.display.flip()

        snake_speed_clock.tick(snake_speed) 

def snake_move(directtion,snake_coords):
    if directtion==UP:
        newHead={'x':snake_coords[0]['x'],'y':snake_coords[0]['y']-1}
    elif directtion==DOWN:
        newHead = {'x': snake_coords[0]['x'], 'y': snake_coords[0]['y'] + 1}
    elif directtion==LEFT:
        newHead = {'x': snake_coords[0]['x']-1, 'y': snake_coords[0]['y'] }
    elif directtion == RIGHT:
        newHead = {'x': snake_coords[0]['x']+1, 'y': snake_coords[0]['y']}
    snake_coords.insert(0,newHead)

def snake_is_alive(snake_coords):
    alive=True
    if snake_coords[0]['x'] == -1 or snake_coords[0]['x'] == map_width or snake_coords[0]['y'] == -1 or \
			snake_coords[0]['y'] == map_height:
        alive=False
    for snake_body in snake_coords[1:]:
        if snake_coords[0]['x']==snake_body['x'] and snake_coords[0]['y']==snake_body['y']:
            alive=False
    return alive

def snake_eat_foods(snake_coords,food):
    if snake_coords[0]['x']==food['x'] and snake_coords[0]['y']==food['y']:
        food['x']=random.randint(0, map_width-1)
        food['y']=random.randint(0, map_height-1)
    else:
        del snake_coords[-1]

def get_random_location():
    return {'x':random.randint(0,map_width-1),'y':random.randint(0,map_height-1)}

def draw_snake(screen, snake_coords):
    for coord in snake_coords:
        x=coord['x']*cell_size
        y=coord['y']*cell_size
        segmentRect=pygame.Rect(x,y,cell_size,cell_size)
        pygame.draw.rect(screen,blue,segmentRect)

def draw_food(screen,food):
    x=food['x']*cell_size
    y=food['y']*cell_size

    foodRect=pygame.Rect(x,y,cell_size,cell_size)
    pygame.draw.rect(screen,dark_blue,foodRect)

def draw_grid(screen):
    for x in range(0,windows_width,cell_size):
        pygame.draw.line(screen,gray,(x,0),(x,windows_height))
    for y in range(0,windows_height,cell_size):
        pygame.draw.line(screen,gray,(0,y),(windows_width,y))
def draw_score(screen, score):
    font = pygame.font.SysFont(None, 40)
    score_str = "{:,}".format(score)
    score_image=font.render('Score: '+score_str,True,black)
    score_rect=score_image.get_rect()

    score_rect.topleft=(windows_width-200,10)
    screen.blit(score_image, score_rect)

def gameover(screen):
    font=pygame.font.SysFont(None, 40)
    tips=font.render('Game Over! Press anykey to continue~~~~~',True, (255, 212, 0))
    screen.blit(tips,(80, 300))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    return

if __name__=='__main__':
    main_game()