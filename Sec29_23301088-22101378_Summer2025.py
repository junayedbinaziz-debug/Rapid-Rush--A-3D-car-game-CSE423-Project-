from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
fuels=0
score=0


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
fuels=0
score=0
life=5
camera_angle = 0  # in degrees
camera_radius = 500  # distance from center

import math





def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18,color=(1,1,1)):
    glColor3f(*color)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_shapes():

    # glPushMatrix()  # Save the current matrix state
    # glColor3f(1, 0, 0)
    # glTranslatef(0, 0, 0)  
    # glutSolidCube(60) # Take cube size as the parameter
    # glTranslatef(0, 0, 100) 
    # glColor3f(0, 1, 0)
    # glutSolidCube(60) 

    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks
    
    glPushMatrix()


    glPopMatrix()  # Restore the previous matrix state


def draw_grid():
    glBegin(GL_QUADS)
    
    glColor3f(0, 1, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(0, -GRID_LENGTH, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(GRID_LENGTH, 0, 0)


    
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, -GRID_LENGTH, 0)

    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, 0, 0)
    glVertex3f(0, 0, 0)
    glVertex3f(0, GRID_LENGTH, 0)
    glEnd()

def draw_track():
    # Make track fit within GRID_LENGTH
    max_length = GRID_LENGTH * 2 - 50  # leave some margin
    max_width  = GRID_LENGTH * 2 - 50
    road_width = 60
    segments   = 20  # smoothness of corners

    halfL = max_length / 2
    halfW = max_width / 2
    innerL = halfL - road_width
    innerW = halfW - road_width

    glColor3f(0.5, 0.5, 0.5)  # gray track

    

    # --- Rounded corners ---
    def draw_corner(cx, cy, start_angle, end_angle):
        for i in range(segments):
            a1 = math.radians(start_angle + (end_angle - start_angle) * i / segments)
            a2 = math.radians(start_angle + (end_angle - start_angle) * (i + 1) / segments)

            # Outer points
            x_outer1 = cx + halfL * math.cos(a1)
            y_outer1 = cy + halfW * math.sin(a1)
            x_outer2 = cx + halfL * math.cos(a2)
            y_outer2 = cy + halfW * math.sin(a2)

            # Inner points
            x_inner1 = cx + innerL * math.cos(a1)
            y_inner1 = cy + innerW * math.sin(a1)
            x_inner2 = cx + innerL * math.cos(a2)
            y_inner2 = cy + innerW * math.sin(a2)

            glBegin(GL_QUADS)
            glVertex3f(x_outer1, y_outer1, 0)
            glVertex3f(x_outer2, y_outer2, 0)
            glVertex3f(x_inner2, y_inner2, 0)
            glVertex3f(x_inner1, y_inner1, 0)
            glEnd()

    # Draw all 4 corners
    draw_corner(0, 0, 0, 90)    # Top-right
    draw_corner(0, 0, 90, 180)  # Top-left
    draw_corner(0, 0, 180, 270) # Bottom-left
    draw_corner(0, 0, 270, 360) # Bottom-right



def draw_car(x=0, y=0, z=0):
    """
    Draws a simple car at position (x, y, z) without using glScale

    
    """

    # --- Wheels ---
    glColor3f(0, 0, 0)  # black wheels
    wheel_positions = [
        (50, 33, -20),   # front-right
        (-55, 33, -20),  # front-left
        (50, -23, -20),  # back-right
        (-55, -23, -20), # back-left
    ]

    for wx, wy, wz in wheel_positions:
        glPushMatrix()
        glTranslatef(wx, wy, wz)
        glRotatef(90, 1, 0, 0)  # rotate cylinder to be horizontal
        gluCylinder(gluNewQuadric(), 15, 15, 10, 10, 10)
        glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, z)  # move car to desired position

    # --- Car body ---
    glColor3f(0, 0, 1)  # red car
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-60, -30, -20)
    glVertex3f(60, -30, -20)
    glVertex3f(60, 30, -20)
    glVertex3f(-60, 30, -20)
    # Back face
    glVertex3f(-60, -30, 20)
    glVertex3f(60, -30, 20)
    glVertex3f(60, 30, 20)
    glVertex3f(-60, 30, 20)
    # Top face
    glVertex3f(-60, 30, -20)
    glVertex3f(60, 30, -20)
    glVertex3f(60, 30, 20)
    glVertex3f(-60, 30, 20)
    # Bottom face
    glVertex3f(-60, -30, -20)
    glVertex3f(60, -30, -20)
    glVertex3f(60, -30, 20)
    glVertex3f(-60, -30, 20)
    # Left face
    glVertex3f(-60, -30, -20)
    glVertex3f(-60, 30, -20)
    glVertex3f(-60, 30, 20)
    glVertex3f(-60, -30, 20)
    # Right face
    glVertex3f(60, -30, -20)
    glVertex3f(60, 30, -20)
    glVertex3f(60, 30, 20)
    glVertex3f(60, -30, 20)
    glEnd()

     # --- Slanted cabin ---
    glColor3f(0, 0.5, 1)
    glBegin(GL_QUADS)
    # Bottom rectangle of cabin
    glVertex3f(-40, -25, 20)
    glVertex3f(40, -25, 20)
    glVertex3f(40, 25, 20)
    glVertex3f(-60, 25, 20)

    # Roof rectangle
    glVertex3f(-30, -20, 50)
    glVertex3f(30, -20, 50)
    glVertex3f(30, 20, 50)
    glVertex3f(-30, 20, 50)

    # Slanted front
    glVertex3f(-60, -25, 20)
    glVertex3f(40, -25, 20)
    glVertex3f(30, -20, 50)
    glVertex3f(-30, -20, 50)

    # Slanted back
    glVertex3f(-60, 25, 20)
    glVertex3f(40, 25, 20)
    glVertex3f(30, 20, 50)
    glVertex3f(-30, 20, 50)

    # Right slope
    glVertex3f(-60, -25, 20)
    glVertex3f(-40, 25, 20)
    glVertex3f(-30, 20, 50)
    glVertex3f(-30, -20, 50)

    # Left slope
    glVertex3f(40, -25, 20)
    glVertex3f(40, 25, 20)
    glVertex3f(30, 20, 50)
    glVertex3f(30, -20, 50)
    glEnd()

    

    glPopMatrix()







def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    global camera_angle, camera_pos, camera_radius, camera_height

    # Rotate camera left
    if key == GLUT_KEY_LEFT:
        camera_angle -= 5  # degrees

    # Rotate camera right
    if key == GLUT_KEY_RIGHT:
        camera_angle += 5  # degrees

    # Move camera up
    if key == GLUT_KEY_UP:
        camera_pos = (camera_pos[0], camera_pos[1], camera_pos[2] + 10)

    # Move camera down
    if key == GLUT_KEY_DOWN:
        camera_pos = (camera_pos[0], camera_pos[1], camera_pos[2] - 10)

    # Calculate camera X,Y from angle
    cam_x = camera_radius * math.cos(math.radians(camera_angle))
    cam_y = camera_radius * math.sin(math.radians(camera_angle))
    cam_z = camera_pos[2]  # keep height

    camera_pos = (cam_x, cam_y, cam_z)



def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
        # if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    x, y, z = camera_pos
    gluLookAt(x, y, z,  # camera position
              0, 0, 0,  # look at center of track
              0, 0, 1)  # up vector



def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
    glPointSize(20)
    glBegin(GL_POINTS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Draw the grid (game floor)
    

    # Display game info text at a fixed screen position
    draw_text(10, 700, f"Life x {life}",color=(0,0,1))
    draw_text(450, 700, f"Fuel Left x {fuels}",color=(0,0.9,0))
    draw_text(900, 700, f"Coins: {score}",color=(1,1,0))

    draw_grid()
    draw_track()
    draw_car()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 730)  # Window size
    glutInitWindowPosition(150, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()

