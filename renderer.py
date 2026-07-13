import curses

from engine import GameState

BOARD_ROW_OFFSET = 2  # score line + top border
BOARD_COL_OFFSET = 1  # left border
BORDER_COLOR_PAIR = 1


def init_colors() -> None:
    if curses.has_colors():
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(BORDER_COLOR_PAIR, curses.COLOR_WHITE, -1)


def border_attr() -> int:
    if curses.has_colors():
        return curses.color_pair(BORDER_COLOR_PAIR) | curses.A_BOLD
    return curses.A_BOLD


def draw_border(stdscr, state: GameState) -> None:
    attr = border_attr()
    top = BOARD_ROW_OFFSET - 1
    bottom = BOARD_ROW_OFFSET + state.height
    left = BOARD_COL_OFFSET - 1
    right = BOARD_COL_OFFSET + state.width
    for col in range(left + 1, right):
        stdscr.addch(top, col, curses.ACS_HLINE, attr)
        stdscr.addch(bottom, col, curses.ACS_HLINE, attr)
    for row in range(top + 1, bottom):
        stdscr.addch(row, left, curses.ACS_VLINE, attr)
        stdscr.addch(row, right, curses.ACS_VLINE, attr)
    stdscr.addch(top, left, curses.ACS_ULCORNER, attr)
    stdscr.addch(top, right, curses.ACS_URCORNER, attr)
    stdscr.addch(bottom, left, curses.ACS_LLCORNER, attr)
    stdscr.addch(bottom, right, curses.ACS_LRCORNER, attr)


def draw(stdscr, state: GameState) -> None:
    stdscr.clear()
    draw_score(stdscr, state)
    draw_border(stdscr, state)
    for row, col in state.snake:
        stdscr.addch(row + BOARD_ROW_OFFSET, col + BOARD_COL_OFFSET, "O")
    food_row, food_col = state.momo
    stdscr.addch(food_row + BOARD_ROW_OFFSET, food_col + BOARD_COL_OFFSET, "*")
    stdscr.refresh()


# Assuming 'stdscr' is a curses window object and GameState is imported
# from engine import GameState

def draw_score(stdscr, state: GameState) -> None:
    """Draws the current score and a pause notification if the game is paused."""
    status = f"Score: {state.score}"
    
    if state.paused:
        status += "   PAUSED (p to resume)"
        
    stdscr.addstr(0, 0, status)


def draw_game_over(stdscr, state: GameState) -> None:
    stdscr.clear()
    draw_border(stdscr, state)
    message = f"Game Over! Score: {state.score}"
    row = state.height // 2 + BOARD_ROW_OFFSET
    col = max(state.width // 2 - len(message) // 2, 0) + BOARD_COL_OFFSET
    stdscr.addstr(row, col, message)
    stdscr.refresh()
