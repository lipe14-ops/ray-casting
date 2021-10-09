import pygame
import math
from dataclasses import dataclass

pygame.init()
SCREEN = pygame.display.set_mode()
pygame.display.set_caption('Raycasting')
pygame.mouse.set_visible(False)
CLOCK = pygame.time.Clock()

SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()
MAP_SIZE = 9
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
STEP_ANGLE = FOV / CASTED_RAYS
SCALE = SCREEN_WIDTH / CASTED_RAYS

MAP = (
    '#########'
    '#       #'
    '### #####'
    '#       #'
    '# ##  # #'
    '# #   # #'
    '# ##### #'
    '#     # #'
    '#########'
)


@dataclass
class Player:
    x: float
    y: float
    speed: int = 5
    angle: float = math.pi


player = Player(500, 400)


def cast_rays(player: Player):
    start_angle = player.angle - HALF_FOV
    CLOCK.tick(60)
    
    SCREEN.fill((0, 0, 0))

    pygame.draw.rect(SCREEN, (173, 216, 230), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2))
    pygame.draw.rect(SCREEN, (0, 64, 0), [0, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT / 2])


    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            target_x = (player.x / 2) - math.sin(start_angle) * depth
            target_y = (player.y / 2) + math.cos(start_angle) * depth

            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)
            
            square = row * MAP_SIZE + col

            if MAP[square] == '#':
                color = 255 / (1 + depth * depth * 0.0001)
                depth *= math.cos(player.angle - start_angle)
                wall_height = 21000 / (depth + 0.0001)
                
                if wall_height > SCREEN_HEIGHT: 
                    wall_height = SCREEN_HEIGHT 
                
                pygame.draw.rect(SCREEN, (color, color // 3, color / 2), [ray * SCALE, (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE + 1, wall_height])
                
                break

        start_angle += STEP_ANGLE
    pygame.display.update()


def main() -> None:
    forward = True
    is_running = True
    
    while is_running:

        CLOCK.tick(30)
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        
        col = int((player.x / 2) / TILE_SIZE)
        row = int((player.y / 2) / TILE_SIZE)
            
        square = row * MAP_SIZE + col

        cast_rays(player)

        if MAP[square] == '#':
            if forward:
                player.x -= -math.sin(player.angle) * 5
                player.y -= math.cos(player.angle) * 5
            else:
                player.x += -math.sin(player.angle) * 5
                player.y += math.cos(player.angle) * 5
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            player.angle -= 0.1
        
        if keys[pygame.K_RIGHT]:
            player.angle += 0.1
        
        if keys[pygame.K_UP]:
            forward = True
            player.x += -math.sin(player.angle) * player.speed
            player.y += math.cos(player.angle) * player.speed
        
        if keys[pygame.K_DOWN]:
            forward = False
            player.x -= -math.sin(player.angle) * player.speed
            player.y -= math.cos(player.angle) * player.speed

    pygame.quit()


if __name__ == '__main__':
    main()
