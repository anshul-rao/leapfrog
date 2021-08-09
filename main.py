import random, pygame, colorsys, sys

# ----- Window Initializations ----- #
pygame.init()
screenWidth = 480
screenHeight = 640
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("CSC Pygame Sample -- Flopping Frog")
font = pygame.font.Font("font/Roboto-Thin.ttf", 18)

# ----- Game Variables ----- #
grav = 0.25
BG = pygame.Color('#BEE0B4')
moveLeft = False
moveRight = False
clock = pygame.time.Clock()
FPS = 60


# load cam


# ----- Functions and Classes ----- #
def draw_bg():
    screen.fill(BG)


"""
class Background:
    def __init__(self):
        self.sprite = pygame.image.load('img/bg.png')
        self.position = 0
        self.uncoloredSprite = pygame.image.load('img/bg.png')

    def setSprite(self, tint):
        copy = self.uncoloredSprite.copy()
        color = colorsys.hsv_to_rgb(tint, 1, 1)
        copy.fill((color[0] * 255, color[1] * 255, color[2] * 255), special_flags=pygame.BLEND_ADD)
        self.sprite = copy
"""


class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.animationList = []
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        for i in range(60):
            img = pygame.image.load(f'img/fly/{i}.png').convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            self.animationList.append(img)
        self.image = self.animationList[self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.isHit = False

    def draw(self):
        screen.blit(self.image, self.rect)
        if self.rect.colliderect(frog.rect):
            frog.boost = True
            frog.velY = -9
            self.isHit = True

    def updateAnimation(self):
        # Update Animation
        animationCooldown = 10
        # Update image depending on current frame
        self.image = self.animationList[self.frameIndex]
        # Check if enough time has passed since update
        if pygame.time.get_ticks() - self.updateTime > animationCooldown:
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        # Loop back to beg of animation
        if self.frameIndex >= len(self.animationList):
            self.frameIndex = 0


class Frog(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("img/frog.png").convert_alpha()
        # Object
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self._boost = False

        # Direction

        self.speed = speed
        self.direction = 1
        self.flip = False
        self.inAir = True
        self.velY = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self, moveLeft, moveRight):
        dx = 0
        dy = 0

        if moveLeft:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if moveRight:
            dx = self.speed
            self.flip = False
            self.direction = 1

        self.velY += grav
        if self.velY > 8:
            self.velY = 8

        dy += self.velY

        if self.rect.left >= screenWidth:
            # dx = 0
            self.rect.x = 2

        if self.rect.right <= 0:
            # dx = screenWidth
            self.rect.x = 430

        self.rect.x += dx
        self.rect.y += dy

    def boost(self):
        if self.rect.colliderect(flies[i].rect):
            self._boost = True
            self.velY = -9


def updateFPS():
    fps = str(int(clock.get_fps()))
    fpsText = font.render(fps, 1, pygame.Color("#2F4F4F"))
    return fpsText


def camera():
    if frog.rect.top <= screenHeight / 3:
        frog.rect.y += abs(frog.velY)
        for fly in flies:
            fly.rect.y += abs(frog.velY)


flies = []
n = 5
for i in range(n):
    flies.append(
        Fly((random.randint(0, screenWidth)), (random.randint(0, screenHeight)), 0.12)
    )


def collisionCheck(frog: Frog, flies: list[Fly]) -> list[Fly]:
    for i in range(len(flies)):
        if flies[i].rect.colliderect(frog.rect) and flies[i].isHit:
            flies[i] = Fly(
                (random.randint(0, screenWidth)),
                (random.randint(0, screenHeight)),
                0.12,
            )
        flies[i].isHit = False
    return flies


initialBoost = Fly(screenWidth / 2, screenHeight - 150, .1)
frog = Frog(screenWidth / 2, screenHeight - 150, 0.17, 5)

# ----- Main Game Loop ----- #
run = True
while run:

    clock.tick(FPS)

    draw_bg()
    screen.blit(updateFPS(), (10, 5))
    frog.draw()
    initialBoost.draw()
    camera()

    # Initial Boost
    if initialBoost.isHit:
        initialBoost.rect.x = 1000
    frog.move(moveLeft, moveRight)

    for fly in flies:
        fly.draw()
        fly.updateAnimation()
        if fly.rect.top >= screenHeight:
            fly.rect.x = random.randint(0, screenWidth)
            fly.rect.y = random.randint(0, screenHeight * 0.75)

    flies = collisionCheck(frog, flies)

    # Check if Alive
    if frog.rect.top >= screenHeight:
        run = False

    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a:
                moveLeft = True
            if event.key == pygame.K_d:
                moveRight = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moveLeft = False
            if event.key == pygame.K_d:
                moveRight = False

    pygame.display.update()

pygame.quit()
