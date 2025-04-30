from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math 
import random

#The Variable of the Game
GRID_LENGTH = 800
TILE_SIZE = 80
game_score = 0
player_life = 5
bullets_missed = 0
game_over = False

#Camera Setting
camera_postion = (0, 600, 600)
camera_follow_gun = False

#Variable for Player and the Gun
player_position = [0, 0, 0]
gun_angle = 0
gun_size = 50

#Varible for the Bullets
bullets_list = []
BULLET_SPEED = 8

#Variables for Enemy
enemies_list = []
enemy_speed = 0.05
NUM_ENEMIES = 5

#Variable for Animation
animation = 0

def init_game():
    global player_position, gun_angle, game_over, game_score, player_life, bullets_missed, bullets_list, enemies_list
    player_position = [0, 0, 0]
    gun_angle = 0
    game_over = False
    game_score = 0
    player_life = 5
    bullets_missed = 0
    bullets_list = []

    #Spawing enemies at random postion
    while True:
        x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        distance = math.sqrt((x - player_position[0])**2 + (y - player_position[1]**2))
        if distance > 300:
            break
    enemies_list.append({
        'pos': [x, y, 0],
        'scale': 1.0,
        'enemy_bounce': 0.01
    })
