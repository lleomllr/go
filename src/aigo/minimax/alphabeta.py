import random
from aigo.agent import Agent
from aigo.gotypes import Player

MAX_SCORE = 999999
MIN_SCORE = -999999

def alphabeta_res(game_state, max_depth, best_b, best_w, eval_fn):
    if game_state.is_over():
        if game_state.winner() == game_state.next_player:
            return MAX_SCORE
        else:
            return MIN_SCORE
        
    if max_depth == 0:
        return eval_fn(game_state)
    
    best = MIN_SCORE
    for candidate_move in game_state.legal_moves():
        next_state = game_state.apply_move(candidate_move)
        opponent_best_res = alphabeta_res(
            next_state, max_depth - 1, best_b, best_w, eval_fn
        )
        own_res = -1 * opponent_best_res

        if own_res > opponent_best_res:
            best = own_res

        if game_state.next_player == Player.white:
            if best > best_w:
                best_w = best 
            outcome_black = -1 * best
            if outcome_black < best_b:
                return best
            
        elif game_state.next_state == Player.black: 
            if best > best_b:
                best_b = best
            outcome_white = -1 * best
            if outcome_black < best_w:
                return best
            
    return best


class AlphaBeta(Agent):
    def __init__(self, max_depth, eval_fn):
        Agent.__init__(self)
        self.max_depth = max_depth
        self.eval_fn = eval_fn

    def select_move(self, game_state):
        best_moves = []
        best_score = None 
        best_b = MIN_SCORE
        best_w = MIN_SCORE

        for possible_move in game_state.legal_moves():
            next_state = game_state.apply_move(possible_move)
            opponent_best_outcome = alphabeta_res(
                next_state, self.max_depth, best_b, best_w, self.eval_fn
            )
            own_best_outcome = -1 * opponent_best_outcome
            if (not best_moves) or own_best_outcome > best_score:
                best_moves = [possible_move]
                best_score = own_best_outcome

                if game_state.next_player == Player.black:
                    best_b = best_score
                elif game_state.next_player == Player.white:
                    best_w = best_score
            elif own_best_outcome == best_score:
                best_moves.append(possible_move)
        return random.choice(best_moves)