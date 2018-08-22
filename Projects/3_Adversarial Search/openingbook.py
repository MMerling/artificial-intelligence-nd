
import random
import pickle
import time
from isolation import Isolation
from sample_players import MinimaxPlayer


NUM_ROUNDS = 100
DEPTH = 4

def build_table(num_rounds=NUM_ROUNDS):
    # You should run no more than `num_rounds` simulations -- the
    # goal of this quiz is to understand one possible way to develop
    # an opening book; not to develop a good one
    
    # NOTE: the GameState object is not hashable, and the python3
    #       runtime includes security features that make object
    #       hashes non-portable. There is a new attribute on
    #       GameState objects in this quiz called `hashable` that
    #       can be used as a dictionary key
    
    # TODO: return a table {k:v} where each k is a game state
    #       and each v is the best action to take in that state
    from collections import defaultdict, Counter
    book = defaultdict(Counter)
    for _ in range(num_rounds):
        #print(_)
        state = Isolation()
    #build_tree(state, book)
    #build_minimax_tree(state,book)
        build_alphabeta_tree(state,book)
    move = {k: max(v, key=v.get) for k, v in book.items()}
        #with open("data.pickle", 'wb') as f:
        #pickle.dump(move, f)
    return move


def build_tree(state, book, depth=DEPTH):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = random.choice(state.actions())
    reward = build_tree(state.result(action), book, depth - 1)
    state_str = "{:b}".format(state.board)
    hash = (state_str, state.locs, state.player())
    book[hash][action] += reward
    return -reward

def build_minimax_tree(state, book, depth=DEPTH):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = minimax(state, depth)
    reward = build_minimax_tree(state.result(action), book, depth - 1)
    state_str = "{:b}".format(state.board)
    hash = (state_str, state.locs, state.player())
    book[hash][action] += reward
    return -reward

def minimax(state, depth):
    
    def min_value(state, depth):
        if state.terminal_test(): return state.utility(state.player())
        if depth <= 0: return score(state)
        value = float("inf")
        for action in state.actions():
            value = min(value, max_value(state.result(action), depth - 1))
        return value
        
    def max_value(state, depth):
        if state.terminal_test(): return state.utility(state.player())
        if depth <= 0: return score(state)
        value = float("-inf")
        for action in state.actions():
            value = max(value, min_value(state.result(action), depth - 1))
        return value
        
    return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))

def build_alphabeta_tree(state, book, depth=DEPTH):
    if depth <= 0 or state.terminal_test():
        return -simulate(state)
    action = alpha_beta_search(state, depth)
    reward = build_alphabeta_tree(state.result(action), book, depth - 1)
    state_str = "{:b}".format(state.board)
    hash = (state_str, state.locs, state.player())
    book[hash][action] += reward
    return -reward

def alpha_beta_search(state, depth):
    def min_value(state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(state.player())
        if depth <= 0:
            return score(state)
        v = float("inf")
        for a in state.actions():
            v = min(v, max_value(state.result(a), alpha, beta, depth-1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(state, alpha, beta, depth):
        if state.terminal_test():
            return state.utility(state.player())
        if depth <= 0:
            return score(state)
        v = float("-inf")
        for a in state.actions():
            v = max(v, min_value(state.result(a), alpha, beta, depth-1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    alpha = float("-inf")
    beta = float("inf")
    best_score = float("-inf")
    best_move = state.actions()[0]
    for a in state.actions()[1:]:
        v = min_value(state.result(a), alpha, beta, depth-1)
        alpha = max(alpha, v)
        if v > best_score:
            best_score = v
            best_move = a
    return best_move

def score(state):
    own_loc = state.locs[state.player()]
    opp_loc = state.locs[1 - state.player()]
    own_liberties = state.liberties(own_loc)
    opp_liberties = state.liberties(opp_loc)
    return len(own_liberties) - len(opp_liberties)

def simulate(state):
    player_id = state.player()
    while not state.terminal_test():
        state = state.result(random.choice(state.actions()))
    return -1 if state.utility(player_id) < 0 else 1


open_book = build_table()
with open("data.pickle", 'wb') as f:
    pickle.dump(open_book, f)
