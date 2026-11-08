def heuristic_1(self, game):
    score = 0

    # Convolves the individual board states
    player_conv = game.convolve_winstates(game.current_state[self.p])
    opponent_conv = game.convolve_winstates(game.current_state['X' if self.p == 'O' else 'O'])
    block_conv = game.convolve_winstates(game.current_state['B'])

    # Set score to +/- inf if one player has won
    for conv in player_conv:
        if game.s in conv:
            return float('inf')
    for conv in opponent_conv:
        if game.s in conv:
            return float('-inf')

    # Combines the convolved matricies to a usable state
    for i in range(len(player_conv)):
        for j in range(1, game.s):
            # Score: the number of unobstructed win conditions, weighted by 2^(length of the condition)
            # This feels like code golf and github copilot had a child, and it's ugly
            score += (np.count_nonzero(player_conv[i][player_conv[1][i]+block_conv[i] == 0] == j) -
                      np.count_nonzero(opponent_conv[i][player_conv[1][i]+block_conv[i] == 0] == j)) << (j << 1)
    return score
