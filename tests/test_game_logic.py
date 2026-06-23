from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    message_for_outcome,
    update_score,
)


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range_is_widest():
    low, high = get_range_for_difficulty("Hard")
    assert (low, high) == (1, 200)
    # Hard should never be easier (narrower) than Normal
    assert high > get_range_for_difficulty("Normal")[1]

def test_unknown_difficulty_defaults_to_normal():
    assert get_range_for_difficulty("Something Else") == (1, 100)


# --- parse_guess ---

def test_parse_valid_integer():
    assert parse_guess("42") == (True, 42, None)

def test_parse_float_truncates_to_int():
    ok, value, err = parse_guess("3.9")
    assert ok is True
    assert value == 3
    assert err is None

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok is False
    assert value is None
    assert err == "Enter a guess."

def test_parse_non_numeric():
    ok, value, err = parse_guess("abc")
    assert ok is False
    assert value is None
    assert err == "That is not a number."


# --- message_for_outcome ---

def test_message_win():
    assert message_for_outcome("Win") == "🎉 Correct!"

def test_message_too_high_says_go_lower():
    # Guess too high means the player should go LOWER
    assert message_for_outcome("Too High") == "📈 Go LOWER!"

def test_message_too_low_says_go_higher():
    # Guess too low means the player should go HIGHER
    assert message_for_outcome("Too Low") == "📉 Go HIGHER!"


# --- update_score ---

def test_win_on_first_attempt_awards_full_points():
    # attempt_number is 1 on a first-try win -> 100 points
    assert update_score(0, "Win", 1) == 100

def test_win_awards_fewer_points_for_later_attempts():
    assert update_score(0, "Win", 3) == 80

def test_win_points_floor_at_ten():
    # Many attempts should never drop below the 10-point floor
    assert update_score(0, "Win", 20) == 10

def test_wrong_guess_does_not_change_score():
    assert update_score(50, "Too High", 2) == 50
    assert update_score(50, "Too Low", 3) == 50
