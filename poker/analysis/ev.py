def ev_of_call(wins, ties, losses, pot_before, cost_to_call, tie_split=2):
    """
    Expected value of calling, given win/tie/loss counts (from
    simulate_equity or enumerate_exact) and the pot economics.

    Assumes ties split the pot tie_split-ways. This is EXACT when there's
    exactly one opponent (a tie is always a clean 2-way split), but an
    APPROXIMATION with 2+ opponents, since a real tie could be shared
    among more than 2 players and this doesn't currently distinguish that.
    """
    n = wins + ties + losses
    equity_share = # your code here -- P(win) + P(tie)/tie_split
    final_pot = pot_before + cost_to_call
    return # your code here -- the formula above


