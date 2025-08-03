from models.combined_round import CombinedRound


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
