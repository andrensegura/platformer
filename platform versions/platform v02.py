import pygame, sys
from pygame import *

VERS_NUM = 0.1

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

up, down, left, right = False, False, False, False

windowSurfaceObj = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('Platformer ' + str(VERS_NUM))

#example sound object
bounceSound = pygame.mixer.Sound('bounce.wav')
bgm = pygame.mixer.Sound('Level.wav')



map = [
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                            WWWWWWW                           W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W"
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                        W                                     W",
"W                        W                                     W",
"W                        W                                     W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                        WWWWWWWWWWWWWWWWWWWWWWWW              W",
"W                                                              W",
"W                                                              W",
"W                                                     WWWWWW   W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                      WWWWWW                  W",
"W                                                              W",
"W                                                WWW           W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"W                                                              W",
"WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW" ]

class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)



class Block(Entity):
	
	def __init__(self, color, width, height, x, y):
		Entity.__init__(self)
		
		pygame.sprite.Sprite.__init__(self)
		
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		
		



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
		self.onGround = True
		
	def update(self, up, down, left, right, platforms):
		if up:
			if self.onGround:
				self.yvel -= 8
				bounceSound.play()
		if down:
			self.yvel += 5
		if left:
			self.xvel = -3
		if right:
			self.xvel = 3
		if not self.onGround:
			self.yvel += 0.5
			if self.yvel > 15:
				self.yvel = 15
		if not(left or right):
			if self.onGround:
				self.xvel = 0
		
		self.rect.left += self.xvel
		self.collide(self.xvel, 0, platforms)
		self.rect.top += self.yvel
		self.onGround = False
		self.collide(0, self.yvel, platforms)
		
	def collide(self, xvel, yvel, plats):
		for p in platforms:
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


platforms = pygame.sprite.Group()	
for row in map:
		for col in row:
			if col == "W":
				wall = Block(blueColor, 10, 10, x, y)
				platforms.add(wall)
			x += 10
		y += 10
		x = 0

player = Platformer(redColor, 10, 10, SCREENWIDTH/2, 10)

platforms.add(player)

bgm.play(-1)

while True:
	windowSurfaceObj.fill(whiteColor)
	msg = str(player.rect.x) + ', ' + str(player.rect.y)
	
	
	msgSurfaceObj = fontObj.render(msg, False, redColor)
	msgRectobj = msgSurfaceObj.get_rect()
	msgRectobj.topleft = (10,20)
	windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
	
	version = fontObj.render("version 0.2", False, redColor)
	versionRectObj = version.get_rect()
	versionRectObj.topleft = (10,40)
	windowSurfaceObj.blit(version, versionRectObj)
	
	for ev in pygame.event.get():
		if ev.type == QUIT:
			pygame.quit()
			sys.exit()
		if ev.type == KEYDOWN and ev.key == K_ESCAPE:
			pygame.event.post(pygame.event.Event(QUIT))
		if ev.type == KEYDOWN and ev.key == K_LEFT:
			left = True
		if ev.type == KEYDOWN and ev.key == K_RIGHT:
			right = True
		if ev.type == KEYDOWN and ev.key == K_UP:
			up = True
		if ev.type == KEYDOWN and ev.key == K_DOWN:
			down = True
				

		if ev.type == KEYUP and ev.key == K_LEFT:
			left = False
		if ev.type == KEYUP and ev.key == K_RIGHT:
			right = False
		if ev.type == KEYUP and ev.key == K_UP:
			up = False
		if ev.type == KEYUP and ev.key == K_DOWN:
			down = False


	player.update(up, down, left, right, platforms)
	platforms.draw(windowSurfaceObj)
	

	
	
	pygame.display.update()
	fpsClock.tick(30)