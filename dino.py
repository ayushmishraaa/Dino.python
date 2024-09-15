import pygame
import os
import random

pygame.init()

# Screen dimensions and settings
width, height = 600, 400
FPS = 60
gravity = 0.6
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dino Run - Black and White")
clock = pygame.time.Clock()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
bg_color = white

# Load and convert images to black and white
def load_image(name, size=None):
    path = os.path.join('resources', name)
    image = pygame.image.load(path).convert()
    image = pygame.transform.scale(image, size) if size else image
    return pygame.transform.threshold(image, black, (0, 0, 0), 0, pygame.THRESHOLD_SIMPLE)

def load_sprite_sheet(name, cols, rows, size=None):
    path = os.path.join('resources', name)
    sheet = pygame.image.load(path).convert()
    sheet = pygame.transform.threshold(sheet, black, (0, 0, 0), 0, pygame.THRESHOLD_SIMPLE)
    sprite_width = sheet.get_width() // cols
    sprite_height = sheet.get_height() // rows
    sprites = []
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
            image = pygame.Surface(rect.size).convert()
            image.blit(sheet, (0, 0), rect)
            if size:
                image = pygame.transform.scale(image, size)
            sprites.append(image)
    return sprites

# Define classes
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = load_sprite_sheet('dino.png', 5, 1, (44, 47))
        self.rect = self.images[0].get_rect(topleft=(width / 15, height * 0.98))
        self.image = self.images[0]
        self.jumping = False
        self.ducking = False
        self.score = 0
        self.counter = 0
        self.gravity = gravity
        self.jump_speed = 11.5
        self.movement = [0, 0]

    def update(self):
        if self.jumping:
            self.movement[1] += self.gravity
        if self.rect.bottom > height * 0.98:
            self.rect.bottom = height * 0.98
            self.jumping = False
        self.rect = self.rect.move(self.movement)

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.movement[1] = -self.jump_speed

class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = load_sprite_sheet('cactus-small.png', 3, 1, (40, 40))
        self.image = self.images[0]
        self.rect = self.image.get_rect(topleft=(width, height * 0.98))
        self.movement = [-5, 0]

    def update(self):
        self.rect.x += self.movement[0]
        if self.rect.right < 0:
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('ground.png', (width, 50))
        self.rect = self.image.get_rect(bottomleft=(0, height))
        self.movement = [-5, 0]

    def update(self):
        self.rect.x += self.movement[0]
        if self.rect.right < 0:
            self.rect.left = width

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('cloud.png', (90, 30))
        self.rect = self.image.get_rect(topleft=(width, random.randint(50, height / 2)))
        self.movement = [-1, 0]

    def update(self):
        self.rect.x += self.movement[0]
        if self.rect.right < 0:
            self.kill()

def main():
    dino = Dino()
    ground = Ground()
    all_sprites = pygame.sprite.Group(dino, ground)
    cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
        
        all_sprites.update()
        cacti.update()
        clouds.update()

        # Spawn new obstacles
        if random.randint(1, 100) == 1:
            cactus = Cactus()
            all_sprites.add(cactus)
            cacti.add(cactus)
        
        if random.randint(1, 150) == 1:
            cloud = Cloud()
            all_sprites.add(cloud)
            clouds.add(cloud)
        
        # Collision detection
        if pygame.sprite.spritecollideany(dino, cacti):
            running = False
        
        # Drawing
        screen.fill(bg_color)
        all_sprites.draw(screen)
        pygame.display.flip()
        
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
