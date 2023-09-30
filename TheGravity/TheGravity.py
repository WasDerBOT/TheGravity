
from pygame import *
from math import *
from numpy import *
# define classes
class Planet():
    def __init__(self,pos,radius,direction):
        self.radius = radius
        self.direction = direction * 0.06
        self.pos = pos
        self.mass = radius * 2
        self.kinematic = False
    def move(self):
        self.pos = self.pos + self.direction
    def log(self):
        pass
    def draw(self,cam):
        draw.circle(window,BLACK,(self.pos[0] + cam.x,self.pos[1] + cam.y),self.radius)
    def force(self,force):
        
        self.direction = (self.direction + force)
    
class Camera():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def MoveTo(self,x,y):
        self.x = x
        self.y = y

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)

# define the size of game window
WIDTH = 1000
HEIGHT = 800
FPS = 60

# initialize Pygame
init()
display.set_caption("My Game")
clock = time.Clock()
window = display.set_mode((WIDTH, HEIGHT))

running = True
# font for text 
font = font.SysFont("C:\Windows\Fonts\Arial",100)  


G = 1


i = 0
window.fill(WHITE)



Objects = []
mx, my = 0,0
nx,ny = 0,0
def getCollision(a,b):
    if a != b:
        if getDist(a,b) < (a.radius  + b. radius):
            return True
        else:
            return False
def getDist(a,b):
    c = array([abs(b.pos[0] - a.pos[0]),abs(b.pos[1] - a.pos[1])])
    return abs(sqrt(c[0]**2 + c[1] ** 2)) + 1
def getAttraction(a,b):
    c = array([b.pos[0] - a.pos[0],b.pos[1] - a.pos[1]])
    c = c / 100 * G * ((a.mass * b.mass) / getDist(a,b)**2 )
    return c

creating = False
moving = False
cam = Camera(0,0,WIDTH,HEIGHT)
while running:
    #Control of framerate
    clock.tick(FPS)
    #Cleaning of screen
    window.fill(WHITE)
    #Events handling
    events = event.get()
    for e in events:
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN and e.button == 1 and not(moving):
            mx,my = mouse.get_pos()
            mx -= cam.x
            my -= cam.y
            creating = True
        if e.type == MOUSEBUTTONUP and e.button == 1 and not(moving):
            nx,ny = mouse.get_pos()
            nx -= cam.x
            ny -= cam.y
            Objects.append(Planet(array([mx,my]),10,-1 * array([nx - mx,ny - my])))
            mx, my = 0,0
            nx,ny = 0,0
            creating = False

        if e.type == MOUSEBUTTONDOWN and e.button == 2 and not(creating):
            mx,my = mouse.get_pos()
            mx -= cam.x
            my -= cam.y
            moving = True
        if e.type == MOUSEBUTTONUP and e.button == 2 and not(creating):
            moving = False
            
        if e.type == MOUSEBUTTONDOWN and e.button == 3 and not(creating) and not(moving):
            mx,my = mouse.get_pos()
            for o in Objects:
                if getDist(Planet(array([mx,my]),0,array([0,0])),o) < o.radius:
                    o.kinematic = not(o.kinematic)
    #Events reacts
    for o in Objects:
        for k in Objects:
            if o != k:
                o.force(getAttraction(o,k) * k.mass / (o.mass + k.mass))
    for o in Objects:
        for k in Objects:
            if getCollision(k,o):
                if k.mass > o.mass:
                    k.radius = k.radius + o.radius
                    k.mass += o.mass
                    k.direction = k.direction / k.mass + o.direction / o.mass
                    Objects.remove(o)
                else:
                    o.radius = k.radius + o.radius
                    o.mass += k.mass
                    o.direction = o.direction / o.mass + k.direction / k.mass
                    Objects.remove(k)

            
    for o in Objects:
        if not(o.kinematic):
            o.move()
        
    if moving:
        nx,ny = mouse.get_pos()
        cam.MoveTo(nx - mx,ny - my)
        
        
    #Drawing objects
    for o in Objects:
        o.draw(cam)
    if creating:
        nx,ny = mouse.get_pos()
        draw.line(window,BLACK,[mx + cam.x,my+ cam.y],[nx,ny],3)
      
    #print(i)
    display.update()   
    i+= 1