from poker import cards
from poker.simulation import simulator


def parse_cards(card_string):
    """
    Convert space-separated short card notation into internal card values.

    Example:
        "As Kh" -> [Ace of Spades, King of Hearts]
    """
    if not card_string.strip():
        return []

    return [
        cards.parse_card(card)
        for card in card_string.split()
    ]


def main():
    print("\nPoker_Sim Equity Calculator")
    print("---------------------------")

    hero_input = input("Hero hand (e.g. As Kh): ")
    board_input = input("Board (e.g. Qs 7d 2s, or leave blank): ")
    range_input = input("Opponent range (e.g. TT+, AQs+, AKo): ")
    trials_input = input("Number of trials [20000]: ")

    hero = parse_cards(hero_input)
    board = parse_cards(board_input)

    if trials_input.strip():
        num_trials = int(trials_input)
    else:
        num_trials = 20000

    wins, ties, losses = simulator.simulate_equity_vs_range(
        hero,
        range_input,
        known_board=board,
        num_trials=num_trials
    )

    results = simulator.calculate_equity_stats(
        wins,
        ties,
        losses
    )

    print("\nResults")
    print("-------")
    print(f"Win:    {results['win_rate']:.2%}")
    print(f"Tie:    {results['tie_rate']:.2%}")
    print(f"Loss:   {results['loss_rate']:.2%}")
    print(f"Equity: {results['equity']:.2%}")
    print(f"Trials: {wins + ties + losses:,}")


if __name__ == "__main__":
    main()