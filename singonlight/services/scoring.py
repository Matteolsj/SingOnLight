def calculate_score(expected_rhythm: list[int], observed_rhythm: list[int], score: int = 0) -> int:
    """Score a rhythm match, rewarding exact and slightly delayed sounds."""
    assert len(expected_rhythm) <= len(observed_rhythm)
    if not expected_rhythm:
        return score

    if expected_rhythm[0] == 1:
        if observed_rhythm[0] == 1:
            return calculate_score(expected_rhythm[1:], observed_rhythm[1:], score + 10)
        if len(observed_rhythm) > 1 and observed_rhythm[1] == 1:
            score += 5
            observed_rhythm = [0] + observed_rhythm[2:]
            if len(expected_rhythm) > 1 and expected_rhythm[1] == 1:
                observed_rhythm[0] = 1
            return calculate_score(expected_rhythm[1:], observed_rhythm, score)

    if expected_rhythm[0] == 0 and observed_rhythm[0] == 1:
        score -= 10

    points = 10 if expected_rhythm[0] == observed_rhythm[0] else 0
    return calculate_score(expected_rhythm[1:], observed_rhythm[1:], score + points)

def calculate_percentage(expected_rhythm: list[int], observed_rhythm: list[int]) -> float:
    """Return the match score as a percentage from 0 to 100."""
    maximum_score = calculate_score(expected_rhythm, expected_rhythm)
    if maximum_score == 0:
        return 0.0
    percentage = calculate_score(expected_rhythm, observed_rhythm) / maximum_score * 100
    return max(0, min(100, percentage))