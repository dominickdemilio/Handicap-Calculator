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
