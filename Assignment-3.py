from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


import math
import random as r
# Camera-related variables
camera_pos = (0,500,500)

fovY = 120  # Field of view
GRID_LENGTH = 650  # Length of grid lines
#rand_var = 423
player_life=5
score=0
missed_bullet=0
horizontal_view_angle=0
vertical_view_angle=500
player_pos=[0,0,0]
player_angle=0
gun_lower_base=25
gun_length=50
gun_point_x=player_pos[0]+gun_lower_base+gun_length
gun_point_y=player_pos[1]+gun_lower_base+gun_length
min_x=-GRID_LENGTH+21
max_x=GRID_LENGTH-21
min_y=-GRID_LENGTH-100
max_y=550-21
enemy_list=[]
enemy_status=True
enemy_body_radius=40
enemy_head_radius=15
enemy_grow_or_shrink=1
enemy_pulse=0.1
collided_enemies=[]
body_quadric=gluNewQuadric()
head_quadric=gluNewQuadric()
bullets=[]
game_state=True
rand_enemy_pos=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
cheat_mode_status=False
auto_shooter=0
view_type='3rd'
camera_rotate=False



def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
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





def draw_player():
    global player_pos,player_angle,game_state
    glPushMatrix()
    glTranslatef(player_pos[0],player_pos[1],player_pos[2])

    if game_state==True:
        glRotatef(player_angle,0,0,1)
    else:
        glRotatef(90,1,0,0)




    #PLAYER BODY
    glColor3f(0, 0, 1)
    gluCylinder(gluNewQuadric(), 3, 10, 30, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    glTranslatef(25, 0, 0) 
    gluCylinder(gluNewQuadric(), 3, 10, 30, 10, 10)

    glTranslatef(-2,-1,40)
    glColor3f(0,0.55,0)
    glutSolidCube(22)

    glTranslatef(-21,1,0)
    glColor3f(0,0.55,0)
    glutSolidCube(22)

    glTranslatef(1,0,20)
    glColor3f(0,0.55,0)
    glutSolidCube(25)

    glTranslatef(19,0,-0.6)
    glColor3f(0,0.55,0)
    glutSolidCube(25)

    glTranslatef(-8,0,22)
    glColor3f(0,0,0)
    gluSphere(gluNewQuadric(), 13, 10, 10)


    glTranslatef(20, 40, -21) 
    glColor3f(1, 1, 1)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 8, 30, 10, 10)

    glTranslatef(-45, 0, 0) 
    glColor3f(1, 1, 1)
    glRotatef(-1, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 8, 30, 10, 10)

    glTranslatef(25, 0, -20) 
    glColor3f(0.75, 0.75, 0.75)
    glRotatef(-1, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 3, 8, 50, 10, 10)
    glPopMatrix()

    

    #Enemy

def draw_enemies():
    for (x,y,z) in enemy_list:
        create_enemies(x,y,z)


def create_enemies(x,y,z):
    global body_quadric,head_quadric,enemy_body_radius,enemy_head_radius

    glPushMatrix()
    glTranslatef(x,y,z)
    glColor3f(1.0,0.16,0.16)
    gluSphere(body_quadric, enemy_body_radius, 100, 100)
    


    glPushMatrix()
    glTranslatef(0,0,enemy_body_radius+5)
    glColor3f(0.0,0.0,0.0)
    gluSphere(head_quadric, enemy_head_radius, 100, 100)
    glPopMatrix()
    glPopMatrix()

def enemies_chase_player():
    global player_pos,enemy_list,player_life,collided_enemies
    speed=0.1
    collision_dist=50
    remove_enemies=[]
    for i in range(len(enemy_list)):
        x,y,z=enemy_list[i]

        diff_in_x=player_pos[0]-x
        diff_in_y=player_pos[1]-y
        diff_in_z=player_pos[2]-z


        player_enemy_distance=math.sqrt(diff_in_x**2+diff_in_y**2+diff_in_z**2)
        if player_enemy_distance==0:
            pass
        norm_x=diff_in_x/player_enemy_distance
        norm_y=diff_in_y/player_enemy_distance
        norm_z=diff_in_z/player_enemy_distance

        enemy_list[i][0]+=norm_x*speed
        enemy_list[i][1]+=norm_y*speed
        enemy_list[i][2]+=norm_z*speed

        if player_enemy_distance<collision_dist:
            if i not in collided_enemies:
                player_life-=1
                print(f'Remaining Player Life: {player_life}')
                remove_enemies.append(i)

        else:
            if i in collided_enemies:
                collided_enemies.remove(i)
    
    remove_enemies=sorted(set(remove_enemies),reverse=True)
    for i in remove_enemies:
        enemy_list.pop(i)
        new_ex=r.randint(-550,550)
        new_ey=r.randint(-550,500)
        new_ez=0
        enemy_list.append([new_ex,new_ey,new_ez])

def reset_game():
    global player_angle,player_pos,bullets,enemy_list,player_life,score,missed_bullet,game_state,cheat_mode_status

    game_state=True
    player_angle=0

    player_pos[:]=[0,0,0]
    
    player_life=5
    score=0
    missed_bullet=0
    bullets.clear()
    assign_random_pos_for_enemies(5)
    cheat_mode_status=False
    
    








def assign_random_pos_for_enemies(num_of_enem):
    global enemy_list
    enemy_list=[]
    for i in range(num_of_enem):
        x=r.randint(-500,500)
        y=r.randint(-500,500)
        z=0
        enemy_list.append([x,y,z])



def cheat_mode():
    global enemy_list,player_pos,rand_enemy_pos,cheat_mode_status
    cheat_mode_status=not cheat_mode_status
    if cheat_mode_status==True:
        enemy_list.clear()
        random_dist=500
        for del_x,del_y in rand_enemy_pos:
            new_x=player_pos[0]+del_x*random_dist
            new_y=player_pos[1]+del_y*random_dist
            enemy_list.append([new_x,new_y,0])


    








    
    



    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

    


def keyboardListener(key, x, y):
    global player_pos,player_angle,game_state,camera_rotate

    if key == b'r' and game_state==False:
        reset_game()
        glutPostRedisplay()
        return 




    if game_state==False:
        return
    rad=math.radians(player_angle)

    forward_dir=[math.cos(rad),math.sin(rad)]

    
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)

    


    if key == b'w':
        if rad==0:
            player_pos[1]+=10
        else:
            if 0<rad<math.pi/2:
                player_pos[0]-=10
                player_pos[1]+=10
            elif rad==math.pi/2:
                player_pos[0]-=10
            elif math.pi/2<rad<math.pi:
                player_pos[0]-=10
                player_pos[1]-=10
            elif rad==math.pi:
                player_pos[1]-=10
            elif math.pi<rad<3*math.pi/2:
                player_pos[0]+=10
                player_pos[1]-=10
            elif rad==3*math.pi/2:
                player_pos[0]+=10
            elif 3*math.pi/2<rad<2*math.pi:
                player_pos[0]+=10
                player_pos[1]+=10
                

        


       
        



    # # Move backward (S key)
    if key == b's':
        if rad==0:
            player_pos[1]-=10
        else:
            if 0<rad<math.pi/2:
                player_pos[0]+=10
                player_pos[1]-=10
            elif rad==math.pi/2:
                player_pos[0]+=10
            elif math.pi/2<rad<math.pi:
                player_pos[0]+=10
                player_pos[1]+=10
            elif rad==math.pi:
                player_pos[1]+=10
            elif math.pi<rad<3*math.pi/2:
                player_pos[0]-=10
                player_pos[1]+=10
            elif rad==3*math.pi/2:
                player_pos[0]-=10
            elif 3*math.pi/2<rad<2*math.pi:
                player_pos[0]-=10
                player_pos[1]-=10
            
        

        



        
        
        
       
        
        

    # # Rotate gun left (A key)
    if key == b'a':
        player_angle+=5
        player_angle=player_angle%360
        
        print(player_angle)

    # # Rotate gun right (D key)
    if key == b'd':
        player_angle-=5
        player_angle=player_angle%360
        print(player_angle)

    # # Toggle cheat mode (C key)
    if key == b'c':
        if game_state!=False:
            cheat_mode()

    # # Toggle cheat vision (V key)
    if key == b'v':
        if cheat_mode_status==True and view_type=='1st':
            
            camera_rotate=not camera_rotate
    






    # # Reset the game if R key is pressed
    



    clip_more_x=50
    clip_more_y=50


    player_pos[0]=max(min_x+clip_more_x,min(max_x-clip_more_x,player_pos[0]))
    player_pos[1]=max(min_y+clip_more_y,min(max_y-clip_more_y,player_pos[1]))

    glutPostRedisplay()


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos,horizontal_view_angle,vertical_view_angle,camera_up,camera_down,game_state

    if game_state==False:
        return

    x, y, z = camera_pos
    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP:
        vertical_view_angle-=3
        


    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN:
        vertical_view_angle+=3



    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        horizontal_view_angle += 1  # Small angle decrement for smooth movement

        
    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        horizontal_view_angle -= 1  # Small angle increment for smooth movement
    
    
    camera_pos = (x, y, z)

    glutPostRedisplay()
def mouseListener(button, state, x, y):
    global view_type
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        shoot()
        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if view_type=='3rd':
            view_type='1st'
        else:
            view_type='3rd'

def set_view():
    global view_type, player_pos, player_angle, vertical_view_angle,camera_pos,camera_rotate
    step=30
    if view_type == '3rd':
        # 3rd-person
        
        
        
            cam_x, cam_y, cam_z = camera_pos
            look_x, look_y, look_z = 0, 0, 0

    else:
        
       #1st person
        if cheat_mode_status==True:
            cam_x = player_pos[0]+10
            cam_y = player_pos[1]
            cam_z = player_pos[2] + 100  

            look_x=cam_x
            look_y=cam_y+step
            look_z=cam_z
        else:
            cam_x = player_pos[0]+10
            cam_y = player_pos[1]
            cam_z = player_pos[2] + 100  

            look_x=cam_x
            look_y=cam_y+step
            look_z=cam_z

            
            rad = math.radians(player_angle)
            step = 100  
            if rad == 0:
                look_x = cam_x
                look_y = cam_y + step
            elif 0 < rad < math.pi / 2:
                look_x = cam_x - step
                look_y = cam_y + step
            elif rad == math.pi / 2:
                look_x = cam_x - step
                look_y = cam_y
            elif math.pi / 2 < rad < math.pi:
                look_x = cam_x - step
                look_y = cam_y - step
            elif rad == math.pi:
                look_x = cam_x
                look_y = cam_y - step
            elif math.pi < rad < 3*math.pi/2:
                look_x = cam_x + step
                look_y = cam_y - step
            elif rad == 3*math.pi/2:
                look_x = cam_x + step
                look_y = cam_y
            elif 3*math.pi/2 < rad < 2*math.pi:
                look_x = cam_x + step
                look_y = cam_y + step
        

        

        # assigning camera position
    gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, 0, 0, 1)



        







def shoot():
    global bullets,player_angle,player_pos
    print(f'Player Bullet: Fired!')
    rad=math.radians(player_angle)
    offset=30
    bullet_x=11+player_pos[0]+ math.sin(rad) *offset
    bullet_y=player_pos[1]+math.cos(rad) *offset
    bullet_z=player_pos[2]+50

    bullets.append({'pos':[bullet_x,bullet_y,bullet_z],'angle':player_angle})

def move_bullets():
    global bullets,enemy_list,score,missed_bullet,cheat_mode_status
    speed = 5  # how fast the bullet moves per frame
    remove_bullets = []
    remove_enemies=[]

    for i, b in enumerate(bullets):
        rad = math.radians(b['angle'])
        # Move in the same direction as forward
        if rad == 0:
            b['pos'][1] += speed
        elif 0 < rad < math.pi/2:
            b['pos'][0] -= speed
            b['pos'][1] += speed
        elif rad == math.pi/2:
            b['pos'][0] -= speed
        elif math.pi/2 < rad < math.pi:
            b['pos'][0] -= speed
            b['pos'][1] -= speed
        elif rad == math.pi:
            b['pos'][1] -= speed
        elif math.pi < rad < 3*math.pi/2:
            b['pos'][0] += speed
            b['pos'][1] -= speed
        elif rad == 3*math.pi/2:
            b['pos'][0] += speed
        elif 3*math.pi/2 < rad < 2*math.pi:
            b['pos'][0] += speed
            b['pos'][1] += speed
        if cheat_mode_status==False:
            for j,e in enumerate(enemy_list):
                if distance(b['pos'],e)<(enemy_body_radius + 45):
                    remove_bullets.append(i)
                    remove_enemies.append(j)
                    score+=1
        else:
            for j,e in enumerate(enemy_list):
                if distance(b['pos'],e)<(enemy_body_radius + 80):
                    remove_bullets.append(i)
                    remove_enemies.append(j)
                    score+=1



        # Remove bullets if they go too far
        x, y, z = b['pos']
        if x < min_x or x > max_x or y < min_y or y > max_y:
            remove_bullets.append(i)
            missed_bullet+=1
            print(f'Bullet missed: {missed_bullet}')

    #remove the enemy hit with the bullet
    remove_bullets=sorted(set(remove_bullets),reverse=True)
    for i in remove_bullets:
        bullets.pop(i)

    remove_enemies=sorted(set(remove_enemies),reverse=True)
    for i in remove_enemies:
        x,y,z=enemy_list[i]
        enemy_list.pop(i)
        if cheat_mode_status==True:
            
            del_x=x-player_pos[0]
            del_y=y-player_pos[1]

            rand_dist=r.randint(-50,50)
            new_ex=player_pos[0]+del_x+rand_dist
            new_ey=player_pos[1]+del_y+rand_dist


        else:
            new_ex=r.randint(-550,550)
            new_ey=r.randint(-550,500)
        enemy_list.append([new_ex,new_ey,0])


def draw_bullets():
    for b in bullets:
        x, y, z = b['pos']
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(0,0,0)
        glutSolidCube(10)
        glPopMatrix()

def distance(d1,d2):
    val=math.sqrt((d1[0]-d2[0])**2 + (d1[1]-d2[1])**2 + (d1[2]-d2[2])**2)
    return val


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, 1.25, 0.1, 2500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    #x, y, z = camera_pos
    # Position the camera and set its orientation
    


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global enemy_body_radius,enemy_head_radius,enemy_grow_or_shrink,enemy_pulse,game_state,player_life,missed_bullet,cheat_mode_status,player_angle,auto_shooter
    if player_life==0 or missed_bullet==10:
        game_state=False
        glutPostRedisplay()
        return 

    if enemy_body_radius>=48:
        enemy_grow_or_shrink=-1
    elif enemy_body_radius<=32:
        enemy_grow_or_shrink=1
    enemy_body_radius+=enemy_pulse*enemy_grow_or_shrink
    enemy_head_radius=enemy_body_radius*0.375
    move_bullets()
    enemies_chase_player()
    #rotate the player
    if cheat_mode_status==True:
        player_angle+=4
        player_angle%=360
        auto_shooter+=0.1
        if auto_shooter>=5:
            shoot()
            auto_shooter=0



    glutPostRedisplay()


def draw_floor():
    step_size=(2*GRID_LENGTH)//13
    row_count=0
    for i in range(-GRID_LENGTH,GRID_LENGTH,step_size):
        col_count=0
        row_count+=1
        for j in range(-GRID_LENGTH,GRID_LENGTH,step_size):
            col_count+=1
            if row_count%2!=0:
                if col_count%2!=0:
                    glBegin(GL_QUADS)
                    glColor3f(1.0,1.0,1.0)
                    glVertex3f(i, j, 0)
                    glVertex3f(i, j-step_size, 0)
                    glVertex3f(i+step_size, j-step_size, 0)
                    glVertex3f(i+step_size, j, 0)
                    glEnd()

                else:
                    glBegin(GL_QUADS)
                    glColor3f(0.7, 0.5, 0.95)
                    glVertex3f(i, j, 0)
                    glVertex3f(i, j-step_size, 0)
                    glVertex3f(i+step_size, j-step_size, 0)
                    glVertex3f(i+step_size, j, 0)
                    glEnd()
                    
            else:
                if col_count%2!=0:
                    glBegin(GL_QUADS)
                    glColor3f(0.7, 0.5, 0.95)
                    glVertex3f(i, j, 0)
                    glVertex3f(i, j-step_size, 0)
                    glVertex3f(i+step_size, j-step_size, 0)
                    glVertex3f(i+step_size, j, 0)
                    glEnd()
                else:
                    glBegin(GL_QUADS)
                    glColor3f(1.0,1.0,1.0)
                    glVertex3f(i, j, 0)
                    glVertex3f(i, j-step_size, 0)
                    glVertex3f(i+step_size, j-step_size, 0)
                    glVertex3f(i+step_size, j, 0)
                    glEnd()
def draw_walls():
    #WALLS

    #BACK WALL
    glBegin(GL_QUADS)
    glColor3f(0.8,0.8,0.8)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH-100,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH-100,0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH-100,100)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH-100,100)
    glEnd()


    #RIGHT WALL
    glBegin(GL_QUADS)
    glColor3f(0.0,1.0,0.0)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH-100,0)
    glVertex3f(-GRID_LENGTH,550,0)
    glVertex3f(-GRID_LENGTH,550,100)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH-100,100)
    glEnd()

    #LEFT WALL
    glBegin(GL_QUADS)
    glColor3f(0.0,0.0,1.0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH-100,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH-100,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH-100,100)
    glVertex3f(GRID_LENGTH,GRID_LENGTH-100,100)
    glEnd()



    #FRONT WALL
    glBegin(GL_QUADS)
    glColor3f(1.0,1.0,1.0)
    glVertex3f(-GRID_LENGTH,550,0)
    glVertex3f(GRID_LENGTH,550,0)
    glVertex3f(GRID_LENGTH,550,100)
    glVertex3f(-GRID_LENGTH,550,100)
    glEnd()

def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    global game_state, score, player_life, missed_bullet
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    setupCamera()  # Configure camera perspective
    glLoadIdentity()  # Reset modelview matrix
    set_view()
    glViewport(0, 0, 1000, 800)  # Set viewport size
    

    

    # glRotatef(horizontal_view_angle,0,0,1)
    
    if game_state==False:
        glPushMatrix()
        draw_floor()
        draw_walls()
        draw_player()
        draw_text(10,700,f'Game is Over. Your Score is {score}')
        draw_text(10,665,'Press "R" to RESTART the Game.')
        glPopMatrix()
    else:
        glPushMatrix()
        draw_floor()
        draw_walls()
        draw_player()
        draw_enemies()
        draw_bullets()
        draw_text(10, 700, f"Player Life Remaining: {player_life}")
        draw_text(10, 675, f"Game Score: {score}")
        draw_text(10, 650, f"Player Bullets Missed: {missed_bullet}")
        glPopMatrix()
    
    
    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(50, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window
    assign_random_pos_for_enemies(5)
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
