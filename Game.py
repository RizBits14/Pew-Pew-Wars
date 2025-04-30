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

def draw_player():
    glPushMatrix()
    glTranslatef(player_position[0], player_position[1], player_position[2])
    glRotatef(gun_angle, 0, 0, 1)
    if game_over == True:
        glRotatef(90, 1, 0, 0)
    glColor3f(0.2, 0.4, 0.8)
    gluSphere(gluNewQuadric(), 30, 20, 20)
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(0, 0, 30)
    glutSolidCube(gun_size * 0.5)
    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(70, 0, 0)
    glColor3f(0.0, 0.0, 0.0)
    glutSolidSphere(5, 10, 10)
    glPopMatrix()
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 70, 10, 10)
    glPopMatrix()

def gun_barrel():
    angle_radian = math.radians(gun_angle)
    barrel_length = 70
    barrel_height = 30
    return [
        player_position[0] + barrel_length * math.cos(angle_radian),
        player_position[1] + barrel_length * math.sin(angle_radian),
        player_position[2] + barrel_height
    ]

def draw_bullets():
    for bullet in bullets_list:
        glPushMatrix()
        glTranslatef(bullet['position'][0], bullet['position'][1], bullet['position'][2])
        glColor3f(1.0, 0.7, 0)
        glutSolidCube(20)
        glPopMatrix()

def draw_enemies():
    for enemy in enemies_list:
        glPushMatrix()
        glTranslatef(enemy['position'][0], enemy['position'][1], enemy['position'][2])
        glScalef(enemy['scale'], enemy['scale'], enemy['scale'])
        glColor3f(0.8, 0.2, 0.2)
        gluSphere(gluNewQuadric(), 40, 20, 20)
        glColor3f(0.9, 0.9, 0.9)
        glTranslatef(0, 0, 30)
        gluSphere(gluNewQuadric(), 15, 10, 10)
        glPopMatrix()

def draw_shapes():
    draw_grid()
    draw_player()
    draw_bullets()
    draw_enemies()

def keyboardListener(key, x, y):
    global player_position, gun_angle, game_over
    if game_over and key == b'r':
        init_game()
        return
    if game_over == True:
        return
    if key == b'a':
        angle_radian = math.radians(gun_angle)
        player_position[0] += math.cos(angle_radian) * 10
        player_position[1] += math.sin(angle_radian) * 10
    if key == b'd':
        angle_radian = math.radians(gun_angle)
        player_position[0] -= math.cos(angle_radian) * 10
        player_position[1] -= math.sin(angle_radian) * 10
    if key == b's':
        angle_radian = math.radians(gun_angle + 90)
        player_position[0] += math.cos(angle_radian) * 10
        player_position[1] += math.sin(angle_radian) * 10
    if key == b'w':
        angle_radian = math.radians(gun_angle - 90)
        player_position[0] += math.cos(angle_radian) * 10
        player_position[1] += math.sin(angle_radian) * 10
    if key == b'q':
        gun_angle += 5 
        if gun_angle >= 360:
            gun_angle -= 360
    if key == b'e':
        gun_angle -= 5 
        if gun_angle < 0:
            gun_angle += 360
    player_position[0] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_position[0]))
    player_position[1] = max(-GRID_LENGTH + 50, min(GRID_LENGTH - 50, player_position[1]))

def specialKeyListener(key, x, y):
    global camera_position
    if key == GLUT_KEY_UP:
        z += 10  
        if z > 800:
            z = 800  
    if key == GLUT_KEY_DOWN:
        z -= 10 
        if z < 100:
            z = 100  
    if key == GLUT_KEY_LEFT:
        x -= 10  
    if key == GLUT_KEY_RIGHT:
        x += 10  
    camera_position = (x, y, z)
    x, y, z = camera_position
    if key == GLUT_KEY_UP:
        z += 10  
        if z > 800:
            z = 800  
    if key == GLUT_KEY_DOWN:
        z -= 10 
        if z < 100:
            z = 100  
    if key == GLUT_KEY_LEFT:
        x -= 10  
    if key == GLUT_KEY_RIGHT:
        x += 10  
    camera_position = (x, y, z)

def mouseListener(button, state, x, y):
    global camera_follow_gun
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        fire_bullet()
        print("Bullet fired!")
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_follow_gun = not camera_follow_gun

def setupCamera():
    global camera_position, player_position, gun_angle, camera_follow_gun
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity() 
    gluPerspective(120, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW) 
    glLoadIdentity()
    if camera_follow_gun:
        angle_radian = math.radians(gun_angle)
        lookAtX = player_position[0] + 100 * math.cos(angle_radian)
        lookAtY = player_position[1] + 100 * math.sin(angle_radian)
        eyeX = player_position[0] - 30 * math.cos(angle_radian)
        eyeY = player_position[1] - 30 * math.sin(angle_radian)
        eyeZ = player_position[2] + 50
        gluLookAt(eyeX, eyeY, eyeZ, lookAtX, lookAtY, player_position[2],0, 0, 1)
    else:
        x, y, z = camera_position
        radius = math.sqrt(x*x + y*y)
        angle = math.atan2(y, x)
        eyeX = radius * math.cos(angle)
        eyeY = radius * math.sin(angle)
        eyeZ = z
        gluLookAt(eyeX, eyeY, eyeZ, 0, 0, 0, 0, 0, 1)

def update_game():
    global animation
    if game_over == True:
        return
    animation += animation
    update_bullets()
    update_enemies()

def idle():
    update_game()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    glEnable(GL_DEPTH_TEST)
    setupCamera()
    draw_shapes()
    draw_text(10, 770, f"Score: {game_score}")
    draw_text(10, 740, f"Life: {player_life}")
    draw_text(10, 710, f"Bullets Missed: {bullets_missed}/10")
    if camera_follow_gun == True:
        draw_text(10, 680, "FIRST-PERSON VIEW")
    if game_over == True:
        draw_text(400, 400, "GAME OVER")
        draw_text(350, 370, "Press 'R' to restart")
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(1000, 800)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Bullet Frenzy - 3D Game")

init_game()
glEnable(GL_DEPTH_TEST)
glEnable(GL_COLOR_MATERIAL)
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(idle)
glutMainLoop()
