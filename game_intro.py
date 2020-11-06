import sys
import pygame

size = width, height = 1200, 800
speed = [1, 1]  # this is a vector [left-right speed, top-down speed]
black = 0, 0, 0

screen = pygame.display.set_mode(size)


class Ball:
    def __init__(self, image_path, speed: list = None):
        self.speed = speed or [1, 1]
        self.ball = pygame.image.load(image_path)
        self.rect = self.ball.get_rect()

    def getDirection(self, speed1: int = 0, speed2: int = 0):
        if (speed1 > 0 and speed2 > 0) or (speed1 < 0 and speed2 < 0):
            return 1
        return -1

    def checkCollision(self, other):
        vertical = bool((self.rect.top < other.rect.bottom and self.rect.top > other.rect.top) or (
                self.rect.bottom > other.rect.top > self.rect.top))
        horizontal = bool((self.rect.left < other.rect.right and self.rect.left > other.rect.left) or (
                self.rect.right > other.rect.left > self.rect.left))
        if vertical and horizontal:
            xDirection = self.getDirection(self.speed[0], other.speed[0])
            yDirection = self.getDirection(self.speed[1], other.speed[1])
            self.speed[0] = self.speed[0] * xDirection
            other.speed[0] = other.speed[0] * xDirection
            self.speed[1] = self.speed[1] * yDirection
            other.speed[1] = other.speed[1] * yDirection

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.left < 0 or self.rect.right > width:
            self.speed[0] = -self.speed[0]
        if self.rect.top < 0 or self.rect.bottom > height:
            self.speed[1] = -self.speed[1]
        for ball in balls:
            if ball != self:
                self.checkCollision(ball)

    def speedUp(self):
        if self.speed[0] > 0:
            self.speed[0] = self.speed[0] + 1
        else:
            self.speed[0] = self.speed[0] - 1
        if self.speed[1] > 0:
            self.speed[1] = self.speed[1] + 1
        else:
            self.speed[1] = self.speed[1] - 1

    def slowDown(self):
        if self.speed[0] > 1:
            self.speed[0] = self.speed[0] - 1
        elif self.speed[0] < -1:
            self.speed[0] = self.speed[0] + 1
        if self.speed[1] > 1:
            self.speed[1] = self.speed[1] - 1
        elif self.speed[1] < -1:
            self.speed[1] = self.speed[1] + 1


first_ball = Ball(image_path="./images/intro_ball.gif")

balls = [first_ball]


def add_ball(image_path: str = None):
    image_path = image_path or "./images/soccer_ball.gif"
    another_ball = Ball(image_path=image_path, speed=[1, 1])
    balls.append(another_ball)

def remove_ball():
    balls.pop()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_UP]:
                add_ball()
            elif pressed[pygame.K_DOWN]:
                remove_ball()
            elif pressed[pygame.K_KP_PLUS]:
                for b in balls: b.speedUp()
            elif pressed[pygame.K_KP_MINUS]:
                for b in balls: b.slowDown()

    for ball in balls:
        ball.move()
    screen.fill(black)
    for ball in balls:
        screen.blit(ball.ball, ball.rect)

    pygame.display.flip()
