import pygame

# CONSTANTE -------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

display = pygame.display.set_mode((1000, 600), pygame.RESIZABLE)
pygame.display.set_caption("Pump'keet up")
pygame.display.set_icon(pygame.image.load("../data/sprite/icon.png").convert())
screen = pygame.Surface((500, 300))
clock = pygame.time.Clock()

# LOAD ------------------------------------------------------------------------
pumpkin = pygame.image.load("../data/sprite/pumpkin.png")


# FUNCTION --------------------------------------------------------------------
def show_fps(caption=""):
    fps = clock.get_fps()
    str_fps = "{} - {:.2f} FPS".format(caption, fps)
    pygame.display.set_caption(str_fps)


def light_effect(display, n, radius, pos, color=(80, 70, 20), hide_screen=True):
    rect = None
    radius_increment = radius / n
    # create n gradient of light
    for i in range(0, n):
        surface = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surface, color, (radius, radius), radius)
        x = pos[0] - radius
        y = pos[1] - radius
        if i == 0:
            rect = surface.get_rect()
            rect.x = x
            rect.y = y
            display.blit(surface, (x, y), special_flags=pygame.BLEND_RGB_MIN)
        display.blit(surface, (x, y), special_flags=pygame.BLEND_RGB_ADD)
        radius -= radius_increment
    if hide_screen:
        width, height = display.get_size()
        rect1 = pygame.Rect(0, 0, width, rect.y)
        rect2 = pygame.Rect(0, 0, rect.x, height)
        rect3 = pygame.Rect(0, rect.y + rect.h, width, height - (rect.y + rect.h))
        rect4 = pygame.Rect(rect.x + rect.w, 0, width - (rect.x + rect.w), height)
        BLACK = (0, 0, 0)
        display.fill(BLACK, rect=rect1)
        display.fill(BLACK, rect=rect2)
        display.fill(BLACK, rect=rect3)
        display.fill(BLACK, rect=rect4)


# CLASS -----------------------------------------------------------------------
class Player:
    def __init__(self):
        self.img = pumpkin
        self.pos = [250, 150]
        self.rect = self.img.get_rect()

    def input(self, keys):
        x_move, y_move = 0, 0
        speed = 1
        if keys[pygame.K_z]:
            y_move -= 1
        if keys[pygame.K_s]:
            y_move += 1
        if keys[pygame.K_d]:
            x_move += 1
        if keys[pygame.K_q]:
            x_move -= 1

        self.pos[0] += x_move
        self.pos[1] += y_move

    def get_center_pos(self):
        return (self.pos[0]+ self.rect.w / 2, self.pos[1] + self.rect.h / 2)

    def update(self, keys):
        self.input(keys)

    def draw(self, display):
        display.blit(self.img, self.pos)


# Not Global Var ------------------------------------------------------------------
player = Player()

# MAINLOOP --------------------------------------------------------------------
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.VIDEORESIZE:
            display = pygame.display.set_mode(event.size, pygame.RESIZABLE)
    pos = pygame.mouse.get_pressed()
    keys = pygame.key.get_pressed()
# UPDATE ----------------------------------------------------------------------
    player.update(keys)
    show_fps("Pump'keet up")

# DRAW ------------------------------------------------------------------------
    display.fill(BLACK)
    screen.fill(BLACK)

    player.draw(screen)
    light_effect(screen, 3, 80, player.get_center_pos())

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
