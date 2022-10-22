import pygame
import json

# CONSTANTE -------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

FPS = 60
WIDTH = 1000
RATIO = (16/9)
HEIGHT = round(WIDTH / RATIO)
screen_ratio = 3

display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, vsync=1)
pygame.display.set_caption("Pump'keet up")
pygame.display.set_icon(pygame.image.load("../data/sprite/icon.png").convert())
screen = pygame.Surface((round(WIDTH / screen_ratio), round((WIDTH / screen_ratio) / RATIO)))
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

def load_tileset(path, tile_width, tile_height):
    image = pygame.image.load(path).convert_alpha()
    image_width, image_height = image.get_size()

    tile_table = []
    for tile_x in range(0, int(image_width / tile_width)):
        line = []
        tile_table.append(line)
        for tile_y in range(0, int(image_height / tile_height)):
            rect = (tile_x * tile_width, tile_y * tile_height, 
                    tile_width, tile_height)
            line.append(image.subsurface(rect))
    return tile_table

def draw_tileset(table, display, tile_width, tile_height):
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            display.blit(tile, (x * tile_width, y * tile_height))

def load_level(path):
    with open(path, "r") as f:
        data = json.load(f)
        level = []
        height = data["layers"][0]["height"]
        width = data["layers"][0]["width"]

        level = []
        for layers in data["layers"]:
            layer = []
            x, y = 0, 0
            row = []
            for i in layers["data"]:
                row.append(i)
                x += 1
                if x >= width:
                    x = 0
                    y += 1
                    layer.append(row)
                    row = []
            level.append(layer)
    return level

def get_tile_table_coordinate(number, tileset_width):
    if number <= 0:
        return (0, 0)
    x, y = 0, 0
    for i in range(0, number):
        x += 1
        if x > tileset_width - 1:
            y += 1
            x = 0
    return (x, y)

def draw_level(display, level, table, tile_size, offset):
    for layer in level:
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                coord = get_tile_table_coordinate(tile - 1, 8)
                display.blit(table[coord[0]][coord[1]], (x * tile_size + offset[0], y * tile_size + offset[1]))

def get_offset(screen, player_pos, offset):
    pos = [0, 0]
    pos[0] = player_pos[0] - offset[0]
    pos[1] = player_pos[1] - offset[1]

    w, h = screen.get_size()
    if pos[0] > (3/4) * w:
        offset[0] = player_pos[0] - (3/4) * w
    elif pos[0] < (1/4) * w:
        offset[0] = player_pos[0] - (1/4) * w
    return offset

def update_offset(screen, player, offset, dt):
    w, h = screen.get_size()
    if player.pos[0] + player.rect.w > (3/4) * w - offset[0]:
        offset[0] -= player.speed * dt
    elif player.pos[0] < (1/4) * w - offset[0]:
        offset[0] += player.speed * dt

    if player.pos[1] < (1/4) * h - offset[1]:
        offset[1] += player.speed * dt
    elif player.pos[1] + player.rect.h > (3/4) * h - offset[1]:
        offset[1] -= player.speed * dt

    return offset

def change_controls(keyboard_map="AZERTY"):
    controls = {"up": pygame.K_z,
                "down": pygame.K_s,
                "right": pygame.K_d,
                "left": pygame.K_q}
    if keyboard_map == "QWERTY":
        controls["up"] = pygame.K_w
        controls["left"] = pygame.K_a
    return controls

# CLASS -----------------------------------------------------------------------
class Player:
    def __init__(self):
        self.img = pumpkin
        self.pos = [100, 100]
        self.rect = self.img.get_rect()
        self.speed = 200

    def input(self, keys, dt):
        x_move, y_move = 0, 0
        speed = 1
        if keys[controls["up"]]:
            y_move -= self.speed * dt
        if keys[controls["down"]]:
            y_move += self.speed * dt
        if keys[controls["right"]]:
            x_move += self.speed * dt
        if keys[controls["left"]]:
            x_move -= self.speed * dt

        self.pos[0] += x_move
        self.pos[1] += y_move

    def get_center_pos(self):
        return (self.pos[0]+ self.rect.w / 2, self.pos[1] + self.rect.h / 2)

    def update(self, keys, dt):
        self.input(keys, dt)

    def draw(self, display, offset):
        display.blit(self.img, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


# Not Global Var ------------------------------------------------------------------
offset = [0, 0]
controls = change_controls(keyboard_map="QWERTY")
table = load_tileset("../data/sprite/tilesheet.png", 16, 16)
level = load_level("../data/level/map.json")
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
    dt = clock.tick(FPS) / 1000
# UPDATE ----------------------------------------------------------------------
    player.update(keys, dt)
    show_fps("Pump'keet up")
    offset = update_offset(screen, player, offset, dt)
    

# DRAW ------------------------------------------------------------------------
    display.fill(BLACK)
    screen.fill(BLACK)

    draw_level(screen, level, table, 16, offset)
    #light_effect(screen, 3, 50, player.get_center_pos(), hide_screen=True)
    player.draw(screen, offset)

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
