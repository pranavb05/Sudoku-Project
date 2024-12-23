import pygame
from sudoku_generator import SudokuGenerator

# Initialize Pygame
pygame.init()

# Screen dimensions and cell size
WIDTH, HEIGHT = 540, 600  # Extra height for buttons
cellsize = WIDTH // 9

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 69, 0)
LIGHT_BLUE = (220, 220, 255)
GRAY = (200, 200, 200)
BUTTON_BG = (205, 133, 63)  # Brown background
BUTTON_TEXT = WHITE  # White text

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, 36)
button_width, button_height = 125, 40
button1_pos = (75, 275)
button2_pos = (225, 275)
button3_pos = (375, 275)
reset_button_pos = (75, 550)
restart_button_pos = (225, 550)
exit_button_pos = (375, 550)

# Initialize game variables
grid_values = [["" for _ in range(9)] for _ in range(9)]
sketched_values = [["" for _ in range(9)] for _ in range(9)]
solution_grid = None
selected_cell = None
scene = 1
difficulty = 0
sudoku_generator = None


def draw_button(text, pos, color):
    global button_width
    x, y = pos
    button_rect = pygame.Rect(x, y, button_width, button_height)
    pygame.draw.rect(screen, color, button_rect)
    text_surface = font.render(text, True, BUTTON_TEXT)
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
                pygame.draw.rect(screen, LIGHT_BLUE, rect)

            # Display confirmed values in black
            if grid_values[r][c] != 0:
                text = font.render(str(grid_values[r][c]), True, BLACK)
                text_rect = text.get_rect(center=(x + cellsize // 2, y + cellsize // 2))
                screen.blit(text, text_rect)
            # Display sketched values in gray
            elif sketched_values[r][c] != "":
                text = font.render(str(sketched_values[r][c]), True, GRAY)
                text_rect = text.get_rect(center=(x + cellsize // 2, y + cellsize // 2))
                screen.blit(text, text_rect)


def get_cell(pos):
    """Returns the row and column of the clicked cell."""
    x, y = pos
    col = x // cellsize
    row = y // cellsize
    if 0 <= row < 9 and 0 <= col < 9:
        return row, col
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


def reset_board():
    global grid_values, sketched_values
    if sudoku_generator:
        grid_values = [row[:] for row in original_board]  # Reset to original board
    sketched_values = [["" for _ in range(9)] for _ in range(9)]  # Clear sketched values



def display_result(result):
    screen.fill(WHITE)
    result_text = "You Win!" if result else "You Lose!"
    text_surface = font.render(result_text, True, BLACK)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text_surface, text_rect)

    restart_button = draw_button("Restart", restart_button_pos, ORANGE)
    exit_button = draw_button("Exit", exit_button_pos, ORANGE)
    pygame.display.flip()

    return restart_button, exit_button


def move_selection(direction):
    """Moves the selected cell based on the arrow key input."""
    global selected_cell
    if selected_cell is None:
        selected_cell = (0, 0)
    row, col = selected_cell
    if direction == "UP" and row > 0:
        row -= 1
    elif direction == "DOWN" and row < 8:
        row += 1
    elif direction == "LEFT" and col > 0:
        col -= 1
    elif direction == "RIGHT" and col < 8:
        col += 1
    selected_cell = (row, col)


running = True
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
                    original_board = [row[:] for row in sudoku_generator.get_board()]
                    grid_values = sudoku_generator.get_board()

        elif scene == 2:  # Game scene
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                selected_cell = get_cell(mouse_pos)
                if reset_button.collidepoint(mouse_pos):
                    reset_board()
                elif restart_button.collidepoint(mouse_pos):
                    scene = 1  # Back to the start screen
                    grid_values = [["" for _ in range(9)] for _ in range(9)]
                    sketched_values = [["" for _ in range(9)] for _ in range(9)]  # Clear sketched values
                    selected_cell = None
                elif exit_button.collidepoint(mouse_pos):
                    running = False
                else:
                    selected_cell = get_cell(event.pos)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_selection("UP")
                elif event.key == pygame.K_DOWN:
                    move_selection("DOWN")
                elif event.key == pygame.K_LEFT:
                    move_selection("LEFT")
                elif event.key == pygame.K_RIGHT:
                    move_selection("RIGHT")
                elif selected_cell is not None:  # Ensure a cell is selected
                    row, col = selected_cell
                    if event.key == pygame.K_RETURN:
                        # Commit the sketched value to the grid
                        try:
                            input_value = int(sketched_values[row][col])
                            if 1 <= input_value <= 9 and grid_values[row][col] == 0:
                                grid_values[row][col] = input_value
                                sketched_values[row][col] = ""

                            input_text = ""
                            # Check if the game is complete
                            if all(all(cell != 0 for cell in row) for row in grid_values):
                                if validate_solution():
                                    scene = 3  # Win scene
                                    result = True
                                else:
                                    scene = 3  # Lose scene
                                    result = False
                            # Clear the sketch
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        sketched_values[row][col] = ""  # Clear sketch in the cell
                    else:
                        try:
                            # Sketch the value in gray if the cell is empty
                            input_value = int(event.unicode)
                            if 1 <= input_value <= 9 and grid_values[row][col] == 0:
                                sketched_values[row][col] = input_value
                        except ValueError:
                            pass

        elif scene == 3:  # Result scene
            restart_button, exit_button = display_result(result)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    scene = 1
                    grid_values = [["" for _ in range(9)] for _ in range(9)]
                    sketched_values = [["" for _ in range(9)] for _ in range(9)]
                    selected_cell = None
                elif exit_button.collidepoint(event.pos):
                    running = False

    if scene == 1:
        screen.fill(WHITE)
        button1 = draw_button("Easy", button1_pos, ORANGE)
        button2 = draw_button("Medium", button2_pos, ORANGE)
        button3 = draw_button("Hard", button3_pos, ORANGE)
    elif scene == 2:
        screen.fill(WHITE)
        draw_board()
        # Draw Reset, Restart, and Exit buttons
        reset_button = draw_button("RESET", reset_button_pos, ORANGE)
        restart_button = draw_button("RESTART", restart_button_pos, ORANGE)
        exit_button = draw_button("EXIT", exit_button_pos, ORANGE)

    pygame.display.flip()

pygame.quit()
