import csv
from models.round import Round
from models.combined_round import CombinedRound


def import_rounds(filename):
    headers = []
    rounds = []

    with open(filename) as f:
        csv_reader = csv.reader(f)

        # First row is headers
        headers = next(csv_reader)

        # Retrieve rounds
        for row in csv_reader:
            player = row[0].replace("’", "'")
            date = row[1]
            time = row[2]
            course = row[3]
            rating = row[6]
            slope = row[7]
            scoring_format = row[9]
            completed_holes = row[10]
            gross_score = row[11]
            gross_score_over_par = row[12]

            round = Round(
                player,
                date,
                time,
                course,
                rating,
                slope,
                scoring_format,
                completed_holes,
                gross_score,
                gross_score,
            )
            rounds.append(round)

    return headers, rounds


def filter_and_sort_rounds(rounds, player):
    # Filters rounds by player, 9 and 18 hole rounds (must be complete), stroke play, and contains necessary statistics to calculate handicap
    # Sorts rounds by most recent date
    filtered_rounds = []

    # Filter rounds
    filtered_rounds = [
        round
        for round in rounds
        if round.player == player
        and round.completed_holes in (9, 18)
        and round.scoring_format == "Stroke Play"
        and all(
            val is not None
            for val in (
                round.rating,
                round.slope,
                round.gross_score,
                round.gross_score_over_par,
            )
        )
    ]

    # Sort rounds by most recent date
    filtered_rounds.sort(key=lambda x: x.date, reverse=True)

    return filtered_rounds


def combine_rounds(rounds):
    # Combines all rounds into full rounds (18 hole rounds remain the same, 9 hole rounds form 18 hole rounds)
    # Takes the most recent 20 rounds
    # Sorts in chronological order
    combined_rounds = []
    placeholder = None

    for round in rounds:
        # Full round
        if round.completed_holes == 18:
            # Add round to combined_rounds
            combined_round = CombinedRound(
                round.date,
                round.course,
                round.rating,
                round.slope,
                round.gross_score,
            )
            combined_rounds.append(combined_round)

        # 9 hole round
        if round.completed_holes == 9:
            if not placeholder:
                # If no previous 9 hole round exists, store in placeholder
                placeholder = round

            else:
                # Combine this 9 hole round with the one in placeholder
                date = placeholder.date
                rating = (placeholder.rating + round.rating) / 2
                slope = (placeholder.slope + round.slope) / 2
                gross_score = placeholder.gross_score + round.gross_score
                course = "Combined 9-hole round"

                # Add round to combined_rounds
                combined_round = CombinedRound(
                    date, course, rating, slope, gross_score
                )
                combined_rounds.append(combined_round)
                placeholder = None  # Reset the placeholder

    # Sort rounds by most recent date
    combined_rounds.sort(key=lambda x: x.date, reverse=True)

    # Takes 20 most recent rounds and sorts by latest date
    recent_rounds = combined_rounds[:20]
    recent_rounds.sort(key=lambda x: x.date, reverse=False)

    return recent_rounds


def get_number_rounds_to_average(num_rounds):
    # Official USGA method to determine how many rounds to average

    rounds_mapping = {
        20: (8, 0),
        19: (7, 0),
        18: (7, -1),
        17: (6, 0),
        16: (6, -1),
        15: (5, 0),
        14: (5, -1),
        13: (4, 0),
        12: (4, -1),
        11: (3, 0),
        10: (3, -2),
        9: (3, -2),
        8: (2, 0),
        7: (2, -1),
        6: (2, -1),
        5: (1, 0),
        4: (1, -1),
        3: (1, -2),
    }

    # Check if 'num_rounds' is in the dictionary, and assign values accordingly
    if num_rounds in rounds_mapping:
        return rounds_mapping[num_rounds]
    else:
        print("Error: Not enough complete rounds to calculate handicap.")
        return (1, 0)


def calc_average_of_smallest_values(rounds, num_to_average):
    # Make list of handicap differentials
    handicap_differentials = [round.handicap_differential for round in rounds]

    # Sort the list in ascending order
    handicap_differentials.sort()

    # Calculate the average
    return sum(handicap_differentials[:num_to_average]) / num_to_average


def calc_handicap_index(rounds):
    # Determine USGA rounds to average and adjustment value
    num_rounds_to_average, adjustment = get_number_rounds_to_average(
        len(rounds)
    )

    # Calculate average of best rounds
    average = calc_average_of_smallest_values(rounds, num_rounds_to_average)

    # Apply adjustment
    adjusted_handicap = average + adjustment

    # Calculate handicap index
    handicap_index = round(0.96 * adjusted_handicap, 1)

    return handicap_index


def output_results(player_name, rounds, handicap_index):
    # Output recent rounds
    for golf_round in rounds:
        # Shorten name if it's over char limit
        course_name = golf_round.course
        if len(course_name) > 32:
            course_name = course_name[:29] + "..."

        print(
            f"{golf_round.date} | {course_name:<32} | Score: {golf_round.gross_score:>3} | Differential: {round(golf_round.handicap_differential, 1):>4}"
        )

    # Output handicap
    print(
        f"\n{player_name}'s official USGA handicap index is {handicap_index}\n"
    )


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
