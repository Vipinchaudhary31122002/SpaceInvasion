import pygame
import random
import math

# initialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((1000,600))

# background of the game
background = pygame.image.load('Images/background.jpg')

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('Images/alien.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('Images/player.png')
playerX = 500
playerY = 525
playerX_change=0

# enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5
for i in range(num_of_enemies):
	enemyImg.append(pygame.image.load('Images/enemy.png'))
	enemyX.append(random.randint(64, 936))
	enemyY.append(random.randint(64, 450))
	if enemyX[i]>0 and enemyX[i]<500:
		enemyX_change.append(-1)
	else:
		enemyX_change.append(1)
	enemyY_change.append(10)

# bullet
# ready - you cannot see the bullet but it is ready for firing
# fire - bullet is currently moving on the screen
bulletImg = pygame.image.load('Images/bullet.png')
bulletX = 0
bulletY = 500
bulletX_change=0
bulletY_change=10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font('Fonts/FreeSansBold.ttf', 32)
textX = 10
textY = 10

# game_over_text
over_font = pygame.font.Font('Fonts/FreeSansBold.ttf', 150)

def show_score(x, y):
	score = font.render("Score: " + str(score_value), True, (255, 255, 255))
	screen.blit(score, (x, y))

def game_over_text():
	over_text = over_font.render("GAME OVER", True, (255, 255, 255))
	screen.blit(over_text, (50, 200))	

def fire_bullet(x, y):
	global bullet_state
	bullet_state = "fire"
	screen.blit(bulletImg, (x+16, y+10))

def player(x,y):
	screen.blit(playerImg, (x, y))

def enemy(x, y, i):
	screen.blit(enemyImg[i], (x, y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
	distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
	if distance <27:
		return True
	return False

# Game loop
running = True
while running:
	screen.fill((0, 0, 0))
	# background image
	screen.blit(background, (0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed then check it is left or right
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -5
			if event.key == pygame.K_RIGHT:
				playerX_change = 5
			if event.key == pygame.K_SPACE:
				if bullet_state == "ready":
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0


	# player movement algo which stop the player from moving away from the boundary
	playerX+=playerX_change
	if playerX <= 0:
		playerX = 0
	elif playerX >= 936:
		playerX = 936

	# enemy movement algo which make the enemy and to move left and right and also after hitting left and right move it on downward axis
	for i in range(num_of_enemies):
		# game over
		if enemyY[i] > 450:
			for j in range(num_of_enemies):
				enemyY[j] = 2000
			game_over_text()
			break

		enemyX[i] += enemyX_change[i]
		if enemyX[i] <= 0:
			enemyX_change[i] = 1
			enemyY[i] += enemyY_change[i]
		elif enemyX[i] >= 936:
			enemyX_change[i] = -1
			enemyY[i] += enemyY_change[i]

		# collision 
		collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
		if collision:
			bulletY =  500
			bullet_state = "ready"
			score_value +=10
			enemyX[i] = random.randint(64, 936)
			enemyY[i] = random.randint(64, 450)

		enemy(enemyX[i], enemyY[i], i)

	# bullet movement
	if bulletY <= 0:
		bulletY = 500
		bullet_state = "ready"
	if bullet_state == "fire":
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	player(playerX, playerY)
	show_score(textX, textY)
	pygame.display.update()
