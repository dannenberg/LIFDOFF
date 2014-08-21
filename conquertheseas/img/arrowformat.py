import pygame
SQUARE_SIZE = 30
src = ""
std = pygame.image.load(src+"arrow.png")
look = [pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA) for _ in xrange(3)]
for i in xrange(3):
    look[i].blit(std, (0, 0), ((SQUARE_SIZE*i, 0), (SQUARE_SIZE, SQUARE_SIZE)))
surf = pygame.Surface((SQUARE_SIZE*13, SQUARE_SIZE), pygame.SRCALPHA)
# 123456789012
# ^>^v^> <^> v
#   > vv  << <
s = {
    0: False,
    1: (2, 0),
    2: (2, 270),
    3: (1, 0),
    4: (2, 180),
    5: (0, 0),
    6: (1, 270),
    7: False,
    8: (2, 90),
    9: (1, 90),
    10: (0, 270),
    11: False,
    12: (1, 180),
}
for x in xrange(13):
    if s[x]:
        surf.blit(pygame.transform.rotate(look[s[x][0]], s[x][1]), (SQUARE_SIZE*x, 0))
pygame.image.save(surf, src+"arrow_formatted.png")
