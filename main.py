import curses
import time

from engine import GameState, change_direction, move, new_game
from renderer import draw, draw_game_over, init_colors

KEY_DIRS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}


def compute_delay(state: GameState) -> float:
    return 0.1


def handle_input(state: GameState, key: int) -> GameState:
    if key in KEY_DIRS:
        return change_direction(state, KEY_DIRS[key])
    return state


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)
    init_colors()

    max_y, max_x = stdscr.getmaxyx()
    height = min(20, max_y - 3)
    width = min(40, max_x - 3)
    state = new_game(height=height, width=width)
    while state.alive:
        key = stdscr.getch()
        state = handle_input(state, key)
        state = move(state)
        draw(stdscr, state)
        time.sleep(compute_delay(state))

    draw_game_over(stdscr, state)
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)
