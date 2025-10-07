import random 
from aigo.agent.base import Agent 
from aigo.agent.helpers import is_eye
from aigo.goboard import Move
from aigo.gotypes import Point

__all__ = ['RandomBot']


class RandomBot(Agent):
    def select_move(self, game_state):
        cand = []
        for r in range(1, game_state.board.num_rows + 1):
            for c in range(1, game_state.board.num_cols + 1):
                p = Point(row=r, col=c)
                if game_state.is_valid_move(Move.play(p)) and not is_eye(game_state.board, p, game_state.next_player):
                    cand.append(p)
        if not cand: 
            return Move.pass_turn()
        return Move.play(random.choice(cand))
        

