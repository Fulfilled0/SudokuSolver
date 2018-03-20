import pygame, sys
from pygame.locals import *
from Exact_Cover import *

class SudokuSolver():
    def __init__(self):
        """Initialize variables.

        """
        pygame.init()
        pygame.font.init()
        self.row_number_to_position = generate_sudoku_row_dicts(3)[0]
        self.position_to_row_number = generate_sudoku_row_dicts(3)[1]
        self.col_headers = generate_sudoku_col_headers(3)
        self.cover_matrix = generate_sudoku_matrix(3)

        self.game_matrix = Matrix(9, 9)
        for i in range(1, 10):
            for j in range(1, 10):
                self.game_matrix.set([0, (25+50*j, 25+50*i)], i, j)

        self.height = 600
        self.width = 550
        self.size = self.width, self.height
        self.white = 255, 255, 255
        self.black = 0, 0, 0
        self.gray = 150, 150, 150
        self.blue = 100, 100, 255
        self.surface = pygame.Surface(self.size)
        self.screen = pygame.display.set_mode(self.size)
        self.selection = None
        self.selection_rect = None
        self.text_font = pygame.font.SysFont("ComicSans MS", 30)
        self.solve_button = None
        self.attempted = False

    def main(self):
        """Main method to keep program running.

        """
        self.screen.fill(self.white)

        self.solve_button = Rect(200, 500, 150, 100)
        pygame.draw.rect(self.screen, self.blue, self.solve_button)
        text_surface = self.text_font.render("SOLVE", True, self.black)
        self.screen.blit(text_surface, (250, 550))

        for i in range(50, 650, 50):
            pygame.draw.line(self.screen, self.black, (i, 50), (i, 500), 1)
        for j in range(50, 550, 50):
            pygame.draw.line(self.screen, self.black, (50, j), (500, j), 1)

        for i in range(50, 650, 150):
            pygame.draw.line(self.screen, self.black, (i, 50), (i, 500), 2)
        for j in range(50, 550, 150):
            pygame.draw.line(self.screen, self.black, (50, j), (500, j), 2)

        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if not self.attempted:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.event_mouse(event)
                    elif event.type == pygame.KEYDOWN:
                        self.event_key(event)
                    if not self.attempted:
                        self.draw_digits()

    def event_mouse(self, event):
        """Determine what happens if mouse keys are pressed. Used to select squares and solve.

        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            row_num = None
            col_num = None
            # curr_square = Rect()
            curr_x = event.pos[0]
            curr_y = event.pos[1]

            if 200 < curr_x < 350 and 500 < curr_y < 600:
                self.solve()

            else:
                if 50 < curr_x < 100:
                    col_num = 1
                elif 100 < curr_x < 150:
                    col_num = 2
                elif 150 < curr_x < 200:
                    col_num = 3
                elif 200 < curr_x < 250:
                    col_num = 4
                elif 250 < curr_x < 300:
                    col_num = 5
                elif 300 < curr_x < 350:
                    col_num = 6
                elif 350 < curr_x < 400:
                    col_num = 7
                elif 400 < curr_x < 450:
                    col_num = 8
                elif 450 < curr_x < 500:
                    col_num = 9

                if 50 < curr_y < 100:
                    row_num = 1
                elif 100 < curr_y < 150:
                    row_num = 2
                elif 150 < curr_y < 200:
                    row_num = 3
                elif 200 < curr_y < 250:
                    row_num = 4
                elif 250 < curr_y < 300:
                    row_num = 5
                elif 300 < curr_y < 350:
                    row_num = 6
                elif 350 < curr_y < 400:
                    row_num = 7
                elif 400 < curr_y < 450:
                    row_num = 8
                elif 450 < curr_y < 500:
                    row_num = 9

                nearest_x = curr_x - (curr_x % 50) + 2
                nearest_y = curr_y - (curr_y % 50) + 2
                fill_in_square = Rect(nearest_x, nearest_y, 48, 48)
                if 50 < curr_x < 500 and 50 < curr_y < 500:
                    if self.selection == (row_num, col_num):
                        self.selection = None
                        self.selection_rect = None
                    else:
                        self.selection = (row_num, col_num)
                        self.selection_rect = fill_in_square



    def event_key(self, event):
        """Determine what happens when keyboard keys are pressed. Used to enter digits into grid.

        """
        if event.type == pygame.KEYDOWN:
            if event.unicode.isdigit:
                if self.selection:
                    self.game_matrix.get(self.selection[0], self.selection[1])[0] = int(event.unicode)

    def solve(self):
        """Solve the current Sudoku puzzle.

        """
        solutions = []
        for i in range(1, 10):
            for j in range(1, 10):
                entry = self.game_matrix.get(i, j)
                if entry[0] != 0:
                    pos = ""
                    pos += "#" + str(entry[0])
                    pos += "R" + str(i)
                    pos += "C" + str(j)
                    row_num = self.position_to_row_number[pos]
                    solutions.append(row_num)
                    self.cover_matrix.row_headers[row_num].C.cover()
                    self.cover_matrix.row_headers[row_num].cover_row()

        found = search(0, self.cover_matrix, solutions)
        self.attempted = True

        if found:
            for sol in solutions:
                sol_pos = self.row_number_to_position[sol]
                sol_num = int(sol_pos[1])
                row_num = int(sol_pos[3])
                col_num = int(sol_pos[5])
                self.game_matrix.get(row_num, col_num)[0] = sol_num

            self.selection = None
            self.selection_rect = None
            self.draw_digits()

        else:
            self.screen.fill(self.white)
            text_surface = self.text_font.render("NO SOLUTIONS FOUND", True, self.black)
            self.screen.blit(text_surface, (150, 300))
            pygame.display.flip()

    def draw_digits(self):
        """Used to show the digits in the grid.

        """
        for i in range(1, 10):
            for j in range(1, 10):
                entry = self.game_matrix.get(i, j)
                curr_rect = Rect(entry[1][0] - 23, entry[1][1] - 23, 48, 48)
                pygame.draw.rect(self.screen, self.white, curr_rect)
                if self.selection_rect:
                    pygame.draw.rect(self.screen, self.gray, self.selection_rect)

        for i in range(1, 10):
            for j in range(1, 10):
                entry = self.game_matrix.get(i, j)
                if entry[0] != 0:
                    text_surface = self.text_font.render(str(entry[0]), True, self.black)
                    self.screen.blit(text_surface, entry[1])
        pygame.display.flip()

if __name__ == "__main__":
    App = SudokuSolver()
    App.main()