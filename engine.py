import random
from dataclasses import dataclass, replace


@dataclass
class GameState:
    snake: list[tuple[int, int]]   # list of (row, col), head is index 0
    direction: tuple[int, int]     # (row_delta, col_delta)
    momo: tuple[int, int]
    score: int
    alive: bool
    height: int
    width: int


def new_game(height: int, width: int) -> GameState:
    mid_row = height // 2
    mid_col = width // 2
    snake = [(mid_row, mid_col), (mid_row, mid_col - 1), (mid_row, mid_col - 2)]
    state = GameState(
        snake=snake,
        direction=(0, 1),
        momo=(0, 0),
        score=0,
        alive=True,
        height=height,
        width=width,
    )
    return replace(state, momo=spawn_food(state))


def did_eat(state: GameState) -> bool:
    return state.snake[0] == state.momo


def is_collision(state: GameState) -> bool:
    row, col = state.snake[0]
    if not (0 <= row < state.height and 0 <= col < state.width):
        return True
    return state.snake[0] in state.snake[1:]


def spawn_food(state: GameState) -> tuple[int, int]:
    occupied = set(state.snake)
    free_cells = [
        (r, c)
        for r in range(state.height)
        for c in range(state.width)
        if (r, c) not in occupied
    ]
    return random.choice(free_cells)


def change_direction(state: GameState, new_dir: tuple[int, int]) -> GameState:
    dr, dc = state.direction
    ndr, ndc = new_dir
    if (ndr, ndc) == (-dr, -dc) and len(state.snake) > 1:
        return state
    return replace(state, direction=new_dir)


def move(state: GameState) -> GameState:
    dr, dc = state.direction
    row, col = state.snake[0]
    new_head = (row + dr, col + dc)

    moved_snake = [new_head] + state.snake[:-1]
    ate = did_eat(replace(state, snake=moved_snake))
    new_snake = [new_head] + state.snake if ate else moved_snake
    new_score = state.score + 1 if ate else state.score

    candidate = replace(state, snake=new_snake, score=new_score)

    if is_collision(candidate):
        return replace(candidate, alive=False)

    if ate:
        candidate = replace(candidate, momo=spawn_food(candidate))

    return candidate
