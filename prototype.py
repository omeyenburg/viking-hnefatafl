import pygame, numpy

pygame.init()
mult = 30
size = 11 * mult, 11 * mult
window = pygame.display.set_mode(size)

BP = 1
WP = 2
KING = 3

board = numpy.zeros((11, 11))

board[5, 5] = KING

board[3, 0] = BP
board[4, 0] = BP
board[5, 0] = BP
board[6, 0] = BP
board[7, 0] = BP
board[5, 1] = BP

board[0, 3] = BP
board[0, 4] = BP
board[0, 5] = BP
board[0, 6] = BP
board[0, 7] = BP
board[1, 5] = BP

board[10, 3] = BP
board[10, 4] = BP
board[10, 5] = BP
board[10, 6] = BP
board[10, 7] = BP
board[9, 5] = BP

board[3, 10] = BP
board[4, 10] = BP
board[5, 10] = BP
board[6, 10] = BP
board[7, 10] = BP
board[5, 9] = BP

board[5, 4] = WP
board[5, 3] = WP
board[5, 6] = WP
board[5, 7] = WP
board[4, 5] = WP
board[3, 5] = WP
board[6, 5] = WP
board[7, 5] = WP
board[4, 4] = WP
board[4, 6] = WP
board[6, 6] = WP
board[6, 4] = WP

move = 1
sel = None
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos[0] // mult, event.pos[1] // mult

            if move == 0 and board[pos] == 1 or move == 1 and board[pos] in (2, 3):
                sel = pos
            elif sel is not None:
                dest = pos
                if (
                    (not dest == sel)
                    and sel[0] == dest[0]
                    or sel[1] == dest[1]
                    and board[dest] == 0
                ):
                    v = board[sel] == KING or dest not in (
                        (0, 0),
                        (10, 0),
                        (0, 10),
                        (10, 10),
                        (5, 5),
                    )
                    if move:
                        p1 = [2, 3]
                        p2 = [1]
                    else:
                        p1 = [1]
                        p2 = [2, 3]

                    def enemy(c, p):
                        return (
                            c in ((0, 0), (10, 0), (0, 10), (10, 10), (5, 5))
                            or board[c] in p
                        )

                    if sel[0] == dest[0]:
                        for y in range(min(sel[1], dest[1]) + 1, max(sel[1], dest[1])):
                            if board[sel[0], y] != 0:
                                v = 0
                                break

                        if 0 < dest[0] < 10:
                            if enemy((dest[0] + 1, dest[1]), p2) and enemy(
                                (dest[0] - 1, dest[1]), p2
                            ):
                                v = 0
                    else:
                        for y in range(min(sel[0], dest[0]) + 1, max(sel[0], dest[0])):
                            if board[y, sel[1]] != 0:
                                v = 0
                                break
                        if 0 < dest[1] < 10:
                            if enemy((dest[0], dest[1] + 1), p2) and enemy(
                                (dest[0], dest[1] - 1), p2
                            ):
                                v = 0
                    if v:
                        board[dest] = board[sel]
                        board[sel] = 0
                        sel = None

                        if (
                            dest[0] < 9
                            and board[dest[0] + 1, dest[1]] in p2
                            and enemy((dest[0] + 2, dest[1]), p1)
                        ):
                            board[dest[0] + 1, dest[1]] = 0
                        if (
                            dest[0] > 1
                            and board[dest[0] - 1, dest[1]] in p2
                            and enemy((dest[0] - 2, dest[1]), p1)
                        ):
                            board[dest[0] - 1, dest[1]] = 0
                        if (
                            dest[1] < 9
                            and board[dest[0], dest[1] + 1] in p2
                            and enemy((dest[0], dest[1] + 2), p1)
                        ):
                            board[dest[0], dest[1] + 1] = 0
                        if (
                            dest[1] > 1
                            and board[dest[0], dest[1] - 1] in p2
                            and enemy((dest[0], dest[1] - 2), p1)
                        ):
                            board[dest[0], dest[1] - 1] = 0
                        move = not move
                    else:
                        pygame.draw.rect(
                            window,
                            (200, 50, 0),
                            (dest[0] * mult, dest[1] * mult, mult, mult),
                        )
    window.fill((0, 0, 0))
    for x, y in numpy.ndindex(board.shape):

        c = [(x + y) % 2 * 70 + 100] * 3
        if (x, y) == sel:
            c = 100, 200, 50
        pygame.draw.rect(
            window, c, (x * mult, y * mult, x * mult + mult, y * mult + mult), 0
        )
        if (x, y) in ((0, 0), (10, 0), (0, 10), (10, 10), (5, 5)):
            c = [(x + y + 1) % 2 * 70 + 100] * 3
            pygame.draw.line(
                window, c, (x * mult, y * mult), (x * mult + mult, y * mult + mult), 3
            )
            pygame.draw.line(
                window, c, (x * mult, y * mult + mult), (x * mult + mult, y * mult), 3
            )

        if board[x, y] in (1, 2):
            c = [(board[x, y] - 1) * 160 + 60] * 3
            pygame.draw.rect(
                window, c, (x * mult + 3, y * mult + 3, mult - 6, mult - 6), 0
            )
        elif board[x, y] == 3:
            pygame.draw.polygon(
                window,
                (220, 220, 220),
                (
                    (x * mult + mult // 2, y * mult + 3),
                    (x * mult + 3, y * mult + mult - 3),
                    (x * mult + mult - 3, y * mult + mult - 3),
                ),
            )
            pygame.draw.lines(
                window,
                (70, 70, 70),
                True,
                (
                    (x * mult + mult // 2, y * mult + 3),
                    (x * mult + 3, y * mult + mult - 3),
                    (x * mult + mult - 3, y * mult + mult - 3),
                ),
            )

    pygame.display.flip()
    clock.tick(20)
