import enum 
import random 
from aigo.agent import Agent

class GameRes(enum.Enum):
    loss = 1
    draw = 2
    win = 3


def reverse_game_res(game_res):
    if game_res == GameRes.loss:
        return game_res.win
    if game_res == GameRes.win:
        return game_res.loss
    return GameRes.draw


def best_res(game_state):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return GameRes.win
        elif game_state.winner() is None:
            return GameRes.draw
        else:
            return GameRes.loss
        
    best_res = GameRes.loss
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_res = best_res(next_state)
        own_res = reverse_game_res(opponent_best_res)

        if own_res.value > best_res.value:
            best_res = own_res
    return best_res


class Minimax(Agent):
    def select_move(self, game_state):
        winning = []
        draw = []
        losing = []

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_res(next_state)
            own_best_outcome = reverse_game_res(opponent_best_outcome)

            if own_best_outcome == GameRes.win:
                winning.append(possible_move)
            elif own_best_outcome == GameRes.draw:
                draw.append(possible_move)
            else:
                losing.append(possible_move)
        if winning:
            return random.choice(winning)
        if draw:
            return random.choice(draw)
        return random.choice(losing)
