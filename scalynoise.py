#!/usr/bin/env python3

import random
from PIL import Image

SEED = None  # Set to a number to make it reproducible!
W = 400
H = 400
SCALE_LEFT = H ** 0.8
SCALE_RIGHT = H ** 0.5


class GridRandom:
    def __init__(self, seed=None):
        self.seed = seed or random.getrandbits(64)
        print('Using seed {}'.format(self.seed))

    def make_random_at(self, x, y):
        x = int(x)
        y = int(y)
        cell_seed = '{}|{}${}'.format(x, y, self.seed)
        return random.Random(cell_seed)


def map_back(x, y):
    # This is the secret sauce of this program:
    # The mapping of image (x,y) to grid (x,y).
    # Figure it out yourself.
    D = W * SCALE_RIGHT / (SCALE_LEFT - SCALE_RIGHT)
    C = SCALE_LEFT * D
    scale = C / (x + D)
    return (x / scale, (y - H / 2) / scale + H / 2)


def make_scalynoise():
    grid_random = GridRandom(SEED)
    data = []
    for y in range(H):
        for x in range(W):
            ox, oy = map_back(x, y)
            rng = grid_random.make_random_at(ox, oy)
            # COuld cache (ox,oy)→RGB mapping, but whatever
            data.append((rng.randint(0, 255), rng.randint(0, 255), rng.randint(0, 255)))
    img = Image.new('RGB', (W, H))
    img.putdata(data)
    return img


def run(filename):
    img = make_scalynoise()
    img.save(filename)
    print('Written to {}'.format(filename))


if __name__ == '__main__':
    import time
    run('output_{}.png'.format(int(time.time())))
