import pygame

def load_tileset_1d(path, tile_width, tile_height, resize=1):
    image = pygame.image.load(path).convert_alpha()
    image_width, image_height = image.get_size()

    tile_table = []
    for tile_x in range(0, int(image_width / tile_width)):
        for tile_y in range(0, int(image_height / tile_height)):
            rect = (tile_x * tile_width, tile_y * tile_height, 
                    tile_width, tile_height)
            img = image.subsurface(rect)
            if resize != 1:
                w, h = img.get_size()
                img = pygame.transform.scale(img, (w * resize, h * resize))
            tile_table.append(img)
    return tile_table

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

def change_anim(anim, list_anim, animationGroup):
    for key in list_anim:
        if key == anim:
            animationGroup.add(list_anim[key])
        else:
            try:
                animationGroup.remove(list_anim[key])
            except Exception:
                pass


class Animation(pygame.sprite.Sprite):
    def __init__(self, x, y, image_list, speed=3, loop=False):
        pygame.sprite.Sprite.__init__(self)

        self.images = image_list

        self.index = 0 
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.counter = 0

        self.speed = speed
        self.loop = loop

    def update(self):
        # update anim
        self.counter += 1

        if self.counter >= self.speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if animation complete
        if self.index >= len(self.images) - 1 and self.counter >= self.speed:
            if not self.loop:
                self.kill()
            else:
                self.counter = 0
                self.index = 0
                self.image = self.images[self.index]
