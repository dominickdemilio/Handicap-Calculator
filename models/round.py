from dataclasses import dataclass
from typing import Optional


@dataclass
class Round:
    player: str
    date: str
    time: str
    course: str
    rating: Optional[float]
    slope: Optional[float]
    scoring_format: str
    completed_holes: Optional[int]
    gross_score: Optional[int]
    gross_score_over_par: Optional[int]

    def __init__(
        self,
        player,
        date,
        time,
        course,
        rating,
        slope,
        scoring_format,
        completed_holes,
        gross_score,
        gross_score_over_par,
    ):
        self.player = player
        self.date = date
        self.time = time
        self.course = course
        self.rating = float(rating) if rating else None
        self.slope = float(slope) if slope else None
        self.scoring_format = scoring_format
        self.completed_holes = int(completed_holes) if completed_holes else None
        self.gross_score = int(gross_score) if gross_score else None
        self.gross_score_over_par = (
            int(gross_score_over_par) if gross_score_over_par else None
        )

    def print_summary(self):
        print(
            f"{self.player}; {self.date}; {self.rating}; {self.slope}; "
            f"{self.scoring_format}; {self.completed_holes}; {self.gross_score}\n"
        )
