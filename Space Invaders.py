import pygame as pyg
import random
import math
from pygame import mixer

#Initialize the pygame
pyg.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 255)
blue = (0, 0, 255)
light_green = (0, 200, 0)
gray = (119, 118, 110)

#Create screen
screen = pyg.display.set_mode((800, 600))

#ackground
background = pyg.image.load("space_bg.png")
background = pyg.transform.scale(background, (800, 600))

#Backgroung Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

#Title and Icon
pyg.display.set_caption("Space Invadors")
icon = pyg.image.load("ufo.png")
pyg.display.set_icon(icon)

# Player
playerImg = pyg.image.load("player.png")
playerImg = pyg.transform.scale(playerImg, (64, 64))
playerX = 370
playerY = 480
playerX_change = 0

# Enemy and multiple enemies
enemyImg = []
enemyX = []
enemyY= []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10

for i in range(num_of_enemies):
    enemyImg.append(pyg.image.load("enemy.png"))
    enemyImg.append(pyg.transform.scale(enemyImg[i], (64, 64)))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)


# Bullet
bullet = pyg.image.load("bullet.png")
bulletImg = pyg.transform.scale(bullet, (32, 32))
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
#Ready means you can't see bullet on the screen
#Fire means bullet is moving towards the target
bullet_state = "ready"

#Score
score_value = 0
font = pyg.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over Text
over_font = pyg.font.Font('freesansbold.ttf', 128)

def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (300, 275))


def show_score(x, y):
    score = font.render("SCORE: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


#Create infinite loop
running = True
while running:
    #Screen.fill((255, 0, 0))
    screen.fill(green)
    #Backgroung image
    screen.blit(background, (0, 0))
    for event in pyg.event.get():
        if event.type == pyg.QUIT:
            running = False
    # If key stroke is placed chech whether it's right/6 or left/4
        if event.type == pyg.KEYDOWN:
            if event.key == pyg.K_KP4:
                playerX_change = -0.8
            if event.key == pyg.K_KP6:
                playerX_change = 0.8
            if event.key == pyg.K_KP5:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    #get the current x coordinates of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, playerY)
        if event.type == pyg.KEYUP:
            if event.key == pyg.K_KP4 or event.key == pyg.K_KP6:
                playerX_change = 0

    # Checking for boundries
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736

    #Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.6
            enemyY[i] += enemyY_change[i]
        if enemyX[i] >= 735:
            enemyX_change[i] = -0.6
            enemyY[i] += enemyY_change[i]

    #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    #Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pyg.display.update()