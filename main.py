import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("BALL SMASH")
fps = pygame.time.Clock()

# Abstraction: Buat kelas Game sebagai parent kelas untuk game apapun
class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def run(self):
        self.initialize()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.render()
            self.clock.tick(30)

        pygame.quit()
        sys.exit()

    def initialize(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

# Encapsulation: Buat kelas Ball untuk mengelola bola di game
class Ball:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def move(self):
        self.x += self.speed * self.direction_x
        self.y += self.speed * self.direction_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Inheritance: Buat kelas pong yang merupakan sub kelas dari Game
class Pong(Game):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.player_paddle = Paddle(20, height // 2 - 50, 20, 100, (255, 0, 0), 5, pygame.K_w, pygame.K_s)
        self.opponent_paddle = Paddle(width - 40, height // 2 - 50, 20, 100, (0, 0, 255), 5)
        self.ball = Ball(width // 2, height // 2, 10, (0, 255, 0), 5)

    def initialize(self):
        pass

    def update(self):
        self.player_paddle.move()
        self.opponent_paddle.move(self.ball)
        self.ball.move()

        #batas atas dan batas bawahnya
        if self.ball.y <= self.ball.radius or self.ball.y >= self.height - self.ball.radius:
            self.ball.direction_y *= -1

        #tabrakan dengan pemukul
        if (self.ball.x - self.ball.radius <= self.player_paddle.x + self.player_paddle.width and
                self.player_paddle.y <= self.ball.y <= self.player_paddle.y + self.player_paddle.height):
            self.ball.direction_x *= -1

        if (self.ball.x + self.ball.radius >= self.opponent_paddle.x and
                self.opponent_paddle.y <= self.ball.y <= self.opponent_paddle.y + self.opponent_paddle.height):
            self.ball.direction_x *= -1

        #ini mengecek ketika bolanya memantul atau bounce
        if self.ball.x - self.ball.radius <= 0 or self.ball.x + self.ball.radius >= self.width:
            self.reset_ball()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.player_paddle.draw(self.screen)
        self.opponent_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()

    def reset_ball(self):
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        self.ball.direction_x = random.choice([-1, 1])
        self.ball.direction_y = random.choice([-1, 1])

# Polymorphism: Buat class Paddle sebagai parent class untuk pemain dan lawan
class Paddle:
    def __init__(self, x, y, width, height, color, speed, up_key=None, down_key=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key

    def move(self, ball=None):
        keys = pygame.key.get_pressed()
        if self.up_key:
            if keys[self.up_key] and self.y > 0:
                self.y -= self.speed
        if self.down_key:
            if keys[self.down_key] and self.y < 600 - self.height:
                self.y += self.speed
        if ball:
            if ball.y < self.y + self.height // 3:
                self.y -= self.speed
            elif ball.y > self.y + self.height // 3:
                self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

if __name__ == "__main__":
    pong = Pong(800, 500)
    pong.run()
