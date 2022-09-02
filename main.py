import random

import pygame as pg

pg.init()

clock = pg.time.Clock()

fps = 60

# setting screen size

SCREEN_WIDTH = 864
SCREEN_HEIGHT = 936
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# giving title to the window
pg.display.set_caption("Jignesh bird")


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    jignesh.rect.x = 100
    jignesh.rect.y = SCREEN_HEIGHT // 2
    score = 0


# DEFINE game variables

ground_scroll = 0
velocity = 0
pipe_gap = 150
game_over = False
pipe_freq = 1550  # mili-seconds
pipe_pass = False
score = 0
last_pipe = pg.time.get_ticks()

"""score"""
font = pg.font.SysFont("bauhaus 93", 60)

red = (255, 70, 220)

# displacement of x-axis of the ground.png
scroll_speed = 3
# how fast is the displacement taking place

# loading images
bg = pg.image.load("img/bg.png")
ground_img = pg.image.load("img/ground.png")
butt_img = pg.image.load("img/restart.png")


class bird(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        # creating list of images that we are loading
        self.images = []
        for num in range(1, 4):
            img = pg.image.load(f"img/bird{num}.png")
            self.images.append(img)

        self.index = 0
        # index of which image is currently being shown on screen
        self.counter = 0
        # acts as a pause between each image
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()  # hit box of the bird
        self.rect.center = [x, y]
        self.velocity = 0

    def update(self, up=0):
        if start == True:
            self.velocity += 0.2
            if self.velocity >= 9.8:
                self.velocity = 9.8
            if up == 1:
                self.velocity = -5
            if self.rect.bottom <= 768 and self.rect.top > 0:
                self.rect.y += int(self.velocity)

        # print(self.velocity)

        # image updates
        self.counter += 1
        jignesh_cd = 30

        if self.counter > jignesh_cd:
            self.counter = 0
            self.index += 1

            if (self.index >= 3):
                self.index = 0
        self.image = self.images[self.index]

        self.image = pg.transform.rotate(self.images[self.index], self.velocity * - 2)


class pipe(pg.sprite.Sprite):
    def __init__(self, x, y, position):

        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("img/pipe.png")
        self.rect = self.image.get_rect()

        if position == 1:  # 1 means pipe is coming from the top of the screen
            self.image = pg.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        else:
            self.rect.topleft = [x, y + pipe_gap // 2]

    def update(self):
        if start == True:
            self.rect.x -= scroll_speed
            if self.rect.right < 0:
                self.kill()


class button(pg.sprite.Sprite):

    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topright = (x, y)

    def draw(self):

        action = False

        pos = pg.mouse.get_pos()

        if self.rect.collidepoint(pos):

            if pg.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pg.sprite.Group()
pipe_group = pg.sprite.Group()
butt = button(int(65 + SCREEN_WIDTH / 2), SCREEN_HEIGHT // 2, butt_img)

jignesh = bird(100, SCREEN_HEIGHT // 2)

bird_group.add(jignesh)

run = True
start = False
game_over = False
""" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MAIN LOOP~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"""
while run:

    clock.tick(fps)
    # draw a background
    screen.blit(bg, (0, 0))
    if game_over:
        butt.draw()
        if butt.draw() == True:
            reset_game()
            score = 0

            game_over = False

    # draw and scroll the ground

    if len(pipe_group) > 0:

        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.left < pipe_group.sprites()[0].rect.right and pipe_pass == False:
            pipe_pass = True
        if pipe_pass and bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
            pipe_pass = False
            score += 1

    draw_text(str(score), font, red, int(SCREEN_WIDTH / 2), 50)
    # print(score)

    screen.blit(ground_img, (ground_scroll, 768))
    if game_over == False:
        bird_group.draw(screen)
        bird_group.update()

        pipe_group.draw(screen)
        pipe_group.update()

        if pg.sprite.groupcollide(pipe_group, bird_group, False, False) or jignesh.rect.top < 0:
            game_over = True

        time_now = pg.time.get_ticks()

        # Generating new pipes
        if time_now - last_pipe > pipe_freq:
            h_diff = random.randint(-150, 150)

            top_pipe = pipe(SCREEN_WIDTH, h_diff + SCREEN_HEIGHT // 2, 1)
            btm_pipe = pipe(SCREEN_WIDTH, h_diff + SCREEN_HEIGHT // 2, -1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        ground_scroll -= scroll_speed

    if abs(ground_scroll) > 36 or game_over == True:
        ground_scroll = 0

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_SPACE or start == False:
                start = True
                bird_group.update(1)
            if event.key == pg.K_UP:
                bird_group.update(1)

        if event.type == pg.QUIT:
            run = False

    pg.display.update()

    pg.display.flip()
