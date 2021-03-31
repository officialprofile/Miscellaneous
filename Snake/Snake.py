import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()
pygame.font.init()

CELL_SIZE = 20
NUM_CELLS = 30
FPS = 60
FREQ = 100
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

BORDER_UL = pygame.image.load("img/border_ul.png")
BORDER_UR = pygame.image.load("img/border_ur.png")
BORDER_BL = pygame.image.load("img/border_bl.png")
BORDER_BR = pygame.image.load("img/border_br.png")
BORDER_U = pygame.image.load("img/border_u.png")
BORDER_L = pygame.image.load("img/border_l.png")
BORDER_R = pygame.image.load("img/border_r.png")
BORDER_B = pygame.image.load("img/border_b.png")
GRASS_1 = pygame.image.load("img/grass_1.png")
GRASS_2 = pygame.image.load("img/grass_2.png")

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
        self.body = [Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            rect = pygame.Rect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color('white'), rect)

    def move(self):
        new_body = self.body[:] if self.add_segment else self.body[:-1]
        new_body.insert(0, new_body[0] + self.direction)
        self.body = new_body[:]
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
        if not 0 <= self.snake.body[0].x < NUM_CELLS or not 0 <= self.snake.body[0].y < NUM_CELLS:
            self.game_over()
        if self.snake.body[0] in self.snake.body[1:]:
            self.game_over()

    def game_over(self):
        print("game over")

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