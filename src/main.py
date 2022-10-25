import json
import pygame
import random

from tools import load_tileset, load_tileset_1d, Animation, change_anim

# CST -------------------------------------------------------------------------
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WIDTH = 1000
RATIO = (16/9)
HEIGHT = round(WIDTH / RATIO)
screen_ratio = 3

FPS = 60
TILE_SIZE = 16

display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, vsync=1)
pygame.display.set_caption("Pump'keet up")
pygame.display.set_icon(pygame.image.load("../data/sprite/icon.png").convert())
screen = pygame.Surface((round(WIDTH / screen_ratio), round((WIDTH / screen_ratio) / RATIO)))
clock = pygame.time.Clock()
animation_group = pygame.sprite.Group()

# LOAD ------------------------------------------------------------------------
small_pumpkin_img = pygame.image.load("../data/sprite/small_pumpkin.png").convert_alpha()
keyboard_map = "AZERTY"
level_path = "../data/level/map.json"

speed = 4
loop = True
resize = 1
anim_player = {"up": Animation(0, 0, load_tileset_1d("../data/sprite/player/player_up.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
               "down": Animation(0, 0, load_tileset_1d("../data/sprite/player/player_down.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
               "right": Animation(0, 0, load_tileset_1d("../data/sprite/player/player_right.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
               "left": Animation(0, 0, load_tileset_1d("../data/sprite/player/player_left.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop)}
speed = 6
loop = True
resize = 1
small_pumpkin_anim = {"up": Animation(0, 0, load_tileset_1d("../data/sprite/small_pumpkin/up.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
                      "down": Animation(0, 0, load_tileset_1d("../data/sprite/small_pumpkin/down.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
                      "right": Animation(0, 0, load_tileset_1d("../data/sprite/small_pumpkin/right.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop),
                      "left": Animation(0, 0, load_tileset_1d("../data/sprite/small_pumpkin/left.png", TILE_SIZE, TILE_SIZE, resize=resize), speed=speed, loop=loop)}

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

def draw_tileset(table, display, tile_width, tile_height):
    for x, row in enumerate(table):
        for y, tile in enumerate(row):
            display.blit(tile, (x * tile_width, y * tile_height))

def load_level(path=level_path):
    with open(path, "r") as f:
        data = json.load(f)
        level = []
        height = data["layers"][0]["height"]
        width = data["layers"][0]["width"]

        level = []
        mob_spawn = []
        for layers in data["layers"]:
            if layers["name"] == "Objects":
                for objects in layers["objects"]:
                    rect = pygame.Rect(int(objects["x"]), int(objects["y"]), int(objects["width"]), int(objects["height"]))
                    mob_spawn.append(pygame.Rect(rect))
            else:
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
    return level, mob_spawn

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
    x_offset, y_offset = 0, 0
    x = player.pos[0] + player.rect.w / 2
    y = player.pos[1] + player.rect.h / 2

    if x > w * (1/2) - offset[0] + player.rect.w / 2:
        x_offset =  w * (1/2) - offset[0] + player.rect.w / 2 - x
    elif x < w * (1/2) - offset[0] - player.rect.w / 2:
        x_offset = w * (1/2) - offset[0] - player.rect.w / 2 - x

    if y > h * (1/2) - offset[1] + player.rect.h / 2:
        y_offset = h * (1/2) - offset[1] + player.rect.h / 2 - y
    elif y < h * (1/2) - offset[1] - player.rect.h / 2:
        y_offset = h * (1/2) - offset[1] - player.rect.h / 2 - y

    offset[0] += x_offset
    offset[1] += y_offset
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
    path = level_path
    with open(path, "r") as f:
        data = json.load(f)
        level = []
        height = data["layers"][0]["height"]
        width = data["layers"][0]["width"]
    return width, height

def get_collision_rect(tile_with_collision, level):
    collisions = []
    for layer in level:
        for y, row in enumerate(layer):
            for x, tile in enumerate(row):
                if tile - 1 in tile_with_collision:
                    collisions.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                                  TILE_SIZE, TILE_SIZE))
    return collisions

def draw_tile_with_collision(display, collisions_rect, offset):
    for rect in collisions_rect:
        pygame.draw.rect(display, (255,0,0), (rect.x + offset[0], rect.y + offset[1], rect.w, rect.h))

def get_collision_type(entity_rect, x_move, y_move, fix_rect):
    collisions_axe = {"x": False, "y": False}
    collision_types = {"up": False,
                       "down": False,
                       "left": False,
                       "right": False}

    final_rect = pygame.Rect(entity_rect)
    final_rect.x += x_move
    if final_rect.colliderect(fix_rect):
        collisions_axe["x"] = True

    final_rect = pygame.Rect(entity_rect)
    final_rect.y += y_move
    if final_rect.colliderect(fix_rect):
        collisions_axe["y"] = True

    if collisions_axe["x"]:
        if x_move > 0:
            collision_types["right"] = True
        elif x_move < 0:
            collision_types["left"] = True
    if collisions_axe["y"]:
        if y_move > 0:
            collision_types["down"] = True
        elif y_move < 0:
            collision_types["up"] = True

    return collision_types, collisions_axe

def generate_pumpkin(mob_list):
    for i in range(0, 10):
        mob_list.append(SmallPumpkin((25, 25)))

def update_mob(mob_list):
    for i in mob_list:
        i.update()

def draw_mob(mob_list, display, offset):
    for i in mob_list:
        i.draw(display, offset)

def draw_list_rect(display, rects, color=(0, 150, 0), outline=1, offset=[0, 0]):
    for rect in rects:
        pygame.draw.rect(display, color, (rect.x + offset[0], rect.y + offset[1], rect.w, rect.h), outline)

# CLASS -----------------------------------------------------------------------
class SmallPumpkin:
    def __init__(self, pos):
        self.pos = [pos[0], pos[1]]
        self.speed = 225
        self.img = small_pumpkin_img
        self.rect = pygame.Rect(0, 0, 12, 12)

    def update(self):
        self.pos[0] += random.randint(0, 2) - 1
        self.pos[1] += random.randint(0, 2) - 1

    def draw(self, display, offset):
        display.blit(self.img, (self.pos[0] + offset[0], self.pos[1] + offset[1]))


class Player:
    def __init__(self):
        self.pos = [25, 25]
        self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.speed = 165
        self.direction = "right"
        change_anim(self.direction, anim_player, animation_group)

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

        return x_move, y_move

    def collision(self, collisions_rect, x_move, y_move):
        # level boundaries
        w, h = get_level_size()
        if self.pos[0] + x_move < 0:
            x_move = 0
        elif self.pos[0] + self.rect.w + x_move> w * 16:
            x_move = 0

        if self.pos[1] + y_move < 0:
            y_move = 0
        elif self.pos[1] + self.rect.h  + y_move > h * 16:
            y_move = 0

        final_rect = pygame.Rect(self.rect)
        final_rect.x = self.pos[0]
        final_rect.y = self.pos[1]

        for rect in collisions_rect:
            collision_types, collisions_axe = get_collision_type(final_rect, x_move, y_move, rect)
            if collisions_axe["x"]:
                x_move = 0
            if collisions_axe["y"]:
                y_move = 0

        return x_move, y_move

    def player_anim(self, x_move, y_move, offset):
        for anim in anim_player:
            anim_player[anim].rect.x = self.pos[0] + offset[0]
            anim_player[anim].rect.y = self.pos[1] + offset[1]

        old_direction = str(self.direction)

        if y_move > 0:
            self.direction = "down"
        elif y_move < 0:
            self.direction = "up"
        if x_move > 0:
            self.direction = "right"
        elif x_move < 0:
            self.direction = "left"

        if old_direction != self.direction:
            change_anim(self.direction, anim_player, animation_group)

    def get_center_pos(self):
        return (self.pos[0]+ self.rect.w / 2, self.pos[1] + self.rect.h / 2)

    def update(self, keys, dt, collisions_rect, offset):
        x_move, y_move = self.input(keys, dt)
        x_move, y_move = self.collision(collisions_rect, x_move, y_move)
        
        self.pos[0] += x_move
        self.pos[1] += y_move

        self.player_anim(x_move, y_move, offset)

    def draw(self, display, offset):
        display.blit(self.img, (self.pos[0] + offset[0], self.pos[1] + offset[1]))
        #pygame.draw.rect(display, (255,0,0), (self.pos[0] + offset[0], self.pos[1] + offset[1],
         #                                     self.rect.w, self.rect.h), 3)


# Not Global Var ------------------------------------------------------------------
offset = [0, 0]
tile_with_collision = [1, 9, 4, 12, 21, 22, 23]
controls = change_controls()
table = load_tileset("../data/sprite/tilesheet.png", 16, 16)
level, mob_spawn = load_level("../data/level/map.json")
player = Player()
mob_list = []
generate_pumpkin(mob_list)

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
    offset = update_offset(screen, player, offset, dt)
    collisions_rect = get_collision_rect(tile_with_collision, level)
    player.update(keys, dt, collisions_rect, offset)
    show_fps("Pump'keet up")
    animation_group.update()
    update_mob(mob_list)

# DRAW ------------------------------------------------------------------------
    display.fill(BLACK)
    screen.fill((74, 94, 47))

    draw_level(screen, level, table, 16, offset)
    #draw_tile_with_collision(screen, collisions_rect, offset)
    #light_effect(screen, 4, 60, player.get_center_pos(), offset, hide_screen=True)
    #player.draw(screen, offset)
    draw_mob(mob_list, screen, offset)
    animation_group.draw(screen)
    draw_list_rect(screen, mob_spawn, offset=offset)

    display.blit(pygame.transform.scale(screen, display.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
