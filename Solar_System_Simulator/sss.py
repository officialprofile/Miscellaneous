import  pygame
import math

pygame.init()

WIDTH, HEIGHT = 1500, 900
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
        self.distance_to_sun = 0
        
        self.orbit = []

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH/2
                y = y * self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 1)
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        F = self.G*self.mass*other.mass/distance**2
        theta = math.atan2(distance_y, distance_x)
        Fx = math.cos(theta)*F
        Fy = math.sin(theta)*F

        return Fx, Fy

    def update_position(self, planets):
        total_Fx = total_Fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_Fx += fx
            total_Fy += fy

        self.xv += total_Fx/self.mass*self.TIMESTEP
        self.yv += total_Fy/self.mass*self.TIMESTEP

        self.x += self.xv*self.TIMESTEP
        self.y += self.yv*self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True
    mercury = Planet(0.387*Planet.AU, 0, 8, GREY, 3.3*10**23)
    mercury.yv = -47400
    venus = Planet(0.723*Planet.AU, 0, 16, WHITE, 4.8685*10**27)
    venus.yv = -35020*1.1
    #venus = Planet(0.723*Planet.AU, 0, 14, WHITE, 4.8685*10**26)
    #venus.yv = -35020*1.1
    earth = Planet(-1*Planet.AU, 0, 16, BLUE, 5.9742*10**24)
    earth.yv = 29783
    mars  = Planet(-1.524*Planet.AU, 0, 12, RED, 6.39*10**23)
    mars.yv = 24077
    planets = [sun, earth, mars, mercury, venus]

    while run:
        clock.tick(60)
        WNDW.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WNDW)

        pygame.display.update()

    pygame.quit()

main()
