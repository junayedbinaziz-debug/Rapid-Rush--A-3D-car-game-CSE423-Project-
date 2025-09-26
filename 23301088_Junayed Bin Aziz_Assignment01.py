# #TASK-1


# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *

# import random as r
# speed = 4
# sky_colour=0.0
# state_of_sky=None
# rainfall_dir=0
# rain_drops_list=[]
# for i in range(500):
#     p1=r.randint(0,500)
#     p2=r.randint(0,500)
#     rain_drops_list.append([p1,p2])
# def iterate():
#     glViewport(0, 0, 500, 500)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()

# def showScreen():
#     glClearColor(sky_colour,sky_colour,sky_colour,1.0)
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     glLoadIdentity()
#     iterate()
#     #call the draw methods here
#     draw()
#     glutSwapBuffers()

# def draw():
#     #roof
#     global rain_drops_list
#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(100,250)
#     glVertex2f(400,250)
#     glVertex2f(250,375)
#     glEnd()

#     #base
#     #left triangle
#     glColor3f(1.0,1.0,1.0)
    
#     glBegin(GL_TRIANGLES)
#     glVertex2f(125,250)
#     glVertex2f(125,50)
#     glVertex2f(375,50)
#     glEnd()

#     #right triangle
#     glColor3f(1.0,1.0,1.0)
    
#     glBegin(GL_TRIANGLES)
#     glVertex2f(375,50)
#     glVertex2f(375,250)
#     glVertex2f(125,250)
#     glEnd()

#     #windows
#     #left window
#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(160,230)
#     glVertex2f(160,150)
#     glVertex2f(230,150)
#     glEnd()




#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(160,230)
#     glVertex2f(230,150)
#     glVertex2f(230,230)
#     glEnd()


#     #right window
#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(270,150)
#     glVertex2f(270,230)
#     glVertex2f(340,150)
#     glEnd()


#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(340,150)
#     glVertex2f(270,230)
#     glVertex2f(340,230)
#     glEnd()

#     #window lines
#     #left window
#     #vertical
#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
#     glVertex2f(195, 150) 
#     glVertex2f(195, 190)
    
#     glEnd()

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
    
#     glVertex2f(195, 190)
#     glVertex2f(195, 230)
#     glEnd()

#     # horizontal

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
#     glVertex2f(160,190) 
#     glVertex2f(195, 190)
#     glEnd()

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
#     glVertex2f(195, 190)
#     glVertex2f(230,190)
#     glEnd()


#     #window lines


#     #right window
#     #vertical
#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
#     glVertex2f(305, 150) 
#     glVertex2f(305, 190)
    
#     glEnd()

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
    
#     glVertex2f(305, 190)
#     glVertex2f(305, 230)
#     glEnd()



#     #horizontal

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
#     glVertex2f(270,190) 
#     glVertex2f(305,190)
    
#     glEnd()

#     glColor3f(1.0,1.0,1.0)
#     glBegin(GL_LINES)
    
#     glVertex2f(305,190)
#     glVertex2f(340,190)
#     glEnd()


#     #Door
#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(220,50)
#     glVertex2f(280,50)
#     glVertex2f(220,140)
#     glEnd()


#     glColor3f(0.0,0.0,1.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(280,50)
#     glVertex2f(220,140)
#     glVertex2f(280,140)
#     glEnd()


#     #knob

#     glColor3f(0.0,0.0,0.0)
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     glVertex2f(230,90)
#     glEnd()


#     #ground
#     #left side of the house
#     #left triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(125,0)
#     glVertex2f(0,250)
#     glVertex2f(0,0)
#     glEnd()

#     #right triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(125,0)
#     glVertex2f(125,250)
#     glVertex2f(0,250)
#     glEnd()

#     #ground below base
#     #left triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(125,0)
#     glVertex2f(375,0)
#     glVertex2f(125,50)
#     glEnd()

#     #right triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(375,0)
#     glVertex2f(375,50)
#     glVertex2f(125,50)
#     glEnd()

#     #right side of the house
#     #left triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(375,0)
#     glVertex2f(500,0)
#     glVertex2f(375,250)
#     glEnd()

#     #right triangle
#     glColor(0.6,0.3,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(500,0)
#     glVertex2f(500,250)
#     glVertex2f(375,250)
#     glEnd()

#     #Trees
#     #Left tree
#     #Leaves
#     glColor(0.0,1.0,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(10,250)
#     glVertex2f(95,250)
#     glVertex2f(52.5,290)
#     glEnd()

#     #base of the tree
#     glColor(0.0,0.0,0.0)
#     glBegin(GL_LINES)
#     glVertex2f(52.5,250)
#     glVertex2f(52.5,150)
#     glEnd()



#     #Trees
#     #right tree
#     #Leaves
#     glColor(0.0,1.0,0.0)
#     glBegin(GL_TRIANGLES)
#     glVertex2f(405,250)
#     glVertex2f(480,250)
#     glVertex2f(438,290)
#     glEnd()

#     #base of the tree
#     glColor(0.0,0.0,0.0)
#     glBegin(GL_LINES)
#     glVertex2f(442.5,250)
#     glVertex2f(442.5,150)
#     glEnd()

#     # rainfall
#     glColor(0.5,0.5,1.0)
#     glBegin(GL_LINES)
#     for p1,p2 in rain_drops_list:
#         glVertex2f(p1,p2)
#         glVertex2f(p1+rainfall_dir,p2-15)
#     glEnd()

   
    

# def animate():
#     global rain_drops_list,speed,rainfall_dir
#     for i in range(len(rain_drops_list)):
#             rain_drops_list[i][0]=(rain_drops_list[i][0]+rainfall_dir)%500
#             rain_drops_list[i][1]=(rain_drops_list[i][1]-speed)%500

#             if rain_drops_list[i][0]>500 or rain_drops_list[i][0]<0:
#                 rain_drops_list[i][0]=r.randint(0,500)

#             if rain_drops_list[i][1]>500 or rain_drops_list[i][1]<0:
#                 rain_drops_list[i][1]=r.randint(0,500)
        
#     glutPostRedisplay()





    
# def keyboardListener(key, x, y):
#     global state_of_sky
#     if key==b'd':
#         state_of_sky='Day'
        
#     if key==b'n':
#         state_of_sky='Night'
   

#     glutPostRedisplay()

# def change_sky_color():
#     global sky_colour,state_of_sky
#     if state_of_sky=='Day':
#         sky_colour+=0.001
#         if sky_colour>1.0:
#             sky_colour=1.0
#     else:
#         sky_colour-=0.001
#         if sky_colour<0.0:
#             sky_colour=0.0
#     glutPostRedisplay()

# def specialKeyListener(key, x, y):
#     global rainfall_dir
#     if key==GLUT_KEY_RIGHT:
#         rainfall_dir+=8
#         if rainfall_dir>16:
#             rainfall_dir=16
#     if key==GLUT_KEY_LEFT:
#         rainfall_dir-=8
#         if rainfall_dir<-16:
#             rainfall_dir=-16
  
        
#     glutPostRedisplay()

# def helper():
#     change_sky_color()
#     animate()















    





# glutInit()
# glutInitDisplayMode(GLUT_RGBA)
# glutInitWindowSize(500, 500) #window size
# glutInitWindowPosition(0, 0)
# wind = glutCreateWindow(b"Building a House in Rainfall") #window name
# glutDisplayFunc(showScreen)
# glutKeyboardFunc(keyboardListener)
# glutIdleFunc(helper)
# glutSpecialFunc(specialKeyListener)

# glutMainLoop()


#TASK-2

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random as r

W_Width, W_Height = 500,500

x=y=0
speed = 0.01
size = 3.5
move_coords=[(1,1),(-1,-1),(1,-1),(-1,1)]
create_new = False
left_click_count=0
pixel_pos_and_colour=[]
pause=False
def convert_coordinate(x,y):
    global W_Width, W_Height
    a = x - (W_Width/2)
    b = (W_Height/2) - y 
    return a,b

def draw(x,y,size):
    glPointSize(size) 
    glBegin(GL_POINTS)
    for i in pixel_pos_and_colour:
            x,y,move_x,move_y,red,green,blue,store_red,store_green,store_blue=i
            glColor3f(red,green,blue)
            glVertex2f(x,y)
    glEnd()



def display():
    #//clear the display
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    	#//color black
    #//load the correct matrix -- MODEL-VIEW matrix
    glMatrixMode(GL_MODELVIEW)
    #//initialize the matrix
    glLoadIdentity()
    #//now give three info
    #//1. where is the camera (viewer)?
    #//2. where is the camera looking?
    #//3. Which direction is the camera's UP direction?
    gluLookAt(0,0,200,	0,0,0,	0,1,0)
    draw(x,y,size)
    glutSwapBuffers()

def init():
    #//clear the screen
    glClearColor(0.0,0.0,0.0,1.0)
    #//load the PROJECTION matrix
    glMatrixMode(GL_PROJECTION)
    #//initialize the matrix
    glLoadIdentity()
    #//give PERSPECTIVE parameters
    gluPerspective(104,	1,	1,	1000.0)






def animate():
    #//codes for any changes in Models, Camera
    global x, y,speed,move,pause,pixel_pos_and_colour,left_click_count,red_store,green_store,blue_store

    if pause==True:
        return
    
    for i in range(len(pixel_pos_and_colour)):
        x,y,move_x,move_y,red,green,blue,store_red,store_green,store_blue=pixel_pos_and_colour[i]
        if left_click_count%2!=0:
            red=0.0
            green=0.0
            blue=0.0
        if left_click_count%2==0:
            red=store_red
            green=store_green
            blue=store_blue

        x+=move_x*speed
        if x>250 or x<-250:
            move_x=-1*(move_x)
            x+=move_x*speed
        y+=move_y*speed
        if y>250 or y<-250:
            move_y=-1*(move_y)
            y+=move_y*speed
        pixel_pos_and_colour[i]=[x,y,move_x,move_y,red,green,blue,store_red,store_green,store_blue]
    
            
    glutPostRedisplay()

def mouseListener(button, state, position_x, position_y):
	#/#/x, y is the x-y of the screen (2D)
    global x,y,move,create_new,pixel_pos_and_colour,left_click_count,pause
    if pause==True:
        return
    if button==GLUT_RIGHT_BUTTON:
        if (state == GLUT_DOWN):
            x, y = convert_coordinate(position_x,position_y)
            move_x,move_y=r.choice(move_coords)
            create_new=True
            red=store_red=r.uniform(0,1)
            green=store_green=r.uniform(0,1)
            blue=store_blue=r.uniform(0,1)
            pixel_pos_and_colour.append([x,y,move_x,move_y,red,green,blue,store_red,store_green,store_blue])

    if button==GLUT_LEFT_BUTTON:
        if state==GLUT_DOWN:
            left_click_count+=1
    
 
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global speed,pause
    if pause==True:
        return
    if key==GLUT_KEY_UP:
        speed *= 2
        print("Speed Increased")
    if key== GLUT_KEY_DOWN:		
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()




def keyboardListener(key, x, y):
    global pause

    global ball_size
    if key==b' ': #spacebar
        if pause==False:
            pause=True
        else:
            pause=False
        
    glutPostRedisplay()






glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) #	//Depth, Double buffer, RGB color

# glutCreateWindow("My OpenGL Program")
wind = glutCreateWindow(b"Building the Amazing Box")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)


glutMouseFunc(mouseListener)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)

glutMainLoop()
   