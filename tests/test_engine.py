from dataclasses import replace

from engine import move, new_game


def test_snake_moves_forward():
    state = new_game(20, 40)
    new_state = move(state)
    assert new_state.snake[0] != state.snake[0]


def test_eating_food_grows_snake():
    state = new_game(20, 40)
    row, col = state.snake[0]
    dr, dc = state.direction
    state = replace(state, momo=(row + dr, col + dc))

    new_state = move(state)

    assert len(new_state.snake) == len(state.snake) + 1


def test_collision_with_wall_kills():
    state = new_game(5, 5)
    state = replace(state, snake=[(0, 2)], direction=(-1, 0))

    new_state = move(state)

    assert new_state.alive is False


def test_score_increases_on_eat():
    state = new_game(20, 40)
    row, col = state.snake[0]
    dr, dc = state.direction
    state = replace(state, momo=(row + dr, col + dc))

    new_state = move(state)

    assert new_state.score == state.score + 1
