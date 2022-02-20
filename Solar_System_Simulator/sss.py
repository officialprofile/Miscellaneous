import  pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 900
WNDW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulator")

BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (200, 0, 0)
GREY = (60, 60, 60)
WHITE = (230, 230, 230)


class Planet:
    AU = 149.6e6 * 1000 # * 1000 because we want meters
    G = 6.67428e-11
    SCALE = 250 / AU # 1 AU = 100 px
    TIMESTEP = 3600*24 # 1 day
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.xv = 0
        self.yv = 0

        self.sun = False
        self.dist_to_sun = 0
        
        self.orbit = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        pygame.draw.circle(win, self.color, (x, y), self.radius)



def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True
    mercury = Planet(0.387*Planet.AU, 0, 8, GREY, 3.3*10**23)
    venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**24)
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    mars  = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WNDW.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.draw(WNDW)

        pygame.display.update()

    pygame.quit()

main()
