import pygame
pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
done = False
img = pygame.image.load("terrain.png")
SS = 30
mapp = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def get_adj(mapp, (cx, cy)):
    if mapp[cy][cx]:
        return sum([v for x, y, v in ((0, 1, 4), (0, -1, 1), (1, 0, 2), (-1, 0, 8)) if 0 <= y+cy < len(mapp) and 0 <= x+cx < len(mapp[0]) and mapp[y+cy][x+cx]])+1
    return 0

mapp = [[get_adj(mapp, (x, y)) for x, ele in enumerate(row)] for y, row in enumerate(mapp)]


def redraw(screen):
    screen.fill((0xFF, 0xFF, 0xFF))
    for y, row in enumerate(mapp):
        for x, ele in enumerate(row):
            screen.blit(img, (x*SS, y*SS), ((ele-1)*SS, 0, SS, SS))

clock = pygame.time.Clock()
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    redraw(screen)
    pygame.display.flip()
pygame.quit()
