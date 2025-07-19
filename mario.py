import pygame
import sys

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
GRAVITY = 0.8

# Level representation: '.' empty, '#' block, 'P' player start, 'G' enemy
LEVEL = [
    "........................................",
    "........................................",
    "........................................",
    "........................................",
    "........................................",
    "............##########.................",
    "........................................",
    "#####.............................######",
    "......G.................................",
    "P.......................................",
]

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False

    def update(self, tiles):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel.x = -5
        elif keys[pygame.K_RIGHT]:
            self.vel.x = 5
        else:
            self.vel.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel.y = -15
            self.on_ground = False

        self.vel.y += GRAVITY

        self.rect.x += self.vel.x
        self.handle_collision(tiles, 'horizontal')
        self.rect.y += self.vel.y
        self.handle_collision(tiles, 'vertical')

    def handle_collision(self, tiles, direction):
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if direction == 'horizontal':
                    if self.vel.x > 0:
                        self.rect.right = tile.rect.left
                    elif self.vel.x < 0:
                        self.rect.left = tile.rect.right
                elif direction == 'vertical':
                    if self.vel.y > 0:
                        self.rect.bottom = tile.rect.top
                        self.vel.y = 0
                        self.on_ground = True
                    elif self.vel.y < 0:
                        self.rect.top = tile.rect.bottom
                        self.vel.y = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(-2, 0)

    def update(self, tiles):
        self.rect.x += self.vel.x
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vel.x > 0:
                    self.rect.right = tile.rect.left
                else:
                    self.rect.left = tile.rect.right
                self.vel.x *= -1
                break

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill((139, 69, 19))
        self.rect = self.image.get_rect(topleft=(x, y))


def build_level(level_map):
    tiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    player = None
    y = 0
    for row in level_map:
        x = 0
        for char in row:
            if char == '#':
                tile = Tile(x * TILE_SIZE, y * TILE_SIZE)
                tiles.add(tile)
            elif char == 'P':
                player = Player(x * TILE_SIZE, y * TILE_SIZE)
            elif char == 'G':
                enemy = Enemy(x * TILE_SIZE, y * TILE_SIZE)
                enemies.add(enemy)
            x += 1
        y += 1
    return tiles, enemies, player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    tiles, enemies, player = build_level(LEVEL)

    all_sprites = pygame.sprite.Group(tiles, enemies, player)

    camera_offset = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player.update(tiles)
        enemies.update(tiles)

        # Check collisions with enemies
        if pygame.sprite.spritecollide(player, enemies, False):
            print("Game Over!")
            pygame.quit()
            sys.exit()

        # Camera follows player
        camera_offset = max(0, player.rect.centerx - SCREEN_WIDTH // 2)

        screen.fill((135, 206, 235))

        for tile in tiles:
            screen.blit(tile.image, (tile.rect.x - camera_offset, tile.rect.y))
        for enemy in enemies:
            screen.blit(enemy.image, (enemy.rect.x - camera_offset, enemy.rect.y))
        screen.blit(player.image, (player.rect.x - camera_offset, player.rect.y))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
