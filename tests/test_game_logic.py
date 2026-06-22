from logic_utils import check_guess, parse_guess

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

def test_parse_guess_too_high_out_of_range():
    # 200 is above the 1-100 range and should be rejected
    ok, value, err = parse_guess("200", 1, 100)
    assert ok is False
    assert value is None

def test_parse_guess_too_low_out_of_range():
    # 0 is below the 1-100 range and should be rejected
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None