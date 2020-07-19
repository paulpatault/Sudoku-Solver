import random
import pygame


class Grid:
    FONT = pygame.font.SysFont("Comic Sans MS", 30)

    def __init__(self, screen, lvl=1):
        self.level = lvl
        self.screen = screen
        self.empty_cases = []
        self.array = self._generate_base()
        self._randomise()
        self._empty()

    def _generate_base(self):
        comp_grid = [
            [1, 2, 3, 7, 8, 9, 4, 5, 6],
            [4, 5, 6, 1, 2, 3, 7, 8, 9],
            [7, 8, 9, 4, 5, 6, 1, 2, 3],
            [2, 3, 1, 8, 9, 7, 5, 6, 4],
            [5, 6, 4, 2, 3, 1, 8, 9, 7],
            [8, 9, 7, 5, 6, 4, 2, 3, 1],
            [3, 1, 2, 9, 7, 8, 6, 4, 5],
            [6, 4, 5, 3, 1, 2, 9, 7, 8],
            [9, 7, 8, 6, 4, 5, 3, 1, 2],
        ]
        return comp_grid

    def _inverse_cols(self, i, j):
        for k in range(0, 9):
            self.array[k][i], self.array[k][j] = self.array[k][j], self.array[k][i]

    def _randomise(self):
        for i in range(0, 3):
            for j in range(0, 5):
                # lines
                l1 = random.randint(i * 3, i * 3 + 2)
                l2 = random.randint(i * 3, i * 3 + 2)
                self.array[l1], self.array[l2] = self.array[l2], self.array[l1]

        for i in range(0, 3):
            for j in range(0, 5):
                # cols
                c1 = random.randint(i * 3, i * 3 + 2)
                c2 = random.randint(i * 3, i * 3 + 2)
                self._inverse_cols(c1, c2)

    def _empty(self):
        for i in range(0, 9):
            for j in range(0, 9):
                if random.randint(0, self.level):
                    self.array[i][j] = "x"
                    self.empty_cases.append((i, j))

    def solve(self):
        def find():
            for i in range(0, 9):
                for j in range(0, 9):
                    if self.array[i][j] == "x":
                        return (i, j)
            return None

        def possible(x, y, n):
            for i in range(0, 9):
                if (self.array[x][i] == n and y != i) or (
                    self.array[i][y] == n and x != i
                ):
                    return False
            y0 = (x // 3) * 3
            x0 = (y // 3) * 3
            for i in range(0, 3):
                for j in range(0, 3):
                    if self.array[y0 + i][x0 + j] == n and (i, j) != (x, y):
                        return False
            return True

        next_ = find()

        if not next_:
            return True
        else:
            x, y = next_

        for n in range(1, 10):
            if possible(x, y, n):
                self.array[x][y] = n
                self.draw()
                pygame.time.delay(30)
                if self.solve():
                    return True
                self.array[x][y] = "x"
        return False

    def draw(self):
        def make_objects(i, j, n):
            SQUARE_SIZE = 42
            OFFSET = 1

            IPLUS = 0
            JPLUS = 0
            if i > 2:
                IPLUS = 2
            if i > 5:
                IPLUS = 4

            if j > 2:
                JPLUS = 2
            if j > 5:
                JPLUS = 4

            y = i * (SQUARE_SIZE + OFFSET) + IPLUS
            x = j * (SQUARE_SIZE + OFFSET) + JPLUS

            rect = pygame.Rect(x, y, SQUARE_SIZE, SQUARE_SIZE)
            color = (220, 220, 220)

            return (color, rect), (x + SQUARE_SIZE / 3, y)

        for i in range(0, 9):
            for j in range(0, 9):
                n = self.array[i][j]

                rect, textpos = make_objects(i, j, n)
                pygame.draw.rect(self.screen, *rect)

                if (i, j) in self.empty_cases:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)

                if n != "x":
                    num = self.FONT.render(str(n), True, color)
                    self.screen.blit(num, textpos)

        pygame.display.update()

    def __repr__(self):
        line = "-------------------------\n"

        res = ""
        for i in range(0, 9):
            if i % 3 == 0:
                res += line
            for j in range(0, 9):
                if j % 3 == 0:
                    res += "| "
                res += str(self.array[i][j])
                res += " "
            res += "|\n"
        res += line
        return res
