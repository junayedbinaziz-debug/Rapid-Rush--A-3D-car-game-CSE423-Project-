from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
import random as r
import time
prev_time=time.time()
diamond_x=r.randint(20,480)
diamond_y=455
diamond_pos=[[diamond_x-12,diamond_y-12],[diamond_x,diamond_y],[diamond_x+12,diamond_y-12],[diamond_x,diamond_y-24]]
catcher_pos=[[180,25],[308,25],[296,10],[195,10]]
diamond_r=r.uniform(0.3,1.0)
diamond_g=r.uniform(0.3,1.0)
diamond_b=r.uniform(0.3,1.0)
diamond_color=[diamond_r,diamond_g,diamond_b]
speed=60
catcher_state=True
score=0
game_state=True
catcher_speed=60
catcher_left=False
catcher_right=False
W_Width, W_Height = 500,500

def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x 
    b = W_Height- y 
    return a,b

def plot_pixel(x,y):
    glBegin(GL_POINTS)
    if (240<=x<=271) and (458<=y<=490): # colour of pause/play button (yellow)
        glColor3f(1.0,0.75,0.0)
    elif (458<=x<=487) and (460<=y<=490): # colour of close button (red)
        glColor3f(1.0,0.0,0.0)
    elif (10<=x<=40) and (460<=y<=490): # colour of restart button (teal)
        glColor3f(0.0,0.65,0.65)
    glVertex2f(x,y)
    glEnd()


def check_zone(x0,y0,x1,y1,og_zone,new_zone):
    dx=x1-x0
    dy=y1-y0
    if dx>0 and dy>0:
        if abs(dx)>abs(dy):
            og_zone=0
            new_zone=0
            MPL(x0,y0,x1,y1,og_zone,new_zone)
            
        else:
            og_zone=1
            new_zone=0
            x0,y0=y0,x0
            x1,y1=y1,x1
            MPL(x0,y0,x1,y1,og_zone,new_zone)

    elif dx<0 and dy>0:
        if abs(dy)>abs(dx):
            og_zone=2
            new_zone=0
            x0,y0=y0,-x0
            x1,y1=y1,-x1
            MPL(x0,y0,x1,y1,og_zone,new_zone)
        else:
            og_zone=3
            new_zone=0
            x0,y0=-x0,y0
            x1,y1=-x1,y1
            MPL(x0,y0,x1,y1,og_zone,new_zone)

    elif dx<0 and dy<0:
        if abs(dx)>abs(dy):
            og_zone=4
            new_zone=0
            x0,y0=-x0,-y0
            x1,y1=-x1,-y1
            MPL(x0,y0,x1,y1,og_zone,new_zone)


        else:
            og_zone=5
            new_zone=0
            x0,y0=-y0,-x0
            x1,y1=-y1,-x1
            MPL(x0,y0,x1,y1,og_zone,new_zone)


    else:
        if abs(dy)>abs(dx):
            og_zone=6
            new_zone=0
            x0,y0=-y0,x0
            x1,y1=-y1,x1
            MPL(x0,y0,x1,y1,og_zone,new_zone)


        else:
            og_zone=7
            new_zone=0
            x0,y0=x0,-y0
            x1,y1=x1,-y1
            MPL(x0,y0,x1,y1,og_zone,new_zone)

def MPL(x0,y0,x1,y1,og_zone,new_zone):
    x0,y0,x1,y1=int(x0),int(y0),int(x1),int(y1)
    dx=x1-x0
    dy=y1-y0
    iNE=2*dy-(2*dx)
    d=2*dy-dx
    iE=2*dy


    x,y=x0,y0

    for i in range(x0,x1+1):
        og_x,og_y=back_to_og_zone(x,y,og_zone)
        plot_pixel(og_x,og_y)
        if d>0:
            d+=iNE
            x+=1
            y+=1
                

        else:
            d+=iE
            x+=1
            

def back_to_og_zone(x,y,og_zone):
    if og_zone==0:
        return x,y
    elif og_zone==1:
        x,y=y,x
        return x,y
        
    elif og_zone==2:
        x,y=-y,x
        return x,y
    elif og_zone==3:
        x,y=-x,y
        return x,y
    elif og_zone==4:
        x,y=-x,-y
        return x,y
    elif og_zone==5:
        x,y=-y,-x
        return x,y
    elif og_zone==6:
        x,y=y,-x
        return x,y
    else:
        x,y=x,-y
        return x,y


    
            










def display():

    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    #draw pixel
    glPointSize(2.0)
    
    #LEFT-ARROW (RESTART BUTTON)
    #horizontal line
    check_zone(10,475,40,475,False,False)
    #upward point
    check_zone(10,475,25,490,False,False)
    #downward point
    check_zone(10,475,25,460,False,False)

    #PAUSE BUTTON
    if game_state==True:
        check_zone(240,490,240,460,False,False)
        check_zone(260,490,260,460,False,False)
    # PLAY BUTTON
    else:
        check_zone(240,489,240,458,False,False)
        check_zone(240,458,271,474,False,False)
        check_zone(271,474,240,489,False,False)


    #CLOSE BUTTON
    check_zone(458,490,487,460,False,False)
    check_zone(458,460,487,490,False,False)

    #DIAMOND
    glColor3f(diamond_color[0],diamond_color[1],diamond_color[2])
    check_zone(int(diamond_pos[0][0]),int(diamond_pos[0][1]),int(diamond_pos[1][0]),int(diamond_pos[1][1]),False,False)
    check_zone(int(diamond_pos[1][0]),int(diamond_pos[1][1]),int(diamond_pos[2][0]),int(diamond_pos[2][1]),False,False)
    check_zone(int(diamond_pos[2][0]),int(diamond_pos[2][1]),int(diamond_pos[3][0]),int(diamond_pos[3][1]),False,False)
    check_zone(int(diamond_pos[3][0]),int(diamond_pos[3][1]),int(diamond_pos[0][0]),int(diamond_pos[0][1]),False,False)
    


    #CATCHER BOWL
    if catcher_state==True:
        glColor3f(1.0,1.0,1.0)
    else:
        glColor3f(1.0,0.0,0.0)
    x1,x2,x3,x4=catcher_pos[0][0],catcher_pos[1][0],catcher_pos[2][0],catcher_pos[3][0]
    
    check_zone(x4,10,x3,10,False,False)
    check_zone(x3,10,x2,25,False,False)
    check_zone(x1,25,x2,25,False,False)
    check_zone(x1,25,x4,10,False,False)
    
    
    
    glutSwapBuffers()


def animate():
    global diamond_pos,diamond_r,diamond_g,diamond_b,diamond_color,speed,catcher_state,score,game_state,prev_time,catcher_speed,catcher_left,catcher_right
    curr_time=time.time()
    delta_time=curr_time-prev_time
    prev_time=curr_time
    if catcher_state==False:
        return
    if game_state==False:
        return
    

    if catcher_left==True:
        if catcher_pos[0][0]<=0:
            catcher_pos[0][0]=0
        else:
            for i in range(len(catcher_pos)):
                catcher_pos[i][0]-=catcher_speed*delta_time
    if catcher_right==True:
        if catcher_pos[1][0]>=500:
            catcher_pos[1][0]=500
        else:
            for i in range(len(catcher_pos)):
                catcher_pos[i][0]+=catcher_speed*delta_time


    if diamond_pos[1][1]<=0:
        diamond_r=0.0
        diamond_g=0.0
        diamond_b=0.0
        diamond_color=[diamond_r,diamond_g,diamond_b]
        catcher_state=False
        print(f'Game Over! Score: {score}')
        glutPostRedisplay()
        return
    for i in range(len(diamond_pos)): 
        diamond_pos[i][1]-=speed*delta_time
        if (catcher_pos[0][0]<=diamond_pos[3][0]<=catcher_pos[1][0]) and ((catcher_pos[0][0]<=diamond_pos[0][0]<=catcher_pos[1][0]) or (catcher_pos[0][0]<=diamond_pos[2][0]<=catcher_pos[1][0]))  and abs((diamond_pos[3][1]-catcher_pos[0][1]))<=4:
            score+=1
            print(f'Score: {score}')
            speed+=30
            diamond_x=r.randint(20,480)
            diamond_y=455
            diamond_pos=[[diamond_x-12,diamond_y-12],[diamond_x,diamond_y],[diamond_x+12,diamond_y-12],[diamond_x,diamond_y-24]]
            diamond_r=r.uniform(0.3,1.0)
            diamond_g=r.uniform(0.3,1.0)
            diamond_b=r.uniform(0.3,1.0)
            diamond_color=[diamond_r,diamond_g,diamond_b]

        
    glutPostRedisplay()
    
def specialKeyListener(key, x, y):
    global catcher_pos,catcher_state,prev_time,catcher_left,catcher_right
    if game_state==False:
        return
    if catcher_state==False:
        return
    else:
        if key==GLUT_KEY_RIGHT:
            catcher_right= True
            catcher_left=False
            
            
        if key==GLUT_KEY_LEFT:
            catcher_left= True
            catcher_right=False
            
            
  
        
    glutPostRedisplay()


def specialKeyUpListener(key,x,y):
    global catcher_left,catcher_right
    if key==GLUT_KEY_RIGHT:
        catcher_right=False
    if key==GLUT_KEY_LEFT:
        catcher_left=False
    




def mouseListener(button, state, position_x, position_y):
    global prev_time,catcher_pos,diamond_pos,diamond_r,diamond_g,diamond_b,diamond_color,speed,catcher_state,score,game_state,diamond_x,diamond_y

    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            x, y = convert_coordinate(position_x,position_y)
            if (10<=x<=40) and (460<=y<=490): # left-arrow (restart) button
                diamond_x=r.randint(20,480)
                diamond_y=455
                catcher_pos=[[180,25],[308,25],[296,10],[195,10]]
                diamond_pos=[[diamond_x-12,diamond_y-12],[diamond_x,diamond_y],[diamond_x+12,diamond_y-12],[diamond_x,diamond_y-24]]
                diamond_r=r.uniform(0.3,1.0)
                diamond_g=r.uniform(0.3,1.0)
                diamond_b=r.uniform(0.3,1.0)
                diamond_color=[diamond_r,diamond_g,diamond_b]
                speed=60
                catcher_state=True
                score=0
                game_state=True
                prev_time=time.time()
                print('Starting over!')
            elif (240<=x<=271) and (458<=y<=490): # pause/play button
                game_state=not game_state
                if game_state==False:
                    return
            elif (458<=x<=487) and (460<=y<=490): # close button
                print(f'Goodbye! Score: {score}')
                glutLeaveMainLoop()

            
                

                
    glutPostRedisplay()




def init():
    #//clear the screen
    glClearColor(0,0,0,0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    






glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(250, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)


wind = glutCreateWindow(b"Catch the Diamonds!")
init()

glutDisplayFunc(display) #display callback function
glutIdleFunc(animate)	
glutSpecialFunc(specialKeyListener)
glutSpecialUpFunc(specialKeyUpListener)
glutMouseFunc(mouseListener)

prev_time=time.time()

glutMainLoop()		#The main loop of OpenGL
