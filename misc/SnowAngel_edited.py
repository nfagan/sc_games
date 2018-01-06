from pygame import *
import random, sys

# this is an edited version of Max Kubierschky's Snow Angel game (version 1.1), found here: https://www.pygame.org/project/1082/2021
# Info on Max (presumably the right guy): http://www.maxky.de/en/index.html

class Flake(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface( (11,11) )
        self.rect = self.image.get_rect()    
        draw.line(self.image,Color("white"),(5,0),(5,10))
        draw.line(self.image,Color("white"),(0,2),(10,8))
        draw.line(self.image,Color("white"),(0,8),(10,2))
        self.vy = 1
        flakes.add(self)
    def update(self):
        self.rect.y += self.vy
        self.rect.x = (self.rect.x+self.vx)%width
        if self.rect.y > height-50:
            flakes.remove(self)
        if angel.lives>0 and self.rect.colliderect(angel.rect):
            angel.lives -= 1
            startLevel()

class Angel(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        self.image = Surface( (11,17) )
        self.rect = self.image.get_rect()    
        poly = ((0,1),(2,4),(8,4),(10,1),(10,8),(7,10),(10,16),(0,16),(3,10),(0,8))
        # alternate look: ((0,8),(2,4),(8,4),(10,8),(10,8),(7,10),(10,16),(0,16),(3,10),(0,8))
        draw.polygon(self.image,Color("white"),poly)
        draw.circle(self.image,Color("white"),(5,2),2)
        self.lives = 100 # changed to 100 from 12
        self.currently_pressed = set()
    # changed angel movement to only allow one key press at a time
    def update(self):
        key_states = key.get_pressed()
        # not allowing keys to be held down, but increasing the amount of movement per key press
        if key_states[K_UP] and K_UP not in self.currently_pressed and K_DOWN not in self.currently_pressed:
            self.rect.y -=  15
            self.currently_pressed.add(K_UP)
            for i in (K_LEFT, K_RIGHT):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[K_DOWN] and self.rect.bottom<height and K_DOWN not in self.currently_pressed and K_UP not in self.currently_pressed:
            self.rect.y += 15
            self.currently_pressed.add(K_DOWN)
            for i in (K_LEFT, K_RIGHT):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[K_LEFT] and self.rect.x>0 and K_LEFT not in self.currently_pressed and K_RIGHT not in self.currently_pressed:
            self.rect.x -= 15
            self.currently_pressed.add(K_LEFT)
            for i in (K_UP, K_DOWN):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[K_RIGHT] and self.rect.right<width and K_RIGHT not in self.currently_pressed and K_LEFT not in self.currently_pressed:
            self.rect.x += 15
            self.currently_pressed.add(K_RIGHT)
            for i in (K_UP, K_DOWN):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        # once no keys are being pressed, all arrow presses become valid again
        elif sum(key_states) == 0:
            self.currently_pressed.clear()
        if (key_states[K_l]and self.rect.bottom<height) or self.rect.top<25:
            startLevel(min(level+1,len(vxRanges)))

flakes = sprite.RenderPlain()
init()
width = 800
height = 600
window = display.set_mode((width, height)) 
screen = display.get_surface() 
fnt = font.Font(None, 24)


def write(s,x,y,center=0):
    text = fnt.render(s,True,Color("white"))
    screen.blit(text,(x-center*text.get_width()/2,y))


vxRanges = ((0,0),(0,0),(-1,1),(1,2),(0,0),(-1,1),(-1,1),(-2,2),(-2,2),(-2,2),(-2,2),(-3,3),(0,0))
vyRanges = ((1,1),(1,2),(1,2),(1,2),(1,3),(1,2),(1,2),(1,2),(1,2),(1,3),(1,3),(1,3),(0,0))
freqs = (0.1,0.1,0.1,0.1,0.2,0.2,0.25,0.25,0.3,0.3,0.4,0.4,0)
clock = time.Clock()
angel = Angel()

def updateFlakes():
    if random.random()<freqs[level-1]:
        f = Flake()
        f.rect.x = random.randint(0,3*width)
        f.rect.bottom = 0    
        f.vx = random.randint(*vxRanges[level-1])
        f.vy = random.randint(*vyRanges[level-1])
    flakes.update()

def startLevel(lvl=0):
    global level
    angel.rect.x = width/2
    angel.rect.bottom = height
    if lvl:
        level = lvl
        for i in range(800):
            updateFlakes()

startLevel(1)
while True:
    for ev in event.get():
        if ev.type == constants.QUIT:
            exit(0)
        # angel keeps track of which keys are currently pressed/unpressed, to determine which movements are allowed
        if ev.type == KEYUP:
            angel.currently_pressed.discard(ev.key)
    screen.fill((0,0,0))
    # No need to display lives
    #write("Lives: %d"%angel.lives,width-120,20)
    if level<len(vxRanges):
        write("Level: %d/%d"%(level,len(vxRanges)-1),width-120,40)
        updateFlakes()
        flakes.draw(screen)
    else:
        write("Congratulations, you have won!",width/2,height/2-10,1)
    if angel.lives>0:
        angel.update()
        screen.blit(angel.image,angel.rect.topleft)
    else:
        write("game over",width/2,height/2-10,1)
        write("Start new game with 'n'.", width/2,height/2+40,1)
    # changing "lives" from 12 to 100
    if key.get_pressed()[K_n]:
        angel.lives = 100
        startLevel(1)
    if level == 1 and angel.lives==100 and angel.rect.bottom==height:
        write("Fly past all the snow flakes without being hit!", width/2,height/2-20,1)
    elif level > 1 and level <= len(vxRanges) - 1 and angel.rect.bottom==height:
        write("When you're ready, keep going!", width/2,height/2-20,1)
    display.flip()
    clock.tick(40)

