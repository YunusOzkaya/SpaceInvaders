import random
import math
import pygame
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# background image
background = pygame.image.load("background.png")
mixer.music.load("mindgames.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Uzay İstilası", )
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# for the explosion
time_to_blit = None
explosion = pygame.image.load("explosion.png").convert()

# PLAYER
playerImg = pygame.image.load("player.png")
playerX = 368
playerY = 480
playerX_Change = 0
playerY_Change = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# ALIEN

alienImg = []
alienX = []
alienY = []
alienX_Change = []
alienY_Change = []
numsOfAllien = 6

for i in range(numsOfAllien):
    alienImg.append(pygame.image.load("alien.png"))
    alienX.append(random.randint(0, 735))
    alienY.append(random.randint(50, 150))
    alienX_Change.append(0.1)
    alienY_Change.append(25)


def alien(x, y, i):
    screen.blit(alienImg[i], (x, y))


# Bullet(ready is that you can't see, fire is bullet will be moving)
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 0.6
bullet_state = "ready"


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Score
score_value = 0
font = pygame.font.Font("spacefont.ttf", 32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font("spacefont.ttf", 64)


def game_over(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 240))
    screen.blit(over_text, (x, y))


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 240))
    screen.blit(score, (x, y))


def isdead(alienX, alienY, playerX, playerY):
    distance = math.sqrt((math.pow(playerX - alienX, 2)) + (math.pow(playerY - alienY, 2)))
    if distance < 35:
        return True
    else:
        return False


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt((math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:
    # background coloring RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Player Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.2
            if event.key == pygame.K_UP:
                playerY_Change = -0.2
            if event.key == pygame.K_DOWN:
                playerY_Change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("bullet.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_Change = 0

    # player boundries
    playerX += playerX_Change
    playerY += playerY_Change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736
    if playerY <= 0:
        playerY = 0
    if playerY >= 536:
        playerY = 536

    # Alien Movement
    for i in range(numsOfAllien):
        # Game over
        if isdead(alienX[i], alienY[i], playerX, playerY) or alienY[i] > 440:
            for j in range(numsOfAllien):
                alienY[j] = 2000
            game_over(250, 250)
            break
        alienX[i] += alienX_Change[i]
        if alienX[i] <= 0:
            alienX_Change[i] = 0.1
            alienY[i] += alienY_Change[i]
        if alienX[i] >= 736:
            alienX_Change[i] = -0.1
            alienY[i] += alienY_Change[i]

        # Collision
        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)
    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
