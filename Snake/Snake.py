import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()
pygame.font.init()

CELL_SIZE = 30
NUM_CELLS = 25
FPS = 60
FREQ = 60
#BACKGROUND_RAW = pygame.image.load("media/bg.jpg")
#BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (CELL_SIZE * NUM_CELLS, CELL_SIZE * NUM_CELLS))
APPLE_RAW = pygame.image.load("img/apple.png")
APPLE = pygame.transform.scale(APPLE_RAW, (CELL_SIZE, CELL_SIZE))
SOUND_EFFECT = pygame.mixer.Sound('music/fruit.wav')
SOUND_EFFECT_BONUS = pygame.mixer.Sound('music/fruit_bonus.wav')
SOUND_BACKGROUND = pygame.mixer.Sound('music/background_music.mp3')
SCREEN_UPDATE = pygame.USEREVENT


pygame.time.set_timer(SCREEN_UPDATE, FREQ)
screen = pygame.display.set_mode((CELL_SIZE*NUM_CELLS, CELL_SIZE*NUM_CELLS))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
font = pygame.font.Font('font/GRASSEVENT.ttf', 10*CELL_SIZE)

BORDER_UL = pygame.transform.scale(pygame.image.load("img/border_ul.png"), (CELL_SIZE, CELL_SIZE))
BORDER_UR = pygame.transform.scale(pygame.image.load("img/border_ur.png"), (CELL_SIZE, CELL_SIZE))
BORDER_BL = pygame.transform.scale(pygame.image.load("img/border_bl.png"), (CELL_SIZE, CELL_SIZE))
BORDER_BR = pygame.transform.scale(pygame.image.load("img/border_br.png"), (CELL_SIZE, CELL_SIZE))
BORDER_U = pygame.transform.scale(pygame.image.load("img/border_u.png"), (CELL_SIZE, CELL_SIZE))
BORDER_L = pygame.transform.scale(pygame.image.load("img/border_l.png"), (CELL_SIZE, CELL_SIZE))
BORDER_R = pygame.transform.scale(pygame.image.load("img/border_r.png"), (CELL_SIZE, CELL_SIZE))
BORDER_B = pygame.transform.scale(pygame.image.load("img/border_b.png"), (CELL_SIZE, CELL_SIZE))
GRASS_1 = pygame.transform.scale(pygame.image.load("img/grass_1.png"), (CELL_SIZE, CELL_SIZE))
GRASS_2 = pygame.transform.scale(pygame.image.load("img/grass_2.png"), (CELL_SIZE, CELL_SIZE))

class Fruit:
    def __init__(self):
        self.random_placement()

    def place_fruit(self):
        apple_rect = pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(APPLE, apple_rect)
        #pygame.draw.rect(screen, pygame.Color('white') , apple_rect)

    def random_placement(self):
        self.x = random.randint(1, NUM_CELLS - 2)
        self.y = random.randint(1, NUM_CELLS - 2)
        self.position = Vector2(self.x, self.y)

class Snake:
    def __init__(self):
        self.orientation_dict = {(1, 0):'L', (-1, 0): 'R', (0, 1): 'B', (0, -1): 'U'}
        self.body = [Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.direction = Vector2(1, 0)
        self.segments_orientation = ['L', 'L', 'L']
        self.add_segment = False

        self.head_up = pygame.transform.scale(pygame.image.load('img/face_up.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.head_down = pygame.transform.scale(pygame.image.load('img/face_down.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.head_left = pygame.transform.scale(pygame.image.load('img/face_left.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.head_right = pygame.transform.scale(pygame.image.load('img/face_right.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))

        self.tail_up = pygame.transform.scale(pygame.image.load('img/tail_up.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.tail_bottom = pygame.transform.scale(pygame.image.load('img/tail_down.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.tail_left = pygame.transform.scale(pygame.image.load('img/tail_left.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.tail_right = pygame.transform.scale(pygame.image.load('img/tail_right.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))

        self.body_ver = pygame.transform.scale(pygame.image.load('img/vertical.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.body_hor = pygame.transform.scale(pygame.image.load('img/horizontal.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))

        self.body_bl = pygame.transform.scale(pygame.image.load('img/corner_bl.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.body_br = pygame.transform.scale(pygame.image.load('img/corner_br.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.body_ul = pygame.transform.scale(pygame.image.load('img/corner_ul.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))
        self.body_ur = pygame.transform.scale(pygame.image.load('img/corner_ur.png').convert_alpha(), (CELL_SIZE, CELL_SIZE))


    def draw(self):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            if i == 0:
                if self.segments_orientation[i] == 'U':
                    screen.blit(self.head_up, rect)
                elif self.segments_orientation[i] == 'B':
                    screen.blit(self.head_down, rect)
                elif self.segments_orientation[i] == 'R':
                    screen.blit(self.head_right, rect)
                elif self.segments_orientation[i] == 'L':
                    screen.blit(self.head_left, rect)
            elif 0 < i < len(self.body) - 1:
                if self.segments_orientation[i-1] == self.segments_orientation[i]:
                    if self.segments_orientation[i-1] == 'U' or self.segments_orientation[i-1] == 'B':
                        screen.blit(self.body_ver, rect)
                    else:
                        screen.blit(self.body_hor, rect)
                else:
                    if self.segments_orientation[i-1] == 'U' and self.segments_orientation[i] == 'L':
                        screen.blit(self.body_ul, rect)
                    elif self.segments_orientation[i-1] == 'U' and self.segments_orientation[i] == 'R':
                        screen.blit(self.body_ur, rect)
                    elif self.segments_orientation[i-1] == 'B' and self.segments_orientation[i] == 'L':
                        screen.blit(self.body_bl, rect)
                    elif self.segments_orientation[i-1] == 'B' and self.segments_orientation[i] == 'R':
                        screen.blit(self.body_br, rect)
                    elif self.segments_orientation[i-1] == 'R' and self.segments_orientation[i] == 'U':
                        screen.blit(self.body_bl, rect)
                    elif self.segments_orientation[i-1] == 'R' and self.segments_orientation[i] == 'B':
                        screen.blit(self.body_ul, rect)
                    elif self.segments_orientation[i-1] == 'L' and self.segments_orientation[i] == 'U':
                        screen.blit(self.body_br, rect)
                    elif self.segments_orientation[i-1] == 'L' and self.segments_orientation[i] == 'B':
                        screen.blit(self.body_ur, rect)
        
            elif i == len(self.body) - 1:
                if self.segments_orientation[i-1] == 'R':
                    screen.blit(self.tail_left, rect)
                elif self.segments_orientation[i-1] == 'L':
                    screen.blit(self.tail_right, rect)
                elif self.segments_orientation[i-1] == 'U':
                    screen.blit(self.tail_up, rect)
                elif self.segments_orientation[i-1] == 'B':
                    screen.blit(self.tail_bottom, rect)
            else:
                pygame.draw.rect(screen, (200, 200, 200), rect)    

    def move(self):
        new_body = self.body[:] if self.add_segment else self.body[:-1]
        new_body.insert(0, new_body[0] + self.direction)
        self.body = new_body[:]

        new_segments_orientation = self.segments_orientation[:] if self.add_segment else self.segments_orientation[:-1]
        self.segments_orientation = [self.orientation_dict[(self.direction[0], self.direction[1])]] + new_segments_orientation        
        self.add_segment = False

    def fruit_consumed(self):
        self.add_segment = True

class Game:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0

    def update(self):
        self.snake.move()
        self.consumption()
        self.failure_checker()

    def draw_background(self):
        screen.fill(pygame.Color('black'))
    
        for w in range(NUM_CELLS):
            for h in range(NUM_CELLS):
                if w == 0 and h == 0:
                    screen.blit(BORDER_UL, (w*CELL_SIZE, h*CELL_SIZE)) 
                elif w == NUM_CELLS - 1 and h == 0:
                    screen.blit(BORDER_UR, (w*CELL_SIZE, h*CELL_SIZE)) 
                elif w == 0 and h == NUM_CELLS - 1:
                    screen.blit(BORDER_BL, (w*CELL_SIZE, h*CELL_SIZE))
                elif w == NUM_CELLS - 1 and h == NUM_CELLS - 1:
                    screen.blit(BORDER_BR, (w*CELL_SIZE, h*CELL_SIZE))
                elif w == 0 and 0 < h < NUM_CELLS - 1:
                    screen.blit(BORDER_L, (w*CELL_SIZE, h*CELL_SIZE))
                elif w == NUM_CELLS - 1 and 0 < h < NUM_CELLS - 1:
                    screen.blit(BORDER_R, (w*CELL_SIZE, h*CELL_SIZE))
                elif 0 < w < NUM_CELLS - 1 and h == 0:
                    screen.blit(BORDER_U, (w*CELL_SIZE, h*CELL_SIZE))
                elif 0 < w < NUM_CELLS - 1 and h == NUM_CELLS - 1:
                    screen.blit(BORDER_B, (w*CELL_SIZE, h*CELL_SIZE))
                else:
                    screen.blit(GRASS_2 if (w+h)%2 else GRASS_1, (w*CELL_SIZE, h*CELL_SIZE)) 
    
    def draw_all(self):
        self.draw_background()
        print_score = font.render(str(self.score), False, (60, 180, 60))
        score_rect = print_score.get_rect(center = (NUM_CELLS*CELL_SIZE/2, NUM_CELLS*CELL_SIZE/2))
        screen.blit(print_score, score_rect)

        self.fruit.place_fruit()
        self.snake.draw()

    def consumption(self):
        if self.fruit.position == self.snake.body[0]:
            self.fruit.random_placement()
            self.snake.fruit_consumed()
            self.score += 1
            pygame.mixer.find_channel(True).play(SOUND_EFFECT if self.score%10 != 0 else SOUND_EFFECT_BONUS) 
            pygame.mixer.music.stop()
    
    def failure_checker(self):   
        if not 1 <= self.snake.body[0].x < NUM_CELLS - 1 or not 1 <= self.snake.body[0].y < NUM_CELLS - 1:
            self.game_over()
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        self.snake.body = [Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.snake.direction = Vector2(1, 0)
        self.snake.segments_orientation = ['L', 'L', 'L']
        self.score = 0

game = Game()
pygame.mixer.find_channel(True).play(SOUND_BACKGROUND, loops = -1) 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)
 
    game.draw_all()
    pygame.display.flip()
    
    clock.tick(FPS)