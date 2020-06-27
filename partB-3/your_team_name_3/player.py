import sys
import json
from math import inf
from your_team_name_3.search import *
import random

class ExamplePlayer:

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (White or Black). The value will be one of the
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        # load and analyse input
        stacks  = {(0, 0): 1, (1, 0): 1, (0, 1): 1, (1, 1): 1, (3, 0): 1, (4, 0): 1, (3, 1): 1, (4, 1): 1, (6, 0): 1, (7, 0): 1, (6, 1): 1, (7, 1): 1}
        targets = {(4, 7): 1, (6, 7): 1, (4, 6): 1, (6, 6): 1, (7, 6): 1, (7, 7): 1, (0, 7): 1, (0, 6): 1, (1, 6): 1, (3, 6): 1, (1, 7): 1, (3, 7): 1}
        target_groups = find_explosion_groups(targets.keys())

        # search for an action sequence
        self.colour = colour
        self.state = State(stacks, target_groups, targets)
        if colour == "black":
            self.state = self.state.reverse()
        print(self.state.heuristic())

    def scode3(self, state):
        N = sum(state.stacks.values()) # token number
        G = len(state.reverse().groups) # group number
        D = 0
        if N > 2:
            for s1 in state.stacks.keys():
                S = inf
                for s2 in state.stacks.keys():
                    if s1 != s2:
                        S = min(S,
                            min(pow(manhattan_distance(s1, s2) + 2, 2), 25)
                            )
                D = D + S
            D = D / N # average distance
        return N,G,D,N * 100 + G * 10 + D


    def score(self, state): # higher the better
        # state.print((self.scode3(state),self.scode3(state.reverse())))
        #state.print((state.heuristic(), state.reverse().heuristic(), len(state.reverse().groups), sum(state.targets.values())))
        return self.scode3(state)[3] - self.scode3(state.reverse())[3]
        # len(state.reverse().groups) - sum(state.targets.values())
        #return sum(state.stacks.values()) - sum(state.targets.values())
        #return -state.heuristic() - (-state.reverse().heuristic())

    def print_auction(self,action):
        if isinstance(action, Move):
            return ("MOVE", action.n, action.a, action.b)
        else:
            return ("BOOM", action.square)

    def terminal_state(self, state):
        return state.is_goal()




    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
        # "MOVE" n, a, b

        def minimax(self, node, depth, maximizingPlayer):
            if depth == 0 or self.terminal_state(node):
                return (None, self.score(node) * (1 if maximizingPlayer else -1))
            if maximizingPlayer:
                value = -10000
                final_action = None
                for (action, successor_state) in node.actions_successors():
                    successor_state = successor_state.reverse()
                    _, new_value = self.minimax(successor_state, depth - 1, False)
                    #print(str(self.print_auction(action)) + "|" + str(new_value) + "|" + str(self.colour))
                    if new_value > value or (random.randint(0, 1) == 0 and new_value == value):
                        value = new_value
                        final_action = action
                return (final_action, value)
            else:
                value = 10000
                final_action = None
                for (action, successor_state) in node.actions_successors():
                    successor_state = successor_state.reverse()
                    _, new_value = self.minimax(successor_state, depth - 1, True)
                    if new_value < value or (random.randint(0, 1) == 0 and new_value == value):
                        value = new_value
                        final_action = action
                return (final_action, value)

        action, score = self.minimax(self.state, 1, True)
        if isinstance(action, Move):
            return ("MOVE", action.n, action.a, action.b)
        else:
            return ("BOOM", action.square)


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        # print("-"*30)
        atype, *aargs = action
        if atype == "MOVE":
            n, a, b = aargs
            next_aution = Move(n, a, b)
        else:
            start_square, = aargs
            next_aution = Boom(start_square)
        if colour == self.colour:
            self.state = next_aution.apply_to(self.state)
        else:
            self.state = self.state.reverse()
            self.state = next_aution.apply_to(self.state)
            self.state = self.state.reverse()
