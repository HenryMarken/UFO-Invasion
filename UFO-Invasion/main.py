import pygame
import random
import math 
import os
import os.path
import shutil

# Initalize #
pygame.init()
win_width = 700
win_height = 750
win = pygame.display.set_mode((win_width,win_height)) # make sure input is tuple
score_font = pygame.font.Font("freesansbold.ttf" , 32)
game_over_font = pygame.font.Font("freesansbold.ttf", 64)
pygame.display.set_caption("UFO Invasion")

# Images #
os.chdir("C:\\Users\\henry\\Desktop\\pythoncode\\mygame\\photos")
background = pygame.image.load("background.png")
alien_image = pygame.image.load("alien.png")
ship_image = pygame.image.load("ship.png")
bullet_image = pygame.image.load("bullet.png")
os.chdir("C:\\Users\\henry\\Desktop\\pythoncode\\mygame")

# Player/Spaceship #
class player:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 20
    def draw(self,win):
        win.blit(ship_image, (self.x, self.y))

# Enemy #

class enemy:
    def __init__(self,width,height):
        self.x = random.randint(0,(win_width - width))
        self.y = random.randint(0,160)
        self.width = width
        self.height = height
        self.vel = 10 * random.choice((-1,1))
        self.change = False

    # Enemy Movement #
    def move(self):
        if self.vel > 0: # going to the right
            if self.x + self.vel > win_width - self.width:
                self.vel *= -1 
                self.change = True
            else: 
                self.x += self.vel
        if self.vel < 0: # going to the left
            if self.x + self.vel < 0:
                self.vel *= -1
                self.change = True
            else:
                self.x += self.vel
        if self.change == True: 
            self.y += 40
            self.change = False

    # Enemy Drawing #
    def draw(self,win):
        self.move()
        win.blit(alien_image, (self.x, self.y))

# Bullet Class
class projectile:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 10
        self.fired = False

    def draw (self, win):
       win.blit(bullet_image, (self.x,self.y))

# Score # 

def show_score(x,y):
    score = score_font.render("Score: " + str(score_value), True, (255,255,255)) 
    win.blit(score, (x,y))

# Collision # 
def isCollision(enemyX, enemyY, bulletX, bulletY):
    if (bulletY in (range(enemyY,(enemyY+alien_height)))) and ((bulletX + bullet_width//2 - bullet.vel) in range(bulletX, (enemyX + alien_width))):
        return True
    else: 
        return False
    
# Redraw After Every Move/Hit #
def redraw():
    win.blit(background,(0,0)) # this is placing backgorund image over window at 0,0
    show_score(0,0)
    bullet.draw(win)
    for alien in aliens:
        alien.draw(win) # this is placing alien at 0,0 this needs to go second or it will be overlapped by background image
    ship.draw(win) 
    if (alien.y + alien_height) > 600 :
        alien.y = 1000
        over_text = game_over_font.render( "GAME OVER", True, (255,255,255))
        win.blit(over_text, (100, 200))
    pygame.display.update() # updating the screen each time

# Creating Player # 
ship_width = 80
ship_height = 80
ship = player(win_width//2,win_height - ship_height,ship_width,ship_height) # first two are location last two are size (check properties of image)

# Creating Enemy # 
aliens = []
alien_width = 80 
alien_height = 80
num_of_enemies = 5

# Creating Bullet # 
bullet_width = 20
bullet_height = 70
bullet = projectile(ship.x + ship.width//2 - bullet_width//2, ship.y, bullet_width, bullet_height)
# Score # 
score_value = 0 

fps = 30 # frames per second setting
fps_clock = pygame.time.Clock()


# Game loop/ Main loop #

Running = True
while Running:
    # 30 frames per second maximum
    fps_clock.tick(fps)
    # Check if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
    # Enemies #  
    if len(aliens) < num_of_enemies:
            aliens.append(enemy(alien_width,alien_height))
            

    # Player Actions #
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and ship.x > ship.vel:
        ship.x -= ship.vel
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and ship.x < win_width - ship.vel - ship.width  :
        ship.x += ship.vel
    if (keys[pygame.K_SPACE]) and not(bullet.fired): 
        bullet.fired = True
        bullet.x = ship.x + ship.width//2 - bullet_width//2
        bullet.y = ship.y
    if bullet.y <=0: # if bullet leaves page
        bullet.fired = False
        bullet.x = ship.x + ship.width//2 - bullet_width//2
        bullet.y = ship.y
    # Checking if bullet is still on screen and keeps moving#  
    if bullet.fired: 
        bullet.y -= bullet.vel
    # Checking if bullet hit target 
    for alien in aliens:
        collision  = isCollision(alien.x, alien.y, bullet.x, bullet.y)
        if collision:
            score_value += 1
            bullet.fired = False
            bullet.x = 1000
            bullet.y = 1000
            alien.x = random.randint(0,(win_width - alien.width))
            alien.y = random.randint(0,160)
        
    
    redraw() # created a function that will redraw everything

# This will terminate the console and end the program
pygame.quit()