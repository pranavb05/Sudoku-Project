import pygame
from sudoku_generator import SudokuGenerator

# Initialize Pygame
pygame.init()

# Screen dimensions and cell size
WIDTH, HEIGHT = 540, 540
cellsize = WIDTH // 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 69, 0)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")

font = pygame.font.Font(None, 36)

button_width, button_height = 100, 40
button1_pos = (75, 275)
button2_pos = (225, 275)
button3_pos = (375, 275)

# Initialize game variables
grid_values = [["" for _ in range(9)] for _ in range(9)]
solution_grid = None
selected_cell = None
scene = 1
difficulty = 0
sudoku_generator = None


def draw_button(text, pos, color):
    x, y = pos
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect


def draw_board():
    """Draws the Sudoku board grid and values."""
    for r in range(9):
        for c in range(9):
            x = c * cellsize
            y = r * cellsize
            rect = pygame.Rect(x, y, cellsize, cellsize)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Grid lines

            if selected_cell == (r, c):
                pygame.draw.rect(screen, (220, 220, 255), rect)

            # Display cell values
            text = font.render(str(grid_values[r][c]) if grid_values[r][c] != 0 else "", True, BLACK)
            text_rect = text.get_rect(center=(x + cellsize // 2, y + cellsize // 2))
            screen.blit(text, text_rect)


def get_cell(pos):
    """Returns the row and column of the clicked cell."""
    x, y = pos
    col = x // cellsize
    row = y // cellsize
    if 0 <= row < 9 and 0 <= col < 9:
        return (row, col)
    return None


def validate_solution():
    """Validates the current grid against Sudoku rules."""
    for row in range(9):
        for col in range(9):
            num = grid_values[row][col]
            if num == 0:
                return False  # Empty cell detected

            # Temporarily clear the cell to avoid false positives during validation
            grid_values[row][col] = 0

            # Check validity of the number in the row, column, and box
            if not (
                sudoku_generator.valid_in_row(row, num)
                and sudoku_generator.valid_in_col(col, num)
                and sudoku_generator.valid_in_box(row // 3 * 3, col // 3 * 3, num)
            ):
                return False  

            # Restore the cell value
            grid_values[row][col] = num

    return True


# Main loop
running = True
input_text = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if scene == 1:  # Menu scene
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button1.collidepoint(mouse_pos):
                    difficulty = 30
                    scene = 2
                elif button2.collidepoint(mouse_pos):
                    difficulty = 40
                    scene = 2
                elif button3.collidepoint(mouse_pos):
                    difficulty = 50
                    scene = 2

                # Generate Sudoku board
                if scene == 2:
                    sudoku_generator = SudokuGenerator(9, difficulty)
                    sudoku_generator.fill_values()
                    solution_grid = sudoku_generator.get_board()
                    sudoku_generator.remove_cells()
                    grid_values = sudoku_generator.get_board()

        elif scene == 2:  # Game scene
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                selected_cell = get_cell(event.pos)

            elif event.type == pygame.KEYDOWN and selected_cell is not None:
                row, col = selected_cell
                if event.key == pygame.K_RETURN:
                    try:
                        input_value = int(input_text)
                        grid_values[row][col] = input_value
                        input_text = ""

                        # Check if the game is complete
                        if all(all(cell != 0 for cell in row) for row in grid_values):
                            if validate_solution():
                                print("You win!")
                            else:
                                print("You lose!")
                    except ValueError:
                        pass
                else:
                    input_text += event.unicode

    if scene == 1:
        screen.fill(WHITE)
        button1 = draw_button("Easy", button1_pos, ORANGE)
        button2 = draw_button("Medium", button2_pos, ORANGE)
        button3 = draw_button("Hard", button3_pos, ORANGE)

    elif scene == 2:
        screen.fill(WHITE)
        draw_board()

        if selected_cell is not None:
            x, y = selected_cell[1] * cellsize, selected_cell[0] * cellsize
            text = font.render(input_text, True, BLACK)
            text_rect = text.get_rect(center=(x + cellsize // 2, y + cellsize // 2))
            screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
