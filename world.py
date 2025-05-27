from perlin_noise import PerlinNoise
from block import draw_block, get_block_type
from constants import WORLD_SIZE, BLOCK_SCALE

def generate_world():
    """Генерация мира с использованием шума Перлина."""
    noise = PerlinNoise(octaves=2, seed=42)
    world = {}
    scale = 0.1
    for x in range(WORLD_SIZE):
        for z in range(WORLD_SIZE):
            height = int(noise([x * scale, z * scale]) * 5 + 5)
            for y in range(height):
                block_type = get_block_type(y, height)
                world[(x, y, z)] = block_type
    return world

def render_world(world):
    """Рендеринг всех блоков мира."""
    for (x, y, z), block_type in world.items():
        draw_block(x, y, z, block_type)