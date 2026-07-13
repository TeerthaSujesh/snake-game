import curses
import time

# Added toggle_pause to the import list
from engine import GameState, change_direction, move, new_game, toggle_pause
from renderer import draw, draw_game_over, init_colors

KEY_DIRS = {
    curses.KEY_UP: (-1, 0),
    curses.KEY_DOWN: (1, 0),
    curses.KEY_LEFT: (0, -1),
    curses.KEY_RIGHT: (0, 1),
}
BASE_DELAY = 0.1
SPEEDUP_PER_LEVEL = 0.01
MIN_DELAY = 0.05
POINTS_PER_LEVEL = 5

def compute_delay(state: GameState) -> float:
    level = state.score // POINTS_PER_LEVEL
    return max(BASE_DELAY - level * SPEEDUP_PER_LEVEL, MIN_DELAY)


def handle_input(state: GameState, key: int) -> GameState:
    # 1. Check for pause key first (independent of arrow keys)
    if key == ord("p") or key == ord("P"):
        return toggle_pause(state)
    
    # 2. Check for movement keys
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
    
    # Initialize state once
    state = new_game(height=height, width=width)

    # Indented the main loop so it lives inside the main() function
    while state.alive:
        key = stdscr.getch()
        state = handle_input(state, key)
        
        if not state.paused:
            state = move(state)
            
        draw(stdscr, state)
        time.sleep(compute_delay(state))

    # Trigger game over behavior when loop finishes
    draw_game_over(stdscr, state)
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    curses.wrapper(main)