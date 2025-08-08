import sys
import pygame

WIDTH, HEIGHT = 600, 800
GRAVITY = 0.5


class Ball:
    def __init__(self):
        self.radius = 10
        self.reset()

    def reset(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.vx = 4
        self.vy = -10

    def update(self, flippers):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0:
            self.vy *= -1
        if self.y - self.radius > HEIGHT:
            self.reset()

        ball_rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                self.radius * 2, self.radius * 2)
        for f in flippers:
            if ball_rect.colliderect(f.rect()):
                self.vy = -abs(self.vy)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)


class Flipper:
    def __init__(self, left):
        self.width = 80
        self.height = 15
        self.angle = 0
        self.left = left
        self.base_y = HEIGHT - 40
        self.base_x = 120 if left else WIDTH - 120
        self.active = False

    def update(self):
        target_angle = -30 if self.active else 0
        speed = 5
        if self.angle < target_angle:
            self.angle += speed
        elif self.angle > target_angle:
            self.angle -= speed

    def rect(self):
        rect = pygame.Rect(0, 0, self.width, self.height)
        rect.center = (self.base_x, self.base_y)
        return rect

    def draw(self, screen):
        rect = self.rect()
        surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, (200, 200, 0), (0, 0, rect.width, rect.height))
        rotated = pygame.transform.rotate(surface, self.angle if self.left else -self.angle)
        new_rect = rotated.get_rect(center=rect.center)
        screen.blit(rotated, new_rect.topleft)


def main(test_mode=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mini Pinball")
    clock = pygame.time.Clock()

    ball = Ball()
    flippers = [Flipper(True), Flipper(False)]

    frames = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    flippers[0].active = True
                elif event.key == pygame.K_RIGHT:
                    flippers[1].active = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    flippers[0].active = False
                elif event.key == pygame.K_RIGHT:
                    flippers[1].active = False

        screen.fill((0, 0, 0))

        ball.update(flippers)
        ball.draw(screen)

        for f in flippers:
            f.update()
            f.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        frames += 1
        if test_mode and frames > 10:
            running = False

    pygame.quit()


if __name__ == "__main__":
    test = "--test" in sys.argv
    main(test_mode=test)
