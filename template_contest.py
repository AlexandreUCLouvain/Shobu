from agent import Agent
import random

class AI(Agent):
    def __init__(self, player, game):
        super().__init__(player, game)
        self.depth_limit = 2

    def play(self, state, remaining_time):
        if remaining_time < 10 :
            return self.game.actions(state)[0]

        alpha = float("-inf")
        beta = float("inf")
        best_action = None
        best_value = float("-inf")

        for action in self.game.actions(state):
            value = self.alpha_beta_search(self.game.result(state, action), self.depth_limit - 1, alpha, beta, False)
            if value > best_value:
                best_value = value
                best_action = action
            alpha = max(alpha, value)

        simulations = 700
        best_action = self.mcts(state, best_action, simulations)

        return best_action

    def alpha_beta_search(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game.is_terminal(state):
            return self.evaluate(state)

        if maximizing_player:
            value = float("-inf")
            for action in self.game.actions(state):
                value = max(value, self.alpha_beta_search(self.game.result(state, action), depth - 1, alpha, beta, False))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = float("inf")
            for action in self.game.actions(state):
                value = min(value, self.alpha_beta_search(self.game.result(state, action), depth - 1, alpha, beta, True))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value

    def mcts(self, state, best_action_from_ab, simulations):
        best_action = best_action_from_ab
        best_score = 0

        for _ in range(simulations):
            score = self.simulate_random_playout(state, best_action)
            if score > best_score:
                best_score = score
                best_action = best_action_from_ab
  
        return best_action

    def simulate_random_playout(self, state, action):
        current_state = self.game.result(state, action)
        while not self.game.is_terminal(current_state):
            possible_actions = self.game.actions(current_state)
            action = random.choice(possible_actions)
            current_state = self.game.result(current_state, action)
        return self.game.utility(current_state, self.player)

    def evaluate(self, state):
        sum = 0
        for board in state.board:
            if len(board[self.player]) == 4:
                sum-=0
            if len(board[self.player]) == 3:
                sum-=1
            if len(board[self.player]) == 2:
                sum-=3
            if len(board[self.player]) == 1:
                sum-=7
            if len(board[self.player]) == 0:
                sum-=float("inf")
            if len(board[1-self.player]) == 4:
                sum+=0
            if len(board[1-self.player]) == 3:
                sum+=1
            if len(board[1-self.player]) == 2:
                sum+=3
            if len(board[1-self.player]) == 1:
                sum+=7
            if len(board[1-self.player]) == 0:
                sum+=float("inf")

            sum -= state.count_boring_actions*6
        
        return sum