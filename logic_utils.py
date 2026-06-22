def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Manual Fix — corrected ranges for Normal and Hard difficulties
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        # Edge case spotted; stretch fix
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)

        # FIX: manual fix, check for out-of-range guesses
        if value < low or value > high:
            return False, None, f"Guess must be between {low} and {high}."

    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns one of: "Win", "Too High", "Too Low"
    """
    # FIX: AI identified that check_guess returned a tuple and had a TypeError fallback
    # for string comparisons that only existed to mask the str(secret) cast at the call
    # site. Both removed together. Now returns outcome string only (matches test assertions)
    # and compares ints directly — no try/except needed.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: AI identified two scoring bugs here. Removed the extra +1 — attempt_number
        # is already the current count, so (attempt_number + 1) was double-counting and
        # underpaying points on every win.
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: AI flagged that Too High was rewarding +5 on even attempts while Too Low
        # always cost -5. Removed the even/odd branch so both directions cost the same.
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score