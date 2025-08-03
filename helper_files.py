import csv
import os
from models.round import Round


def import_rounds(filename):
    headers = []
    rounds = []

    filepath = os.path.join("data", filename)

    with open(filepath) as f:
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
