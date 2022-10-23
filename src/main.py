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
keyboard_map = "AZERTY"

# FUNCTION --------------------------------------------------------------------
def show_fps(caption=""):
    fps = clock.get_fps()
    str_fps = "{} - {:.2f} FPS".format(caption, fps)
    pygame.display.set_caption(str_fps)

def light_effect(display, n, radius, pos, offset, color=(15, 15, 15), hide_screen=True):
    color = (180, 167, 100)

    pos = list(pos)
    pos[0] += offset[0]
    pos[1] += offset[1]

    radius_increment = radius / n

    #fill rest of the circle & screen in black
    surf = surface = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surface, color, (radius, radius), radius)
    x = pos[0] - radius
    y = pos[1] - radius
    rect = surface.get_rect()
    rect.x = x
    rect.y = y
    display.blit(surface, (x, y), special_flags=pygame.BLEND_RGB_MIN)
    
    # aplly n circle with alpha incr
    surface = pygame.Surface(display.get_size(), pygame.SRCALPHA)
    start_alpha = 15
    alpha_increment = (255 - start_alpha) / (n + 1)
    color_alpha = [color[0], color[1], color[2], 255 - start_alpha]
    for i in range(0, n):
        pygame.draw.circle(surface, color_alpha, pos, radius)
        color_alpha[3] -= alpha_increment
        radius -= radius_increment
    display.blit(surface, (0, 0))    

    # fill all the screen black except central clight circle
    WIDTH, HEIGHT = display.get_size()
    rect1 = pygame.Rect(0, 0, WIDTH, rect.y)
    rect2 = pygame.Rect(0, 0, rect.x, HEIGHT)
    rect3 = pygame.Rect(0, rect.y + rect.h, WIDTH, HEIGHT - (rect.y + rect.h))
    rect4 = pygame.Rect(rect.x + rect.w, 0, WIDTH - (rect.x + rect.w), HEIGHT)
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

def get_level_size():
    path = "../data/level/map.json"
    with open(path, "r") as f:
        data = json.load(f)
        level = []
        height = data["layers"][0]["height"]
        width = data["layers"][0]["width"]
    return width, height

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

    def collision(self):
        w, h = get_level_size()
        if self.pos[0] < 0:
            self.pos[0] = 0
        elif self.pos[0] + self.rect.w > w * 16:
            self.pos[0] = w * 16 - self.rect.w

        if self.pos[1] < 0:
            self.pos[1] = 0
        elif self.pos[1] + self.rect.h > h * 16:
            self.pos[1] = h * 16 - self.rect.h

    def get_center_pos(self):
        return (self.pos[0]+ self.rect.w / 2, self.pos[1] + self.rect.h / 2)

    def update(self, keys, dt):
        self.input(keys, dt)
        self.collision()

    def draw(self, display, offset):
        display.blit(self.img, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


# Not Global Var ------------------------------------------------------------------
offset = [0, 0]
controls = change_controls()
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
            if event.key == pygame.K_v:
                if keyboard_map == "AZERTY":
                    keyboard_map = "QWERTY"
                else:
                    keyboard_map = "AZERTY"
                controls = change_controls(keyboard_map=keyboard_map)

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
    screen.fill((74, 94, 47))

    draw_level(screen, level, table, 16, offset)
    light_effect(screen, 10, 60, player.get_center_pos(), offset, hide_screen=True)
    player.draw(screen, offset)

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
