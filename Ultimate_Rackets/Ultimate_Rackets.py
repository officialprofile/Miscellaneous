import pygame
import sys
from pygame.math import Vector2

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Arial Narrow', 300)
clock = pygame.time.Clock()

FPS = 120
WIDTH = 800
HEIGHT = 600
BALL_SIZE = 20
RACKET = 100
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ultimate Rackets')

class Ball:
    def __init__(self):
        self.position = Vector2(HEIGHT/2 - BALL_SIZE, WIDTH/2 - BALL_SIZE)
        self.direction = Vector2(1, 1)

    def animate(self):
        ball = pygame.Rect(self.position.x, self.position.y, BALL_SIZE, BALL_SIZE)
        pygame.draw.rect(screen, pygame.Color('white'), ball)
        self.position += self.direction

    def check_collision(self):
        if self.position.x < 0:
            self.direction.x *= -1
            score['player2'] += 1
        elif self.position.x > WIDTH - BALL_SIZE:
            self.direction.x *= -1
            score['player1'] += 1
        elif self.position.x - BALL_SIZE == player1.position.x and player1.position.y <= self.position.y <= player1.position.y + RACKET:
            self.direction.x *= -1
        elif self.position.x + BALL_SIZE == player2.position.x and player2.position.y <= self.position.y <= player2.position.y + RACKET:
            self.direction.x *= -1
        elif self.position.y < 0 or self.position.y > HEIGHT - BALL_SIZE:
            self.direction.y *= -1

class Player:
    def __init__(self, opponent = False):
        self.position = Vector2(BALL_SIZE, HEIGHT/2 - RACKET/2) if not opponent else Vector2(WIDTH - 2*BALL_SIZE, HEIGHT/2 - RACKET/2)

    def draw(self):
        player = pygame.Rect(self.position.x, self.position.y, BALL_SIZE, RACKET)
        pygame.draw.rect(screen, pygame.Color('gold'), player)
    
    def update(self, event, opponent):
        if opponent:
            if event == pygame.K_UP:
                self.position.y -= 20
            elif event == pygame.K_DOWN:
                self.position.y += 20
        else:
            if event == pygame.K_w:
                self.position.y -= 20
            elif event == pygame.K_s:
                self.position.y += 20

score = {'player1':0, 'player2':0}
ball = Ball()
player1 = Player()
player2 = Player(opponent = True)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2.update(event.key, opponent = True)
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1.update(event.key, opponent = False)
    
    screen.fill((10, 21, 32))
    print_score = font.render(str(score['player1'])+" : "+str(score['player2']), False, (17, 35, 54))
    screen.blit(print_score, (WIDTH/2 - 200, HEIGHT/2 - 100))
    player1.draw()
    player2.draw()
    ball.check_collision()
    ball.animate()
    pygame.display.flip()
    clock.tick(FPS)