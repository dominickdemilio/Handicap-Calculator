from dataclasses import dataclass, field


@dataclass
class CombinedRound:
    date: str
    course: str
    rating: float
    slope: float
    gross_score: int
    handicap_differential: float = field(init=False)

    def __post_init__(self):
        if self.slope == 0:
            raise ValueError("Slope cannot be zero")
        self.handicap_differential = (
            (self.gross_score - self.rating) * 113 / self.slope
        )
