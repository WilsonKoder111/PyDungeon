__author__ = 'WilsonKoder'

# Dungeon Game by Wilson

import pygame
import random
import sys

pygame.init()

# Window Setup

windowSize = (800, 600)
window = pygame.display.set_mode(windowSize)

# Clock and FPS

clock = pygame.time.Clock()
FPS_LIMIT = 60

# Game Variables

colors = {"red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255), "white": (255, 255, 255), "black": (0, 0, 0),
          "yellow": (255, 255, 0)}

running = True

# Input

moveUp = False
moveDown = False
moveLeft = False
moveRight = False

# Player Variables

playerPosition = [400, 300]

# Projectile Class

projectiles = []
PLAYER_IMG_PATH = "res/img/player.png"
playerImage = pygame.image.load(PLAYER_IMG_PATH)
playerSpeed = 5


class Projectile:

    direction = ""
    pos = [1, 1]

    def __init__(self, dir, playerPos):
        if dir is "up" or "down" or "left" or "right":
            self.direction = dir
            print("shoot " + dir)
            self.pos = playerPos[:]

    def update_pos(self):
        if self.direction is "up":
            self.pos[1] -= 5
        elif self.direction is "down":
            self.pos[1] += 5
        elif self.direction is "left":
            self.pos[0] -= 5
        elif self.direction is "right":
            self.pos[0] += 5

# Enemy class

enemies = []
count = 0


class Enemy:
    pos = [1, 1]

    def __init__(self):
        self.pos = [random.randint(0, 799), random.randint(0, 599)]

    def match_position(self, player_pos):
        if self.pos[0] < player_pos[0]:
            self.pos[0] += 1
        else:
            self.pos[0] -= 1

        if self.pos[1] < player_pos[1]:
            self.pos[1] += 1
        else:
            self.pos[1] -= 1


def draw_enemies():
    for enemy in enemies:
        pygame.draw.circle(window, colors["green"], enemy.pos, 14, 0)


def draw_projectiles():
    for projectile in projectiles:
        position = projectile.pos
        pygame.draw.circle(window, colors["black"], position, 14, 0)


def clean_memory():
    for proj in projectiles:
        if proj.pos[0] > 800 or proj.pos[0] < -14 or proj.pos[1] < -14 or proj.pos[1] > 814:
            projectiles.remove(proj)

# collision algorthim taken from https://developer.mozilla.org/en-US/docs/Games/Techniques/2D_collision_detection


def check_projectile_collision():
    for enemy in enemies:
        for proj in projectiles:
            if enemy.pos[0] < proj.pos[0] + 28 and enemy.pos[0] + 28 > proj.pos[0] and enemy.pos[1] < proj.pos[1] + 14 and enemy.pos[1] + 14 > proj.pos[1]:
                print("shot")
                try:
                    enemies.remove(enemy)
                    projectiles.remove(proj)
                except ValueError:
                    print("oops!")


def check_player_collision():
    for enemy in enemies:
        if enemy.pos[0] < playerPosition[0] + 28 and enemy.pos[0] + 28 > playerPosition[0] and enemy.pos[1] < playerPosition[1] + 14 and enemy.pos[1] + 14 > playerPosition[1]:
            print("dead")
            pygame.quit()
            sys.exit()

# Main loop

while running:
    clock.tick(FPS_LIMIT)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # movement
            if event.key == pygame.K_w:
                moveUp = True
            elif event.key == pygame.K_s:
                moveDown = True

            if event.key == pygame.K_a:
                moveLeft = True
            elif event.key == pygame.K_d:
                moveRight = True

            if event.key == pygame.K_p:
                playerSpeed = 10

            # shooting

            if event.key == pygame.K_UP:
                proj = Projectile("up", playerPosition)
                projectiles.append(proj)
                print(len(projectiles))
            elif event.key == pygame.K_DOWN:
                proj = Projectile("down", playerPosition)
                projectiles.append(proj)

            if event.key == pygame.K_LEFT:
                proj = Projectile("left", playerPosition)
                projectiles.append(proj)
            elif event.key == pygame.K_RIGHT:
                proj = Projectile("right", playerPosition)
                projectiles.append(proj)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moveUp = False
            elif event.key == pygame.K_s:
                moveDown = False

            if event.key == pygame.K_a:
                moveLeft = False
            elif event.key == pygame.K_d:
                moveRight = False

    for projectile in projectiles:
        projectile.update_pos()

    if moveUp:
        playerPosition[1] -= int(playerSpeed)
    elif moveDown:
        playerPosition[1] += int(playerSpeed)

    if moveLeft:
        playerPosition[0] -= int(playerSpeed)
    elif moveRight:
        playerPosition[0] += int(playerSpeed)

    count += 1

    if count > 50:
        new_enemy = Enemy()
        enemies.append(new_enemy)
        count = 0

    for enemy in enemies:
        enemy.match_position(playerPosition)

    window.fill(colors["yellow"])
    check_projectile_collision()
    check_player_collision()

    # drawing code goes here

    draw_projectiles()
    draw_enemies()
    window.blit(playerImage, (playerPosition[0] - 14, playerPosition[1] - 14))
    pygame.display.flip()
    clean_memory()

pygame.quit()
sys.exit()