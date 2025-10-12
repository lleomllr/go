import random
from aigo.agent import Agent
from aigo.scoring import GameRes

MAX_SCORE = 999999
MIN_SCORE = -999999

def reverse_game_res(game_res):
    if game_res == GameRes.loss:
        return game_res.win
    if game_res == GameRes.win:
        return game_res.loss
    return GameRes.draw


def best_result(game_state, max_depth, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player():
            return MAX_SCORE
        else: 
            return MIN_SCORE
        
    if max_depth == 0:
        return eval_fn(game_state)
    
    best_one = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_res = best_result(
            next_state, max_depth - 1, eval_fn
        )
        own_res = -1 * opponent_best_res
        if own_res > best_one:
            best_one = own_res
    return best_one


class DepthPruned(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None 

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = best_result(next_state, self.max_depth, self.eval_fn)
            own_best_outcome = -1 * opponent_best_outcome

            if (not best_moves) or own_best_outcome >  best_score:
                best_moves = [possible_move]
                best_score = own_best_outcome
            elif own_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)