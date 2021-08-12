import pygame
import random
import math
import time

# ----- Window Initializations ----- #
pygame.init()
screenWidth = 480
screenHeight = 640
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("CSC Pygame Sample -- Flopping Frog")
pygame.display.set_icon(pygame.image.load('data/img/frog.png'))
font = pygame.font.Font("data/font/KGHAPPYSolid.ttf", 18)
scoreFont = pygame.font.Font("data/font/KGHAPPYSolid.ttf", 70)
entryFont = pygame.font.Font("data/font/KGHAPPYSolid.ttf", 40)
scoreWidth = 0
scoreHeight = 0

# ----- Game Variables ----- #
grav = 0.25

BG = pygame.Color('#BEE0B4')
startIMG = pygame.image.load('data/img/startbtn.png').convert_alpha()
exitIMG = pygame.image.load('data/img/exitbtn.png').convert_alpha()
logo = pygame.image.load('data/img/logo.png').convert_alpha()
logoRect = logo.get_rect()
logoRect.x = (screenWidth / 2) - 184
logo = pygame.transform.scale(logo, (int(logo.get_width() * .4), int(logo.get_height() * .4)))

background = pygame.image.load('data/img/bg.png').convert_alpha()
background = pygame.transform.scale(background, (int(background.get_width() * 1.3), int(background.get_height() * 1.3)))
backgroundRect = background.get_rect()
backgroundTwo = pygame.image.load('data/img/bg.png').convert_alpha()
backgroundTwo = pygame.transform.scale(backgroundTwo,
                                       (int(backgroundTwo.get_width() * 1.3), int(backgroundTwo.get_height() * 1.3)))
backgroundTwoRect = backgroundTwo.get_rect()
backgroundTwoRect.y = -640

bell = pygame.mixer.Sound('data/sound/bell.wav')
bell.set_volume(.5)
coin = pygame.mixer.Sound('data/sound/coin.wav')
death = pygame.mixer.Sound('data/sound/death.wav')

fliesCollected = 0

moveLeft = False
moveRight = False
clock = pygame.time.Clock()
FPS = 60


# ----- Functions and Classes ----- #
def draw_bg():
    # screen.fill(BG)
    screen.blit(background, (0, backgroundRect.y))
    screen.blit(background, (0, backgroundTwoRect.y))


class Button():
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * scale), int(image.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and (self.clicked is False):
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action


class Fly(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.animationList = []
        self.frameIndex = 0
        self.updateTime = pygame.time.get_ticks()
        for i in range(60):
            img = pygame.image.load(f'data/img/fly/{i}.png').convert_alpha()
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
            if (frog.flyCount % 10 == 0) and (frog.flyCount != 0):
                coin.play()
                frog.score += 500
            else:
                bell.play()
            frog.flyCount += 1

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
        img = pygame.image.load("data/img/frog.png").convert_alpha()
        # Object
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        )
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.boost = False
        self.flyCount = 0
        self.score = 0

        # Direction

        self.speed = speed
        self.direction = 1
        self.flip = False
        self.inAir = True
        self.velY = 0

    def draw(self):

        if ((self.flyCount - 1) % 10 == 0) and self.flyCount > 5:
            image = "froglow"
        elif self.velY < -3:
            image = "frogjump"
        elif moveLeft:
            image = "frogleft"
        elif moveRight:
            image = "frogright"
        else:
            image = "frog"
        image = f"data/img/{image}.png"
        image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(
            image, (int(image.get_width() * 0.17), int(image.get_height() * 0.17))
        )
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
        self.score -= self.velY

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
            self.boost = True
            self.velY = -9

    def getScore(self):
        return self.score

    def getFlyCount(self):
        return self.flyCount


def updateFPS():
    fps = str(int(clock.get_fps()))
    fpsText = font.render(fps, 1, pygame.Color("#2F4F4F"))
    return fpsText


def displayFlyCount():
    count = 'FLY COUNT: ' + str(frog.getFlyCount() - 1)
    flyCountText = font.render(count, 1, pygame.Color('#2F4F4F'))
    return flyCountText


def displayScore(score: int):
    if score == 0:
        score = 'Jump to the sky!'
        scoreText = entryFont.render(score, 1, pygame.Color('#2F4F4F'))
    else:
        score = str(int(score / 10))
        scoreText = scoreFont.render(score, 1, pygame.Color('#2F4F4F'))
    global scoreWidth
    scoreWidth = scoreText.get_width()
    global scoreHeight
    scoreHeight = scoreText.get_height()
    return scoreText


def camera():
    if frog.rect.top <= screenHeight / 3:
        backgroundRect.y += abs(frog.velY)
        backgroundTwoRect.y += abs(frog.velY)
        frog.rect.y += abs(frog.velY)
        for fly in flies:
            fly.rect.y += abs(frog.velY)
    if backgroundRect.top >= screenHeight:
        backgroundRect.y = -640
    if backgroundTwoRect.top >= screenHeight:
        backgroundTwoRect.y = -640


flies = []
n = 6
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
        # frog.isHit = False

    return flies


initialBoost = Fly(screenWidth / 2, screenHeight - 150, .1)
frog = Frog(screenWidth / 2, screenHeight - 150, 0.17, 5)

startBTN = Button((screenWidth / 4) - 100, screenHeight // 1.75, startIMG, 0.25)
exitBTN = Button((3 * (screenWidth / 4)) - 125, screenHeight // 1.75, exitIMG, 0.25)

menuScore = 0

# ----- Main Game Loop ----- #
mainMenu = True
run = True
while run:
    clock.tick(FPS)

    draw_bg()

    screen.blit(updateFPS(), (10, 5))

    if mainMenu:
        # screen.blit(logo, logoRect)
        screen.blit(logo, (screen.get_width() / 2 - logo.get_width() / 2,
                           screen.get_height() / 2 - 130 - logo.get_height() / 2 + math.sin(time.time() * 5) * 5 - 25))

        screen.blit(displayScore(menuScore), ((screenWidth / 2) - scoreWidth / 2, (screenHeight / 2) - 25))

        if startBTN.draw():
            mainMenu = False
        if exitBTN.draw():
            death.play()
            run = False

    else:
        screen.blit(displayFlyCount(), (screenWidth - 165, 5))
        screen.blit(displayScore(frog.getScore()), ((screenWidth / 2) - scoreWidth / 2, (screenHeight / 2) - 230))

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
        if frog.rect.top >= screenHeight and mainMenu is False:
            menuScore = frog.getScore()
            death.play()
            frog = Frog(screenWidth / 2, screenHeight - 150, 0.17, 5)
            initialBoost = Fly(screenWidth / 2, screenHeight - 150, .1)
            for fly in flies:
                fly.rect.x = random.randint(0, screenWidth)
                fly.rect.y = random.randint(0, screenHeight * 0.75)

            mainMenu = True

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moveLeft = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moveRight = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    moveLeft = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    moveRight = False

    for event in pygame.event.get():
        # Quit Game
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
