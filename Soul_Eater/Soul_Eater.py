import pygame
import sys
import random
from pygame.math import Vector2

pygame.init()
pygame.font.init()

CELL_SIZE = 20
NUM_CELLS = 40
FPS = 60
FREQ = 100
BACKGROUND_RAW = pygame.image.load("media/bg.jpg")
BACKGROUND = pygame.transform.scale(BACKGROUND_RAW, (CELL_SIZE * NUM_CELLS, CELL_SIZE * NUM_CELLS))
SOUL_RAW = pygame.image.load("media/soul.png")
SOUL = pygame.transform.scale(SOUL_RAW, (CELL_SIZE, CELL_SIZE))
SOUND_EFFECT = pygame.mixer.Sound('media/sound_effect.wav')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, FREQ)


class Soul:
    def __init__(self):
        self.random_placement()

    def place_soul(self):
        soul_rect = pygame.Rect(self.position.x * CELL_SIZE, self.position.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        screen.blit(SOUL, soul_rect)
        #pygame.draw.rect(screen, pygame.Color('white') , soul_rect)

    def random_placement(self):
        self.x = random.randint(0, NUM_CELLS - 1)
        self.y = random.randint(0, NUM_CELLS - 1)
        self.position = Vector2(self.x, self.y)

class Eater:
    def __init__(self):
        self.body = [Vector2(4, 10), Vector2(3, 10), Vector2(2, 10)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            rect = pygame.Rect(segment.x * CELL_SIZE, segment.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color('black'), rect)

    def move(self):
        new_body = self.body[:] if self.add_segment else self.body[:-1]
        new_body.insert(0, new_body[0] + self.direction)
        self.body = new_body[:]
        self.add_segment = False

    def soul_consumed(self):
        self.add_segment = True

class Game:
    def __init__(self):
        self.eater = Eater()
        self.soul = Soul()
        self.score = 0

    def update(self):
        self.eater.move()
        self.consumption()
        self.failure_checker()
    
    def draw_all(self):
        self.soul.place_soul()
        self.eater.draw()
        print_score = font.render("Souls eaten: "+str(self.score), False, pygame.Color('black'))
        screen.blit(print_score, (10, 5))

    def consumption(self):
        if self.soul.position == self.eater.body[0]:
            self.soul.random_placement()
            self.eater.soul_consumed()
            self.score += 1
            pygame.mixer.Sound.play(SOUND_EFFECT)
            pygame.mixer.music.stop()
    
    def failure_checker(self):   
        if not 0 <= self.eater.body[0].x < NUM_CELLS or not 0 <= self.eater.body[0].y < NUM_CELLS:
            self.game_over()
        if self.eater.body[0] in self.eater.body[1:]:
            self.game_over()

    def game_over(self):
        print("game over")



screen = pygame.display.set_mode((CELL_SIZE*NUM_CELLS, CELL_SIZE*NUM_CELLS))
pygame.display.set_caption('Soul Eater')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial Black', CELL_SIZE)
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.eater.direction != Vector2(0, 1):
                game.eater.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.eater.direction != Vector2(0, -1):
                game.eater.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.eater.direction != Vector2(1, 0):
                game.eater.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.eater.direction != Vector2(-1, 0):
                game.eater.direction = Vector2(1, 0)

    screen.fill(pygame.Color('black'))
    screen.blit(BACKGROUND, (0, 0))
    game.draw_all()
    pygame.display.flip()
    
    clock.tick(FPS)