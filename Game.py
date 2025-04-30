from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math 
import random

GRID_LENGTH = 800
TILE_SIZE = 80
game_score = 0
player_life = 5
bullets_missed = 0
game_over = False

camera_position = (0, 600, 600)
camera_follow_gun = False

player_position = [0, 0, 0]
gun_angle = 0
gun_size = 50

bullets_list = []
BULLET_SPEED = 8

enemies_list = []
enemy_speed = 0.05
NUM_ENEMIES = 5

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
    enemies_list = []
    for i in range(NUM_ENEMIES):
        spawn_enemy()

def spawn_enemy():
    while True:
        x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        distance = math.sqrt((x - player_position[0])**2 + (y - player_position[1])**2)
        if distance > 300:
            break
    enemies_list.append({
        'position': [x, y, 0],
        'scale': 1.0,
        'enemy_bounce': 0.01
    })

def fire_bullet():
    if game_over == True:
        return
    angle_radian = math.radians(gun_angle)
    barrel_length = 70
    barrel_height = 30
    bullet_position_x_axis = player_position[0] + barrel_length * math.cos(angle_radian)
    bullet_position_y_axis = player_position[1] + barrel_length * math.sin(angle_radian)
    bullet_position_z_axis = player_position[2] + barrel_height
    bullet_direction_x_axis = math.cos(angle_radian)
    bullet_direction_y_axis = math.sin(angle_radian)
    bullet = {
        'position': [bullet_position_x_axis, bullet_position_y_axis, bullet_position_z_axis],
        'direction': [bullet_direction_x_axis, bullet_direction_y_axis, 0],
        'bullet_life': 200
    }
    bullets_list.append(bullet)

def update_bullets():
    global bullets_list, enemies_list, game_score, bullets_missed
    bullets_to_remove = []
    for i in range(len(bullets_list)):
        bullet = bullets_list[i]
        bullet['position'][0] += bullet['direction'][0] * BULLET_SPEED
        bullet['position'][1] += bullet['direction'][1] * BULLET_SPEED
        bullet['bullet_life'] -= 1
        if (abs(bullet['position'][0]) > GRID_LENGTH or 
            abs(bullet['position'][1]) > GRID_LENGTH or 
            bullet['bullet_life'] <= 0):
            bullets_to_remove.append(i)
            bullets_missed += 1
            print(f"Bullet missed! Total missed: {bullets_missed}/10")
            continue
        for j in range(len(enemies_list)):
            enemy = enemies_list[j]
            dx = bullet['position'][0] - enemy['position'][0]
            dy = bullet['position'][1] - enemy['position'][1]
            dz = bullet['position'][2] - enemy['position'][2]
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            if distance < 40:
                bullets_to_remove.append(i)
                game_score += 10
                spawn_enemy()
                enemies_list.pop(j)
                break
    for i in sorted(bullets_to_remove, reverse=True):
        if i < len(bullets_list):
            bullets_list.pop(i)
    if bullets_missed >= 10:
        end_game()

def update_enemies():
    global enemies_list, player_life
    for enemy in enemies_list[:]:
        dx = player_position[0] - enemy['position'][0]
        dy = player_position[1] - enemy['position'][1]
        distance = math.sqrt(dx**2 + dy**2)
        if distance > 0:
            enemy['position'][0] += (dx / distance) * enemy_speed
            enemy['position'][1] += (dy / distance) * enemy_speed
            enemy['scale'] += enemy['enemy_bounce']
            if enemy['scale'] > 1.2 or enemy['scale'] < 0.8:
                enemy['enemy_bounce'] *= -1
            if distance < 60:
                player_life -= 1
                print(f"Player hit! Lives remaining: {player_life}")
                spawn_enemy()
                enemies_list.remove(enemy)
                if player_life <= 0:
                    end_game()
                break

def end_game():
    global game_over
    game_over = True

def draw_text():
    global game_over
    game_over = True

def draw_text(x, y, text, font = GLUT_BITMAP_HELVETICA_18): # type: ignore
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for i in text:
        glutBitmapCharacter(font, ord(i))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    glBegin(GL_QUADS)
    glColor3f(1, 1, 1)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glColor3f(0.7, 0.5, 0.95)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()
