from pygame import *
import random, sys

# This activity is adapted from Max Kubierschky's Snow Angel game (version 1.1), found here: https://www.pygame.org/project/1082/2021
# Info on Max (presumably the right guy): http://www.maxky.de/en/index.html


input_mode = raw_input("Would you like to play in 1) keyboard mode or 2) button box mode? ")
while True:
    try:
        assert input_mode == "1" or input_mode == "2"
        break
    except:
        input_mode = raw_input("Invalid response. Enter \"1\" for keyboard mode or \"2\" for button box mode: ")

if input_mode == "1":
    up = K_UP
    down = K_DOWN
    left = K_LEFT
    right = K_RIGHT
else:
    # Note these are different mappings than in sc_games (left/right switched) because the practice
    # MRI display flips everything
    up = K_1
    down = K_3
    left = K_2
    right = K_4

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
            angel.just_failed = True
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
        self.just_failed = False
    # changed angel movement to only allow one key press at a time
    def update(self):
        key_states = key.get_pressed()
        # not allowing keys to be held down, but increasing the amount of movement per key press
        if key_states[up] and up not in self.currently_pressed and down not in self.currently_pressed:
            self.rect.y -=  15
            self.currently_pressed.add(up)
            for i in (left, right):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[down] and self.rect.bottom<height and down not in self.currently_pressed and up not in self.currently_pressed:
            self.rect.y += 15
            self.currently_pressed.add(down)
            for i in (left, right):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[left] and self.rect.x>0 and left not in self.currently_pressed and right not in self.currently_pressed:
            self.rect.x -= 15
            self.currently_pressed.add(left)
            for i in (up, down):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        elif key_states[right] and self.rect.right<width and right not in self.currently_pressed and left not in self.currently_pressed:
            self.rect.x += 15
            self.currently_pressed.add(right)
            for i in (up, down):
                if not key_states[i]:
                    self.currently_pressed.discard(i)
        # once no keys are being pressed, all arrow presses become valid again
        elif sum(key_states) == 0:
            self.currently_pressed.clear()
        if (key_states[K_l]and self.rect.bottom<height) or self.rect.top<25:
            startLevel(min(level+1,len(vxRanges)))

flakes = sprite.RenderPlain()
init()
# changed window size to be appropriate for full screen
width = 1440
height = 900
window = display.set_mode((width, height), FULLSCREEN) # changed to full screen
screen = display.get_surface()
fnt = font.Font(None, 24)


def write(s,x,y,center=0):
    text = fnt.render(s,True,Color("white"))
    # in MRI mode, need to flip text horizontally to display correctly on MRC's practice MRI display
    # this option may have to be changed for use on other MRI/practice MRI set-ups
    if input_mode == "2":
        text = transform.flip(text, True, False)
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

mouse.set_visible(False) # turn off cursor
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
    # hitting the "n" key starts a new game (do we want to keep this?)
    if key.get_pressed()[K_n]:
        angel.lives = 100
        startLevel(1)
    # added the ability to quit with the "q" or escape keys
    if key.get_pressed()[K_q] or key.get_pressed()[K_ESCAPE]:
        exit(0)
    if level == 1 and angel.lives==100 and angel.rect.bottom==height:
        write("Fly past all the snowflakes without being hit!", width/2,height/2-20,1)
    if angel.just_failed: 
        if angel.rect.bottom == height:
            write("Try again!", width/2,height/2-20,1)
        else:
            angel.just_failed = False
    elif level > 1 and level < len(vxRanges) and angel.rect.bottom==height:
        write("When you're ready, keep going!", width/2,height/2-20,1)
    display.flip()
    clock.tick(40)

