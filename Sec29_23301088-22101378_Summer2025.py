from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random





# --- Game variables ---
game_started = False
track_entered = False
car_radius=5
paused = False
quadric = gluNewQuadric()



# Coin variables
coin_pickups = []   # list of (x, y, z)
coin_value=10
num_coins = 5
coin_radius = 2
coin_thickness = 2


# --- Car speed ---
base_speed = 0.5         # initial speed
normal_speed = base_speed # reference speed (resets after boost/slowdown)
boost_speed = 1.2         # boosted speed
slowdown_speed = 0.25     # slowed speed
score_speed_factor = 0.005  # speed increase per score point
max_speed = 3.0           # maximum possible speed




# --- Invisibility Power-up ---
invisible_active = False
invisible_timer = 0
invisible_duration = 400  # frames (~3 seconds)
invisible_alpha = 0.4     # transparency (0=fully invisible, 1=opaque)

invisible_pickups = []  # stores (x, y, z)
num_invisible = 3       # number of invisibility spheres





#Up press detection
up_press_count = 0
max_up_presses = 3


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

#OBSTACLES
num_obstacles = 8
obstacle_positions = []  # stores (x, y) for each cube
obstacle_size = 10  # cube size

# Track which obstacles were already hit
obstacles_hit = set()
# TRACK GEOMETRY
track_radius_outer = GRID_LENGTH - 100
road_width = 60
track_radius_inner = track_radius_outer - road_width
track_radius_center = track_radius_outer - road_width / 2


def spawn_invisible_powerups(n=num_invisible):
    global invisible_pickups
    invisible_pickups.clear()
    road_width = 60
    track_radius_outer = GRID_LENGTH - 100
    track_center_radius = track_radius_outer - road_width / 2

    for i in range(n):
        angle = random.uniform(0, 2*math.pi)
        r = random.uniform(track_radius_outer - road_width + 5, track_radius_outer - 5)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = 2
        invisible_pickups.append((x, y, z))

def draw_invisible_powerups():
    for x, y, z in invisible_pickups:
        glPushMatrix()
        glTranslatef(x, y, z + 2)
        glColor3f(0, 0, 1)  # blue color
        gluSphere(quadric, 2.5, 20, 20)  # radius, slices, stacks
        glPopMatrix()


def check_invisible_collection():
    global invisible_active, invisible_timer, invisible_pickups
    new_list = []
    for x, y, z in invisible_pickups:
        dx = car_x - x
        dy = car_y - y
        if dx*dx + dy*dy < 5*5:
            invisible_active = True
            invisible_timer = invisible_duration

            # Respawn the collected blue sphere at a new random position
            track_radius_outer = GRID_LENGTH - 100
            road_width = 60
            angle = random.uniform(0, 2*math.pi)
            r = random.uniform(track_radius_outer - road_width + 5, track_radius_outer - 5)
            new_x = r * math.cos(angle)
            new_y = r * math.sin(angle)
            new_list.append((new_x, new_y, z))  # keep the same z
        else:
            new_list.append((x, y, z))
    invisible_pickups[:] = new_list




def spawn_coins(n=num_coins):
    global coin_pickups
    coin_pickups.clear()

    road_width = 60
    track_radius_outer = GRID_LENGTH - 100
    track_center_radius = track_radius_outer - road_width / 2

    for _ in range(n):
        angle = random.uniform(0, 2 * math.pi)
        # place coin along road width randomly
        r = random.uniform(track_radius_outer - road_width + 5, track_radius_outer - 5)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = coin_thickness / 2   # so coin sits on the floor
        coin_pickups.append((x, y, z))

        






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
    segments = 100  # more segments = smoother circle

    for i in range(segments):
        angle1 = 2 * math.pi * i / segments
        angle2 = 2 * math.pi * (i + 1) / segments

        # Outer edge
        x1_outer = track_radius * math.cos(angle1)
        y1_outer = track_radius * math.sin(angle1)
        x2_outer = track_radius * math.cos(angle2)
        y2_outer = track_radius * math.sin(angle2)

        # Inner edge
        x1_inner = (track_radius - road_width) * math.cos(angle1)
        y1_inner = (track_radius - road_width) * math.sin(angle1)
        x2_inner = (track_radius - road_width) * math.cos(angle2)
        y2_inner = (track_radius - road_width) * math.sin(angle2)

        # Draw quad for this segment
        glBegin(GL_QUADS)
        glVertex3f(x1_outer, y1_outer, 0.1)
        glVertex3f(x2_outer, y2_outer, 0.1)
        glVertex3f(x2_inner, y2_inner, 0.1)
        glVertex3f(x1_inner, y1_inner, 0.1)
        glEnd()




def check_car_on_track():
    global game_state, game_started, track_entered, car_radius
    # use the global track radii you set near the top of the file
    global track_radius_inner, track_radius_outer

    if not game_started:
        return  # don't check until the car actually started moving

    # current distance of car centre from world origin (track centre)
    dist = math.hypot(car_x, car_y)

    # margin = radius of car in world units (tweak if needed)
    margin = car_radius

    if not track_entered:
        # consider track entered only when the car's CENTER lies inside the road band
        if track_radius_inner <= dist <= track_radius_outer:
            track_entered = True
    else:
        # game over ONLY when the car is completely outside the road:
        #  - completely inside the inner hole: (dist + margin) < inner
        #  - completely outside the outer edge: (dist - margin) > outer
        if (dist + margin) < track_radius_inner or (dist - margin) > track_radius_outer:
            game_state = False












# --- Car ---
def draw_car(x=0, y=0, z=0):
    scale = 0.1
    def S(v): return v * scale

    # Colors
    if invisible_active:
        body_color = cabin_color = wheel_color = backlight_color = (0.4, 0.7, 1.0)  # pale blue
    else:
        body_color = (0, 0, 1)         # blue body
        cabin_color = (0, 0.5, 1)      # blue cabin
        wheel_color = (0, 0, 0)        # black wheels
        backlight_color = (1, 0, 0)    # red backlights

    # --- Wheels ---
    wheel_positions = [(40, 20, 5), (40, -20, 5), (-40, 20, 5), (-40, -10, 5)]
    for wx, wy, wz in wheel_positions:
        glPushMatrix()
        glTranslatef(S(wx)+x, S(wy)+y, S(wz)+z)
        glRotatef(90,1,0,0)
        glColor3f(*wheel_color)
        quad = gluNewQuadric()
        gluCylinder(quad, S(5), S(5), S(10), 12, 12)
        glPopMatrix()

    # --- Body ---
    z_offset = 10
    glPushMatrix()
    glTranslatef(S(x), S(y), S(z+z_offset))
    glColor3f(*body_color)
    glBegin(GL_QUADS)
    # bottom & top
    glVertex3f(S(-45), S(-25), S(0))
    glVertex3f(S(45), S(-25), S(0))
    glVertex3f(S(45), S(25), S(0))
    glVertex3f(S(-45), S(25), S(0))
    glVertex3f(S(-45), S(-25), S(15))
    glVertex3f(S(45), S(-25), S(15))
    glVertex3f(S(45), S(25), S(15))
    glVertex3f(S(-45), S(25), S(15))
    glEnd()

    # --- Cabin ---
    glColor3f(*cabin_color)
    glBegin(GL_QUADS)
    glVertex3f(S(-25), S(-20), S(20))
    glVertex3f(S(25), S(-20), S(20))
    glVertex3f(S(25), S(20), S(20))
    glVertex3f(S(-25), S(20), S(20))
    glVertex3f(S(-20), S(-15), S(25))
    glVertex3f(S(20), S(-15), S(25))
    glVertex3f(S(20), S(15), S(25))
    glVertex3f(S(-20), S(15), S(25))
    glEnd()
    glPopMatrix()

    # --- Backlights ---
    backlight_positions = [(-45, 15, 20), (-45, -15, 20)]
    glColor3f(*backlight_color)
    for bx, by, bz in backlight_positions:
        glPushMatrix()
        glTranslatef(S(bx)+x, S(by)+y, S(bz)+z)
        glutSolidCube(S(6))
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



def spawn_obstacles():
    global obstacle_positions
    obstacle_positions.clear()
    track_radius_outer = GRID_LENGTH - 100
    road_width = 60
    track_center_radius = track_radius_outer - road_width / 2

    for _ in range(num_obstacles):
        angle = random.uniform(0, 2*math.pi)
        r = track_center_radius
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        obstacle_positions.append((x, y))


def draw_obstacles():
    glColor3f(1, 0, 0)  # red cubes
    for x, y in obstacle_positions:
        glPushMatrix()
        glTranslatef(x, y, obstacle_size / 2)  # lift cube so it sits on track
        glutSolidCube(obstacle_size)
        glPopMatrix()



def check_obstacle_collision():
    global life, game_state, car_x, car_y, obstacles_hit, invisible_active
    for idx, (ox, oy) in enumerate(obstacle_positions):
        dx = car_x - ox
        dy = car_y - oy
        dist2 = dx*dx + dy*dy
        if dist2 < (obstacle_size-2)**2:  # within obstacle radius
            if invisible_active:
                continue  # Ignore collision if invisible
            if idx not in obstacles_hit:  # only reduce life once
                life -= 1
                obstacles_hit.add(idx)
                if life <= 0:
                    life = 0
                    game_state = False
            break
        else:
            # Remove from hit set once car leaves obstacle
            if idx in obstacles_hit:
                obstacles_hit.remove(idx)








# --- Rain ---
def draw_rain():
    brightness = sum(sky_color)/3
    rain_col = (0,0,1) if brightness > 0.5 else (0.7,0.7,1.0)
    glColor3f(*rain_col)

    drop_width = 0.5
    drop_height = 5

    for x, y, z in raindrops:
        glBegin(GL_QUADS)
        glVertex3f(x - drop_width/2, y, z)
        glVertex3f(x + drop_width/2, y, z)
        glVertex3f(x + drop_width/2, y, z - drop_height)
        glVertex3f(x - drop_width/2, y, z - drop_height)
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
        tangent_angle_deg = math.degrees(angle) + 90

        glPushMatrix()
        glTranslatef(x_center, y_center, arrow_z)
        glRotatef(tangent_angle_deg, 0, 0, 1)

        # Draw arrow as thin quad
        glBegin(GL_QUADS)
        glVertex3f(0, -arrow_width / 2, 0)
        glVertex3f(arrow_length, -arrow_width / 2, 0)
        glVertex3f(arrow_length, arrow_width / 2, 0)
        glVertex3f(0, arrow_width / 2, 0)
        glEnd()

        glPopMatrix()


def check_checkpoint_collision():
    global boost_active, boost_timer, car_speed
    for (cx, cy) in checkpoint_positions:
        dx = car_x - cx
        dy = car_y - cy
        if dx*dx + dy*dy < 10*10:   # within radius 8
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
    global show_instruction, car_angle, game_state, paused

    if not game_state or paused:
        return  # Stop handling keys if game is over or paused

    if key == GLUT_KEY_LEFT:
        car_angle += turn_speed
        show_instruction = False
    elif key == GLUT_KEY_RIGHT:
        car_angle -= turn_speed





def keyboard_listener(key, x, y):
    global target_sky_color, paused
    if key == b'd':
        target_sky_color = [1.0, 1.0, 1.0]
    elif key == b'n':
        target_sky_color = [0.0, 0.0, 0.0]
    elif key == b'r':
        restart_game()
    elif key == b'p':  # toggle pause
        paused = not paused


def restart_game():
    global car_x, car_y, car_angle, car_speed, fuels, fuel_consumed_distance
    global boost_active, boost_timer, slowdown_active, slowdown_timer, game_state
    global fuel_pickups, checkpoint_angles, checkpoint_positions
    global speedbreaker_angles, speedbreaker_positions, blink_counter
    global track_entered, game_started, up_press_count
    global score, life  # <-- add life here
    global invisible_active, invisible_timer  # <-- reset invisibility

    score = 0  # reset coins collected
    life = 5   # reset life back to 5

    car_x, car_y, car_angle = 0, 0, 0
    car_speed = normal_speed
    fuels = 50
    fuel_consumed_distance = 0

    boost_active, boost_timer = False, 0
    slowdown_active, slowdown_timer = False, 0
    invisible_active, invisible_timer = False, 0   # <-- reset invisibility
    game_state = True
    track_entered = False
    game_started = False
    blink_counter = 0

    up_press_count = 0  # <-- reset UP arrow presses

    # Respawn pickups, checkpoints, speed breakers, coins
    fuel_pickups.clear()
    spawn_fuel_pickups(8)
    spawn_checkpoints()
    spawn_speedbreakers()
    spawn_coins(num_coins)
    spawn_invisible_powerups()







def draw_coin(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z + 5)  # float above the track
    glColor3f(1, 0.84, 0)      # gold
    gluSphere(quadric, coin_radius, 20, 20)  # radius, slices, stacks
    glPopMatrix()












def draw_coins():
    for x, y, z in coin_pickups:
        draw_coin(x, y, z)








def check_coin_collection():
    global coin_pickups, score, num_coins
    new_coins = []
    for x, y, z in coin_pickups:
        dx = car_x - x
        dy = car_y - y
        if dx*dx + dy*dy < 5*5:  # radius 5
            score += coin_value
            # Respawn the collected coin at a new random position
            angle = random.uniform(0, 2*math.pi)
            r = random.uniform(track_radius_outer - road_width + 5, track_radius_outer - 5)
            new_x = r * math.cos(angle)
            new_y = r * math.sin(angle)
            new_coins.append((new_x, new_y, z))
        else:
            new_coins.append((x, y, z))
    coin_pickups[:] = new_coins







# --- Car movement ---
def process_car_movement():
    global car_x, car_y, fuel_consumed_distance, fuels, game_state, game_started, car_speed

    if not game_state:
        return  # Stop car movement if game over

    rad = math.radians(car_angle)
    old_x, old_y = car_x, car_y

    # Update speed based on score, if not boosting or slowing down
    if not boost_active and not slowdown_active:
        car_speed = base_speed + score * score_speed_factor
        if car_speed > max_speed:
            car_speed = max_speed

    # Car always moves forward
    car_x += car_speed * math.cos(rad)
    car_y += car_speed * math.sin(rad)
    game_started = True  # start checking for leaving track

    # --- Fuel consumption ---
    dx = car_x - old_x
    dy = car_y - old_y
    distance = math.hypot(dx, dy)

    fuel_consumed_distance += distance
    if fuel_consumed_distance >= 50:
        fuels = max(fuels - 1, 0)
        fuel_consumed_distance = 0

    if fuels <= 0:
        fuels = 0
        game_state = False  # out of fuel => game over


def draw_sky_far(color_top=(0.0,0.5,1.0), color_bottom=(0.5,0.8,1.0)):
    glPushMatrix()
    glLoadIdentity()  # ignore camera transforms

    # Place quad very far on Z-axis
    z_far = -1000  # far behind the scene
    glBegin(GL_QUADS)
    # top
    glColor3f(*color_top)
    glVertex3f(-1000, -1000, z_far)
    glVertex3f( 1000, -1000, z_far)

    # bottom
    glColor3f(*color_bottom)
    glVertex3f( 1000,  1000, z_far)
    glVertex3f(-1000,  1000, z_far)
    glEnd()

    glPopMatrix()








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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,1000,800)
    draw_sky_far(color_top=sky_color, color_bottom=sky_color)

    setupCamera()
    draw_grid()
    draw_track()
    draw_rain()
    draw_checkpoints()
    draw_speedbreakers()
    if sky_color[0]<0.5:
        draw_stars()
    draw_fuel_pickups()
    draw_coins()
    draw_obstacles()
    glPushMatrix()
    draw_invisible_powerups()

    glTranslatef(car_x, car_y, 0)
    glRotatef(car_angle,0,0,1)
    draw_car(0,0,0)
    glPopMatrix()
    draw_text(10,700,f"Life x {life}",color=(0,0,1))
    draw_text(450,700,f"Fuel Left x {fuels}",color=(0,0.9,0))
    draw_text(900,700,f"Coins: {score}",color=(1,1,0))

    if game_state and show_instruction and (blink_counter//60)%2==0:
        draw_text(400,500,"<--- TAKE LEFT", color=(1,1,0))
    if paused:
        draw_text(470, 450, "PAUSED", color=(1, 1, 0))



    # Display Game Over
    if game_state==False:
        draw_text(470,490,"GAME OVER", color=(1,0,0))
        draw_text(420,460,'PRESS "R" TO RESTART',color=(0,0.85,0))
        draw_text(465,430,f'TOTAL SCORE:{score}',color=(1,1,0))

        

    glutSwapBuffers()


# --- Idle ---
def idle():
    global blink_counter, sky_color, boost_active, boost_timer, car_speed
    global slowdown_active, slowdown_timer, paused, invisible_active, invisible_timer

    if paused:
        # Only redraw the screen, don't update game state
        glutPostRedisplay()
        return

    if not game_state:
        glutPostRedisplay()
        return

    # --- Smooth sky color transition ---
    for i in range(3):
        delta = target_sky_color[i] - sky_color[i]
        sky_color[i] += delta * 0.02

    # --- Car movement and fuel ---
    process_car_movement()
    check_car_on_track()

    # --- Update counters ---
    blink_counter += 1

    # --- Check collections ---
    check_fuel_collection()
    check_checkpoint_collision()
    check_speedbreaker_collision()
    check_obstacle_collision()
    update_rain()
    check_coin_collection()
    check_invisible_collection()

    # --- Handle boost timer ---
    if boost_active:
        boost_timer -= 1
        if boost_timer <= 0:
            boost_active = False
            car_speed = base_speed + score * score_speed_factor
            if car_speed > max_speed:
                car_speed = max_speed

    # --- Handle slowdown timer ---
    if slowdown_active:
        slowdown_timer -= 1
        if slowdown_timer <= 0:
            slowdown_active = False
            car_speed = base_speed + score * score_speed_factor
            if car_speed > max_speed:
                car_speed = max_speed

    # --- Handle invisibility timer ---
    if invisible_active:
        invisible_timer -= 1
        if invisible_timer <= 0:
            invisible_active = False

    # --- Redraw ---
    glutPostRedisplay()











# --- Main ---
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000,730)
    glutInitWindowPosition(150,0)
    glutCreateWindow(b"Rapid Rush")
    spawn_fuel_pickups(8)
    spawn_checkpoints()
    spawn_speedbreakers()
    spawn_obstacles()
    spawn_coins()
    spawn_invisible_powerups()

    glEnable(GL_DEPTH_TEST)
    glutDisplayFunc(showScreen)
    glutSpecialFunc(special_key_pressed)
    glutKeyboardFunc(keyboard_listener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()

