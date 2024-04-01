import pygame
import random

pygame.init()

W, H = 1200, 800
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (0, 0, 0)


class Paddle:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.rect = pygame.Rect(W // 2 - self.width // 2, H - self.height - 30, self.width, self.height)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed

    def move_right(self):
        if self.rect.right < W:
            self.rect.right += self.speed

    def shrink(self, reduction_rate):
        if self.width > 10:
            self.width -= reduction_rate
            self.rect.width = self.width


# Ball
ballRadius = 15
ballSpeed = 6
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1


acceleration = 0.001


game_score = 0
game_score_fonts = pygame.font.SysFont('comicsansms', 40)
game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (0, 0, 0))
game_score_rect = game_score_text.get_rect()
game_score_rect.center = (210, 20)


collision_sound = pygame.mixer.Sound('catch.mp3')

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    if delta_x > delta_y:
        if rect.top < ball.centery < rect.bottom:
            dy = -dy
            ball.y += dy
        elif rect.left < ball.centerx < rect.right:
            dx = -dx
            ball.x += dx
    elif delta_y > delta_x:
        if rect.left < ball.centerx < rect.right:
            dx = -dx
            ball.x += dx
        elif rect.top < ball.centery < rect.bottom:
            dy = -dy
            ball.y += dy
    return dx, dy


block_list = []
color_list = []


for i in range(10):
    for j in range(4):
        if random.random() < 0.1:
            color = (100, 100, 100)
            unbreakable = True
        else:
            color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))  # Random color for breakable bricks
            unbreakable = False
        block = pygame.Rect(10 + 120 * i, 50 + 70 * j, 100, 50)
        block_list.append((block, unbreakable))
        color_list.append(color)



losefont = pygame.font.SysFont('comicsansms', 40)
losetext = losefont.render('Game Over', True, (255, 255, 255))
losetextRect = losetext.get_rect()
losetextRect.center = (W // 2, H // 2)


winfont = pygame.font.SysFont('comicsansms', 40)
wintext = losefont.render('You win yay', True, (0, 0, 0))
wintextRect = wintext.get_rect()
wintextRect.center = (W // 2, H // 2)

paddle = Paddle(150, 100, 20)  # Creating paddle object

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(bg)


    for idx, (block, unbreakable) in enumerate(block_list):
        pygame.draw.rect(screen, color_list[idx], block)

    pygame.draw.rect(screen, pygame.Color(255, 255, 255), paddle.rect)
    pygame.draw.circle(screen, pygame.Color(255, 0, 0), ball.center, ballRadius)

    ball.x += ballSpeed * dx
    ball.y += ballSpeed * dy


    ballSpeed += acceleration

    if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
        dx = -dx
    if ball.centery < ballRadius + 50:
        dy = -dy
    if paddle.rect.colliderect(ball) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle.rect)

    hitIndex = ball.collidelist([block[0] for block in block_list])

    if hitIndex != -1:
        hitRect, unbreakable = block_list[hitIndex]
        if not unbreakable:
            block_list.pop(hitIndex)
            color_list.pop(hitIndex)
            dx, dy = detect_collision(dx, dy, ball, hitRect)
            game_score += 1
            collision_sound.play()
            paddle.shrink(1)
        else:
            dx, dy = detect_collision(dx, dy, ball, hitRect)

    game_score_text = game_score_fonts.render(f'Your game score is: {game_score}', True, (255, 255, 255))
    screen.blit(game_score_text, game_score_rect)

    if ball.bottom > H:
        screen.fill((0, 0, 0))
        screen.blit(losetext, losetextRect)
    elif not len(block_list):
        screen.fill((255, 255, 255))
        screen.blit(wintext, wintextRect)

    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        paddle.move_left()
    if key[pygame.K_RIGHT]:
        paddle.move_right()

    pygame.display.flip()
    clock.tick(FPS)
