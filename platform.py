""" I'm gonna need a lot of comments, because I have no clue what a lot of the game mechanics are and how they operate.
I also think the way the movement mechanics are implemented should be redone because they're a bit of a buggy mess currently """

import pygame, sys
from pygame import * # WHY ARE YOU IMPORTING STAR I THOUGHT THIS WAS BAD

VERS_NUM = 0.4
MSG = 'Click the button to spawn a bird! Press space to switch between characters!' # Space button breaks and stops working. Also unusable "bird" in upper right for no reason.

pygame.init()
fpsClock = pygame.time.Clock()


redColor = pygame.Color(255, 0, 0)
greenColor = pygame.Color(0, 255, 0)
blueColor = pygame.Color(0, 0, 255)
whiteColor = pygame.Color(255, 255, 255)
fontObj = pygame.font.Font('freesansbold.ttf', 12)
SCREENWIDTH = 640
SCREENHEIGHT = 480
x, y = 0, 0

up, down, left, right = False, False, False, False # Interesting
currentPlayer = 0

windowSurfaceObj = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Platformer ' + str(VERS_NUM) + ': ' + MSG)

# Example sound object
bounceSound = pygame.mixer.Sound('bounce.wav')
bgm = pygame.mixer.Sound('LevelLoop.wav')



map = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W       W           W                                          W",
"WWWWW           W       W    WWWWWWW                           W",
"W            W                                                 W",
"W                                                              W",
"W                                                              W",
"W                                        W          WW         W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                          WWW     WWW                         W",
"W                                                              W"
"W                                                              W",
"W                              WW        W                     W",
"W                                                              W",
"W                                                              W",
"W     WW       WW           W                   WW             W",
"W    WW    W    W                                              W",
"W     W   WWW   W                                              W", # Tried to make playable area a bit more interesting
"W     W  WWWWW  W        WW                                    W",
"W     WWWWWWWWWWW                                       WWWWWW W",
"W     W                                                        W",
"W    WW               W                                        W",
"W     W                                                        W",
"W     W                             WW                         W",
"W     W           WW                                           W",
"W     W                                                        W",
"W    WW                                                        W",
"W     W        W                                               W",
"W     W                                                        W",
"W     W               WWWWWWWWWWWWWWWWWWWWWW                   W",
"WW    W              W                                         W",
"W     W             W     W     W    W    WWWWWWW              W",
"W   WWWWWW   WWWWWWW                     W            WWWWWW   W",
"W                                       W                      W",
"W                   WWWWWWWWWWWWWWWWWWWW                       W",
"WWW         W      W                                           W",
"W                 W                                            W",
"WWWWWWW   WWWWWWWW                              WW             W",
"W                                                              W",
"W       W                                                      W",
"W      WWW                     WWWWWWWWWWW                     W",
"W     WWWWW                                                    W",
"W       W                                                      W",
"W   WWW   WWW                                                  W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" ]

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # What



class Block(Entity):
    def __init__(self, color, width, height, x, y):
        Entity.__init__(self)
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect() #GETREKT
        self.rect.x = x
        self.rect.y = y


class SpawnButton(Block):
    def __init__(self, color, x, y, entity):
        Block.__init__(self, color, 10, 10, x, y)
        self.mousex = 0
        self.mousey = 0
        self.entity = entity
        
    def spawn(self, go = False):
        if go:
            return self.entity
    
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == pygame.MOUSEBUTTONDOWN:
                self.mousex, self.mousey = event.pos
                if self.get_rect().collide_point(self.mousex,self.mousey):
                    return self.entity

class Platformer(Entity):
    def __init__(self, color, width, height, x, y):
        Entity.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.xvel = 0
        self.yvel = 0
        self.onGround = False
        
    def update(self, up, down, left, right, platforms, isPlatformer = True):
        if up:
            if isPlatformer and self.onGround: # Jumping
                self.yvel -= 8
                bounceSound.play()
            elif not isPlatformer:
                self.yvel -= 3
                if self.yvel < -5:
                    self.yvel = -5
        if not self.onGround:
            self.yvel += 0.5
            if self.xvel > 0 and not right: # Momentum decay. For whatever reason, rightward momentum decays way faster than it should. 
                if self.xvel > 2:
                    self.xvel -= .3
                elif self.xvel > 1:
                    self.xvel -= .2
                else:
                    self.xvel -= .1
            if self.xvel < 0 and not left: # Momentum decay
                if self.xvel < -2:
                    self.xvel += .3
                elif self.xvel < -1:
                    self.xvel += .2
                else:
                    self.xvel += .1
            if self.yvel > 15:
                self.yvel = 15
        if down:
            self.yvel += 5
        if left:
            self.xvel = -3
        if right:
            self.xvel = 3
        if not(left or right):
            if self.onGround:
                self.xvel = 0
        
        self.rect.left += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.top += self.yvel
        self.onGround = False
        self.collide(0, self.yvel, platforms)
        
    def collide(self, xvel, yvel, plats):
        for p in plats:
                if sprite.collide_rect(self, p) and isinstance(p, Block):
                    if xvel > 0:
                        self.rect.right = p.rect.left
                    if xvel < 0:
                        self.rect.left = p.rect.right
                    if yvel > 0:
                        self.rect.bottom = p.rect.top
                        self.onGround = True
                        self.yvel = 0
                    if yvel < 0:
                        self.rect.top = p.rect.bottom
                        self.yvel = 0

                        
class Bird(Platformer):

    def update(self, up, down, left, right, platforms):
        super(Bird, self).update(up, down, left, right, platforms, False)


        
player = []
platforms = pygame.sprite.Group()
for row in map:
        for col in row:
            if col == "W":
                wall = Block(blueColor, 10, 10, x, y)
                platforms.add(wall)
            x += 10
        y += 10
        x = 0

platy = Platformer(redColor, 10, 10, SCREENWIDTH/2, 10)
spawnBird = SpawnButton(greenColor, 620, 10, Bird(greenColor, 10, 10, 20, 20))

platforms.add(platy)
player.append(platy)
platforms.add(spawnBird)

bgm.play(-1)
bgm_on = True

while True:
    windowSurfaceObj.fill(whiteColor)
    msg = str(player[currentPlayer].rect.x) + ', ' + str(player[currentPlayer].rect.y)
    
    
    msgSurfaceObj = fontObj.render(msg, False, redColor)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (10,20)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    
    version = fontObj.render("version " + str(VERS_NUM) , False, redColor)
    versionRectObj = version.get_rect()
    versionRectObj.topleft = (10,40)
    windowSurfaceObj.blit(version, versionRectObj)
    
    for ev in pygame.event.get():
        if ev.type == QUIT:
            bgm.stop()
            pygame.quit()
            sys.exit()
        if ev.type == KEYDOWN and ev.key == K_m: # Music toggle
            if bgm_on:
                bgm.stop()
                bgm_on = False
            else:
                bgm.play(-1)
                bgm_on = True
            pygame.event.post(pygame.event.Event(QUIT))
        if ev.type == MOUSEBUTTONDOWN:
            p = spawnBird.spawn(True)
            player.append(p)
            platforms.add(p)
        if ev.type == KEYDOWN and ev.key == K_LEFT:
            left = True
        if ev.type == KEYDOWN and ev.key == K_RIGHT:
            right = True
        if ev.type == KEYDOWN and ev.key == K_UP:
            up = True
        if ev.type == KEYDOWN and ev.key == K_DOWN:
            down = True
        if ev.type == KEYDOWN and ev.key == K_SPACE:
            currentPlayer += 1
            if currentPlayer >= len(player):
                currentPlayer = 0

        if ev.type == KEYUP and ev.key == K_LEFT:  # I believe this causes problems with input being erroneously given, because sometimes the player character
            left = False                           # will continue sliding or jumping after you've stopped. Probably means KEYUP isn't registering for some reason. 
        if ev.type == KEYUP and ev.key == K_RIGHT: # I suspect multiple inputs can't be processed at once.
                                                   # This is the biggest bug the game has so far, fixing it will solidify the platforming mechanics. 
            right = False
        if ev.type == KEYUP and ev.key == K_UP:
            up = False
        if ev.type == KEYUP and ev.key == K_DOWN:
            down = False

    if player:
        player[currentPlayer].update(up, down, left, right, platforms)
    
    
    p = spawnBird.spawn()
    if p:
        player.append(p)
        platforms.add(p)
    
    platforms.draw(windowSurfaceObj)
    

    
    
    pygame.display.update()
    fpsClock.tick(30)
