from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random


# --- Game variables ---
GRID_LENGTH = 600
fuels = 50
score = 0
life = 5

car_x = 0
car_y = 0
car_angle = 0

car_speed = 0.5
normal_speed = car_speed
turn_speed = 1.8
blink_counter = 0
sky_color = [0.0, 0.0, 0.0]
target_sky_color = [0.0, 0.0, 0.0]

fuel_pickups = []  # (x,y,z)
fuel_consumed_distance = 0

boost_active = False
boost_timer = 0
boost_duration = 200     # frames (~200/60 ≈ 3 sec)
boost_speed = 1.2        # boosted speed


game_state=True

# Stars
num_stars = 100
stars = [(random.uniform(-GRID_LENGTH, GRID_LENGTH),
          random.uniform(-GRID_LENGTH, GRID_LENGTH),
          random.uniform(20, 100)) for _ in range(num_stars)]

# Toggle states for arrow keys
toggle = {
    GLUT_KEY_UP: False,
    GLUT_KEY_DOWN: False,
    GLUT_KEY_LEFT: False,
    GLUT_KEY_RIGHT: False
}

# Instruction flag
show_instruction = True

# --- Rain ---
num_raindrops = 200
raindrops = [(random.uniform(-GRID_LENGTH, GRID_LENGTH),
              random.uniform(-GRID_LENGTH, GRID_LENGTH),
              random.uniform(50, 200)) for _ in range(num_raindrops)]
rain_speed = 4.0

# --- Checkpoints (arrows along track) ---
checkpoint_angles = []
num_checkpoints = 10
checkpoint_blink_counter = 0

#Speed Breakers
speed_breaker_angles=[]
num_of_speed_breakers=8


# --- Speed breaker slowdown ---
slowdown_active = False
slowdown_timer = 0
slowdown_duration = 60   # frames (~1 second at 60 FPS)
slowdown_speed = 0.25    # reduced speed




# --- Text rendering ---
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(*color)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# --- Grid ---
def draw_grid():
    step = 50
    glColor3f(0.0, 1.0, 0.0)
    for x in range(-GRID_LENGTH, GRID_LENGTH, step):
        for y in range(-GRID_LENGTH, GRID_LENGTH, step):
            glBegin(GL_QUADS)
            glVertex3f(x, y, 0)
            glVertex3f(x + step, y, 0)
            glVertex3f(x + step, y + step, 0)
            glVertex3f(x, y + step, 0)
            glEnd()

def draw_stars():
    glColor3f(1, 1, 1)
    glPointSize(2)
    glBegin(GL_POINTS)
    for x, y, z in stars:
        glVertex3f(x, y, z)
    glEnd()

# --- Track ---
def draw_track():
    glColor3f(0.3, 0.3, 0.3)
    road_width = 60
    track_radius = GRID_LENGTH - 100
    segments = 100

    glBegin(GL_TRIANGLE_STRIP)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x_outer = track_radius * math.cos(angle)
        y_outer = track_radius * math.sin(angle)
        glVertex3f(x_outer, y_outer, 0.1)

        x_inner = (track_radius - road_width) * math.cos(angle)
        y_inner = (track_radius - road_width) * math.sin(angle)
        glVertex3f(x_inner, y_inner, 0.1)
    glEnd()

# --- Car ---
def draw_car(x=0, y=0, z=0):
    scale = 0.1
    def S(v): return v * scale

    # Wheels
    glColor3f(0, 0, 0)
    wheel_positions = [
        (40, 20, 5),
        (40, -20, 5),
        (-40, 20, 5),
        (-40, -10, 5)
    ]
    for wx, wy, wz in wheel_positions:
        glPushMatrix()
        glTranslatef(S(wx), S(wy), S(wz))
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, S(5), S(5), S(10), 12, 12)
        glPopMatrix()

    # Body
    z_offset = 10
    glPushMatrix()
    glTranslatef(S(x), S(y), S(z + z_offset))
    glColor3f(0, 0, 1)
    glBegin(GL_QUADS)
    glVertex3f(S(-45), S(-25), S(0))
    glVertex3f(S(45), S(-25), S(0))
    glVertex3f(S(45), S(25), S(0))
    glVertex3f(S(-45), S(25), S(0))
    glVertex3f(S(-45), S(-25), S(15))
    glVertex3f(S(45), S(-25), S(15))
    glVertex3f(S(45), S(25), S(15))
    glVertex3f(S(-45), S(25), S(15))
    glEnd()

    # Cabin
    glColor3f(0, 0.5, 1)
    glBegin(GL_QUADS)
    glVertex3f(S(-25), S(-20), S(15))
    glVertex3f(S(25), S(-20), S(15))
    glVertex3f(S(25), S(20), S(15))
    glVertex3f(S(-25), S(20), S(15))
    glVertex3f(S(-20), S(-15), S(25))
    glVertex3f(S(20), S(-15), S(25))
    glVertex3f(S(20), S(15), S(25))
    glVertex3f(S(-20), S(15), S(25))
    glEnd()

    # Backlights
    glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(S(-45), S(15), S(10))
    glVertex3f(S(-40), S(15), S(10))
    glVertex3f(S(-40), S(15), S(5))
    glVertex3f(S(-45), S(15), S(5))
    glVertex3f(S(-45), S(-15), S(10))
    glVertex3f(S(-40), S(-15), S(10))
    glVertex3f(S(-40), S(-15), S(5))
    glVertex3f(S(-45), S(-15), S(5))
    glEnd()

    glPopMatrix()

# --- Fuel ---
def spawn_fuel_pickups(n=8):
    global fuel_pickups
    road_width = 60
    track_radius = GRID_LENGTH - 100
    for _ in range(n):
        angle = random.uniform(0, 2*math.pi)
        r = random.uniform(track_radius - road_width + 5, track_radius - 5)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        fuel_pickups.append((x, y, 2))

def draw_fuel_can(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    quad = gluNewQuadric()
    glColor3f(0,0,0)
    gluCylinder(quad, 3, 3, 8, 32, 32)
    for sh in [2,4,6]:
        glPushMatrix()
        glTranslatef(0,0,sh)
        glColor3f(1,1,1)
        gluCylinder(quad, 3.1,3.1,0.15,32,1)
        glPopMatrix()
    glPopMatrix()

def draw_fuel_pickups():
    for x,y,z in fuel_pickups:
        draw_fuel_can(x,y,z)

# --- Rain ---
def draw_rain():
    brightness = sum(sky_color)/3
    rain_col = (0,0,1) if brightness>0.5 else (0.7,0.7,1.0)
    glColor3f(*rain_col)
    glBegin(GL_LINES)
    for x,y,z in raindrops:
        glVertex3f(x,y,z)
        glVertex3f(x,y,z-5)
    glEnd()

def update_rain():
    global raindrops
    new_list = []
    for x,y,z in raindrops:
        z -= rain_speed
        if z<=0:
            z = random.uniform(100,200)
            x = random.uniform(-GRID_LENGTH, GRID_LENGTH)
            y = random.uniform(-GRID_LENGTH, GRID_LENGTH)
        new_list.append((x,y,z))
    raindrops[:] = new_list

# --- Checkpoints (evenly distributed arrows) ---
def spawn_checkpoints():
    global checkpoint_angles, checkpoint_positions
    checkpoint_angles = []
    checkpoint_positions = []
    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2  

    for i in range(num_checkpoints):
        angle = 2 * math.pi * i / num_checkpoints
        checkpoint_angles.append(angle)

        x = track_center_radius * math.cos(angle)
        y = track_center_radius * math.sin(angle)
        checkpoint_positions.append((x, y))


def draw_checkpoints():
    global checkpoint_blink_counter
    checkpoint_blink_counter += 1

    glow = 0.5 + 0.5 * math.sin(checkpoint_blink_counter * 0.1)

    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2  

    arrow_length = 35
    arrow_width = 18
    arrow_z = 0.5

    glColor3f(0.0, glow, 0.0)

    for angle in checkpoint_angles:
        # Position along track
        x_center = track_center_radius * math.cos(angle)
        y_center = track_center_radius * math.sin(angle)

        # Tangent to the circle = direction of road
        tangent_angle_deg = math.degrees(angle) + 90   # <-- FIXED

        glPushMatrix()
        glTranslatef(x_center, y_center, arrow_z)
        glRotatef(tangent_angle_deg, 0, 0, 1)

        # Draw arrow (pointing in +X direction by default)
        glBegin(GL_TRIANGLES)
        glVertex3f(0, -arrow_width / 2, 0)
        glVertex3f(0, arrow_width / 2, 0)
        glVertex3f(arrow_length, 0, 0)
        glEnd()

        glPopMatrix()

def check_checkpoint_collision():
    global boost_active, boost_timer, car_speed
    for (cx, cy) in checkpoint_positions:
        dx = car_x - cx
        dy = car_y - cy
        if dx*dx + dy*dy < 8*8:   # within radius 8
            boost_active = True
            boost_timer = boost_duration
            car_speed = boost_speed
            break


def spawn_speedbreakers():
    global speedbreaker_angles, speedbreaker_positions
    speedbreaker_angles = []
    speedbreaker_positions = []

    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2  

    for i in range(num_of_speed_breakers):
        angle = 2 * math.pi * i / num_of_speed_breakers
        speedbreaker_angles.append(angle)

        x = track_center_radius * math.cos(angle)
        y = track_center_radius * math.sin(angle)
        speedbreaker_positions.append((x, y))


def draw_speedbreakers():
    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2  

    breaker_length = 20   # along driving direction
    breaker_width  = road_width * 0.6  # almost covers road width
    breaker_z = 0.2   # <<-- FLUSH WITH ROAD (instead of 1.5)

    for angle in speedbreaker_angles:
        x_center = track_center_radius * math.cos(angle)
        y_center = track_center_radius * math.sin(angle)

        tangent_angle_deg = math.degrees(angle)

        glPushMatrix()
        glTranslatef(x_center, y_center, breaker_z)
        glRotatef(tangent_angle_deg, 0, 0, 1)

        # striped pattern along the road
        num_stripes = 4
        stripe_spacing = breaker_width / num_stripes

        for i in range(num_stripes):
            if i % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0, 0, 0)

            y1 = -breaker_width/2 + i * stripe_spacing
            y2 = y1 + stripe_spacing
            x1 = -breaker_length/2
            x2 = breaker_length/2

            glBegin(GL_QUADS)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
            glEnd()

        glPopMatrix()



def check_speedbreaker_collision():
    global slowdown_active, slowdown_timer, car_speed

    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2  

    for angle in speedbreaker_angles:
        cx = track_center_radius * math.cos(angle)
        cy = track_center_radius * math.sin(angle)

        dx = car_x - cx
        dy = car_y - cy
        dist2 = dx*dx + dy*dy

        if dist2 < (12*12):   # within radius 12
            slowdown_active = True
            slowdown_timer = slowdown_duration
            car_speed = slowdown_speed
            break





# --- Input ---
def special_key_pressed(key, x, y):
    global show_instruction, car_angle,game_state
    if game_state==False:
        return
    if key == GLUT_KEY_LEFT:
        car_angle += turn_speed    # rotate left instantly
        show_instruction = False
    elif key == GLUT_KEY_RIGHT:
        car_angle -= turn_speed    # rotate right instantly
    elif key == GLUT_KEY_UP:
        toggle[GLUT_KEY_UP] = not toggle[GLUT_KEY_UP]


def keyboard_listener(key, x, y):
    global target_sky_color
    if key == b'd':
        target_sky_color = [1.0, 1.0, 1.0]
    elif key == b'n':
        target_sky_color = [0.0, 0.0, 0.0]
    elif key==b'r':
        restart_game()

def restart_game():
    global car_x, car_y, car_angle, car_speed, fuels, fuel_consumed_distance
    global boost_active, boost_timer, slowdown_active, slowdown_timer, game_state
    global fuel_pickups, checkpoint_angles, checkpoint_positions
    global speedbreaker_angles, speedbreaker_positions, blink_counter

    car_x, car_y, car_angle = 0, 0, 0
    car_speed = normal_speed
    fuels = 50
    fuel_consumed_distance = 0

    boost_active, boost_timer = False, 0
    slowdown_active, slowdown_timer = False, 0
    game_state = True

    blink_counter = 0

    # Respawn fuel pickups, checkpoints, and speed breakers
    fuel_pickups.clear()
    spawn_fuel_pickups(8)
    spawn_checkpoints()
    spawn_speedbreakers()


# --- Car movement ---
def process_car_movement():
    global car_x, car_y, fuel_consumed_distance, fuels, game_state
    if not game_state:
        return  # Stop car movement if game over

    rad = math.radians(car_angle)
    old_x, old_y = car_x, car_y
    if toggle[GLUT_KEY_UP]:
        car_x += car_speed * math.cos(rad)
        car_y += car_speed * math.sin(rad)

    dx, dy = car_x - old_x, car_y - old_y
    moved = math.sqrt(dx*dx + dy*dy)
    fuel_consumed_distance += moved
    if fuel_consumed_distance > 50 and fuels > 0:
        fuels -= 1
        fuel_consumed_distance = 0

    if fuels <= 0:
        fuels = 0
        game_state = False  # <-- Game Over



def check_fuel_collection():
    global fuels, fuel_pickups
    new_pickups = []
    road_width = 60
    track_radius = GRID_LENGTH - 100
    for x,y,z in fuel_pickups:
        dx = car_x - x
        dy = car_y - y
        if dx*dx+dy*dy < 5*5:
            fuels = min(fuels+20,100)
            angle = random.uniform(0, 2*math.pi)
            r = random.uniform(track_radius-road_width+5, track_radius-5)
            new_pickups.append((r*math.cos(angle), r*math.sin(angle),2))
        else:
            new_pickups.append((x,y,z))
    fuel_pickups[:] = new_pickups

# --- Camera ---
def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    cam_distance = 40
    cam_height = 15
    rad = math.radians(car_angle)
    cam_x = car_x - cam_distance*math.cos(rad)
    cam_y = car_y - cam_distance*math.sin(rad)
    cam_z = cam_height
    target_x = car_x + 80*math.cos(rad)
    target_y = car_y + 80*math.sin(rad)
    target_z = 10
    gluLookAt(cam_x, cam_y, cam_z, target_x, target_y, target_z, 0,0,1)

# --- Display ---
def showScreen():
    glClearColor(sky_color[0], sky_color[1], sky_color[2], 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,1000,800)
    setupCamera()
    draw_grid()
    draw_track()
    draw_rain()
    draw_checkpoints()
    draw_speedbreakers()
    if sky_color[0]<0.5:
        draw_stars()
    draw_fuel_pickups()
    glPushMatrix()
    glTranslatef(car_x, car_y, 0)
    glRotatef(car_angle,0,0,1)
    draw_car(0,0,0)
    glPopMatrix()
    draw_text(10,700,f"Life x {life}",color=(0,0,1))
    draw_text(450,700,f"Fuel Left x {fuels}",color=(0,0.9,0))
    draw_text(900,700,f"Coins: {score}",color=(1,1,0))

    if game_state and show_instruction and (blink_counter//60)%2==0:
        draw_text(400,500,"<--- TAKE LEFT", color=(1,1,0))


    # Display Game Over
    if game_state==False:
        draw_text(470,480,"GAME OVER", color=(1,0,0))
        draw_text(420,450,'PRESS "R" TO RESTART',color=(1,1,1))
        draw_text(465,420,f'TOTAL SCORE:{score}',color=(1,1,0))

        

    glutSwapBuffers()


# --- Idle ---
def idle():
    global blink_counter, sky_color, boost_active, boost_timer, car_speed
    global slowdown_active, slowdown_timer

    if game_state==False:
        glutPostRedisplay()  # Still redraw to show "GAME OVER" text
        return  # Skip all updates

    # Smoothly transition sky color
    for i in range(3):
        delta = target_sky_color[i] - sky_color[i]
        sky_color[i] += delta * 0.02

    process_car_movement()
    blink_counter += 1
    check_fuel_collection()
    check_checkpoint_collision()
    check_speedbreaker_collision()
    update_rain()

    # handle boost timer
    if boost_active:
        boost_timer -= 1
        if boost_timer <= 0:
            boost_active = False
            car_speed = normal_speed

    # handle slowdown timer
    if slowdown_active:
        slowdown_timer -= 1
        if slowdown_timer <= 0:
            slowdown_active = False
            car_speed = normal_speed
    
    glutPostRedisplay()






# --- Main ---
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,730)
    glutInitWindowPosition(150,0)
    glutCreateWindow(b"3D OpenGL Car Game")
    spawn_fuel_pickups(8)
    spawn_checkpoints()
    spawn_speedbreakers()
    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutSpecialFunc(special_key_pressed)
    glutKeyboardFunc(keyboard_listener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
