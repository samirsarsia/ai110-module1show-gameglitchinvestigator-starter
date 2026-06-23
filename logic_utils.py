def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty.

    Harder difficulties use a wider range.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    # FIX: Hard is now the widest range (1-200). Originally it was 1-50, narrower
    # than Normal, so "Hard" was actually easier. Claude caught the inverted ranges.
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    Returns one of: "Win", "Too High", "Too Low".
    """
    # FIX: Returns a single outcome string (not a tuple). The old version returned
    # (outcome, message) and had a buggy string-comparison fallback. Claude noted
    # the tuple broke tests/test_game_logic.py, which assert against a plain string.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


# FIX: Hint directions corrected here. The old fallback told the player to go
# HIGHER when too high and LOWER when too low. Claude flagged the reversed hints.
def message_for_outcome(outcome: str):
    """Return the user-facing hint message for an outcome."""
    if outcome == "Win":
        return "🎉 Correct!"
    if outcome == "Too High":
        return "📈 Go LOWER!"
    if outcome == "Too Low":
        return "📉 Go HIGHER!"
    return ""


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number.

    A win awards more points the fewer attempts it took. Wrong guesses do
    not change the score.
    """
    # FIX: Use (attempt_number - 1) so a first-try win scores the full 100; the old
    # code used (attempt_number + 1) and double-counted. Wrong guesses no longer
    # change the score (the old code added/subtracted 5 by attempt parity). Claude
    # walked me through the off-by-one and the arbitrary parity-based scoring.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return current_score + points

    return current_score
