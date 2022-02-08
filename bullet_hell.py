#-------------------------------------------------------------------------------
# Name:        Bullet Hell Test
# Purpose:     Pass time while bored in Zoom meeting w/ boss
#
# Author:      Zman350x
#
# Created:     03/02/2022
# Copyright:   (c) STREAMWORKS Studios 2022
# Licence:     none
#-------------------------------------------------------------------------------
import pygame, math, time, random
pygame.init()

screen = pygame.display.set_mode((500, 500), flags=pygame.SCALED|pygame.RESIZABLE)
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()

LIGHT_GRAY = 200,200,200
DARK_GRAY = 100,100,100
RED = 200,0,0
GREEN = 0,200,0
PURPLE = 150,0,200
BLACK = 0,0,0

class HealthBar:
    def __init__(self):
        self.x = 15
        self.y = 455
        self.health = 10

        self.size = 200, 30
        self.surface = pygame.Surface(self.size)

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x-5, self.y-5, self.size[0]+10, self.size[1]+10))
        self.surface.fill(RED)
        pygame.draw.rect(self.surface, GREEN, (0, 0, self.health*20, 30))
        screen.blit(self.surface, (self.x, self.y))

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xForce = 0
        self.yForce = 0

        self.horizontalAxis = 0
        self.verticalAxis = 0

        self.size = 20, 20
        self.surface = pygame.Surface(self.size)
        self.surface.fill(RED)

    def draw(self):
        screen.blit(self.surface, (self.x, self.y))
    def updatePosition(self):
        self.x += self.xForce
        self.y -= self.yForce
        self.x = clamp(self.x, 0, 480)
        self.y = clamp(self.y, 0, 480)
    def applyForce(self, xForce, yForce):
        self.xForce += xForce
        self.yForce += yForce
    def update(self):
        self.xForce += self.horizontalAxis
        self.yForce += self.verticalAxis
        self.draw()
        self.updatePosition()
        self.xForce *=0.9
        self.yForce *=0.9

class Bullet:
    instances = []
    def __init__(self):
        self.angle = random.random()*math.tau
        self.spawnRadius = 360
        self.speed = 1.6

        self.x = math.cos(self.angle)*self.spawnRadius + 250
        self.y = -math.sin(self.angle)*self.spawnRadius + 250
        self.xForce = -math.cos(self.angle + random.random() - 0.5) * self.speed
        self.yForce = -math.sin(self.angle + random.random() - 0.5) * self.speed

        self.addHorizontal = 0
        self.addVertical = 0

        self.size = 5, 5
        self.surface = pygame.Surface(self.size)
        self.surface.fill(PURPLE)

        self.time = time.time()

        Bullet.instances.append(self)

    def draw(self):
        screen.blit(self.surface, (self.x, self.y))

    def updatePosition(self):
        self.x += self.xForce
        self.y -= self.yForce
        #self.x = clamp(self.x, 0, 480)
        #self.y = clamp(self.y, 0, 480)

    def applyForce(self, xForce, yForce):
        self.xForce += xForce
        self.yForce += yForce

    def update(self):
        self.xForce += self.addHorizontal
        self.yForce += self.addVertical
        self.draw()
        self.updatePosition()

        if time.time() - self.time > 10:
            Bullet.instances.remove(self)

    def collision(self, obj):
        return pygame.Rect(self.x, self.y, self.size[0], self.size[1]).colliderect(pygame.Rect(obj.x, obj.y, obj.size[0], obj.size[1]))

def clamp(val, minVal, maxVal):
    if minVal > val: return minVal
    if maxVal < val: return maxVal
    return val

def main():
    player = Player(240, 240)
    health = HealthBar()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.verticalAxis += 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.horizontalAxis -= 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.verticalAxis -= 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.horizontalAxis += 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player.verticalAxis -= 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    player.horizontalAxis += 1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player.verticalAxis += 1
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    player.horizontalAxis -= 1

        if random.randrange(10) == 0:
            Bullet()

        screen.fill(LIGHT_GRAY)
        player.update()

        for bullet in Bullet.instances:
            bullet.update()
            if bullet.collision(player):
                health.health -= 1
                Bullet.instances.remove(bullet)

        health.draw()

        if health.health <= 0:
            font = pygame.font.Font(None, 100)
            textBitmap = font.render("GAME OVER", True, BLACK)
            screen.blit(textBitmap, (250-textBitmap.get_width()/2, 250-textBitmap.get_height()/2))
            pygame.display.update()
            clock.tick(0.5)
            pygame.quit()
            quit()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
