import pygame

pygame.init()

FONT = pygame.font.Font('freesansbold.ttf', 40)
SH = 800
SW = 1200
BarL = 100
BarH = 25
barSpeed = 15
rows = 4
cols = 10
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
screen = pygame.display.set_mode((SW, SH))
pygame.display.set_caption('BrickBreaker')

class Bar:
    def __init__(self):
        self.x = SW//2 - BarL//2
        self.y = SH - BarH
        self.xdir = 0
        self.reset = False
    def move(self):
        keyLeft = False
        keyRight = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keyLeft = True
                self.xdir = -1
            if event.key == pygame.K_RIGHT:
                keyRight = True
                self.xdir = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.xdir = 0
            if event.key == pygame.K_RIGHT:
                self.xdir = 0
        if bar.x in range(-15, 0) and keyLeft:
            bar.xdir = 0
            keyLeft = False
        if bar.x in range(SW - BarL, SW - BarL + 15) and keyRight:
            bar.xdir = 0
            keyRight = False
        
        self.x += (self.xdir * barSpeed)
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, BarL, BarH))

class Bricks:
    def __init__(self):
        self.length = SW//cols
        self.height = 50
        self.blocks = []
        self.build()
    def build(self):
        self.blocks = []
        for row in range(rows):
            blockRow = []
            for col in range(cols):
                blockX = col * self.length
                blockY = row * self.height
                rect = pygame.Rect(blockX, blockY, self.length, self.height)
                if row == 0:
                    strength = 3
                elif row == 2 or row == 1:
                    strength = 2
                elif row == 3:
                    strength = 1
                
                individualBlock = [rect, strength]
                blockRow.append(individualBlock)
            self.blocks.append(blockRow)
    def draw(self):
        for row in self.blocks:
            for block in row:
                if block[1] == 1:
                    blockColor = (0,255,0)
                elif block[1] == 2:
                    blockColor = (0,0,255)
                elif block[1] == 3:
                    blockColor = (255,0,0)
                pygame.draw.rect(screen, blockColor, block[0])
                pygame.draw.rect(screen, (0,0,0), block[0], 2)

class Ball:
    def __init__(self):
        self.x = SW//2 - 10
        self.y = SH - BarH
        self.radius = 10
        self.speedX = 12
        self.speedY = 12
        self.gameOver = False
    def move(self):
        global Bar
        if self.x <= 0 or self.x >= SW - self.radius * 2:
            self.speedX *= -1
        if self.y <= 0:
            self.speedY *= -1
        if self.y >= SH - self.radius * 2:
            self.gameOver = True
        if bar.x < self.x < bar.x + BarL and bar.y < self.y + self.radius * 2 < bar.y + BarH: 
            self.speedY *= -1
        self.x += self.speedX
        self.y += self.speedY
        pygame.draw.circle(screen, (255,255,255), (self.x, self.y), self.radius)
    def reset(self):
            self.x = SW // 2 - 10
            self.y = SH - BarH - 10
            self.speedX = 12 
            self.speedY = -12 
            self.gameOver = False
            bricks.build()

def hitBrick():
    for row in bricks.blocks:
        for block in row:
            rect = block[0]
            if ball.x + ball.radius in range(rect.x, rect.x + rect.width) and ball.y in range(rect.y, rect.y + rect.height):
                ball.speedY *= -1
                block[1] -= 1
                if block[1] <= 0:
                    newRect = pygame.Rect(0,0, 0, 0) 
                    block[0] = newRect 
                    ball.speedY *= -1
                    
def allBricksHit(): 
    for row in bricks.blocks: 
        if len(row) > 0: 
            return False 
    return True

score = FONT.render('1', True, (255,255,255))
scoreRect = score.get_rect(center = (500, 700))

bar = Bar()
ball = Ball()
bricks = Bricks()
run = True
while run:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    bar.move()
    ball.move()
    if ball.gameOver:
        ball.reset()
    hitBrick()
    if allBricksHit(): 
        screen.fill((0, 0, 0)) 
        end_message = FONT.render('You Win!', True, (255, 255, 255)) 
        screen.blit(end_message, (SW // 2 - end_message.get_width() // 2, SH // 2 - end_message.get_height() // 2)) 
        pygame.display.update() 
        pygame.time.wait(3000)
    bricks.draw()
    pygame.time.delay(50)
    pygame.display.update()
pygame.quit()