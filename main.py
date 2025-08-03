from helper_files import import_rounds
from helper_math import calc_handicap_index
from helper_rounds import filter_and_sort_rounds, combine_rounds, output_results


def main():
    filename = "round_history_3.csv"
    player = "Dominick D'Emilio"

    # Import round data
    headers, rounds = import_rounds(filename)

    # Filter rounds by player, number of completed holes, scoring format
    # Sort by most recent rounds
    rounds = filter_and_sort_rounds(rounds, player)

    # Compile list of 20 or less "complete" rounds (combining 9 hole rounds)
    # Sort by latest rounds
    rounds = combine_rounds(rounds)

    # Calculate handicap index
    handicap_index = calc_handicap_index(rounds)

    # Output
    output_results(player, rounds, handicap_index)


if __name__ == "__main__":
    main()
