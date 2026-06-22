import random
import streamlit as st

# FIX: hint messages moved to the UI layer since check_guess now returns outcome only.
MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

def get_range_for_difficulty(difficulty: str):
    # FIX: Manual Fix — corrected ranges for Normal and Hard difficulties
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int, high: int):
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    # FIX: Tuning fix for attempts based on optimal startegy
    # ceil(log2(range)) + 1 (for off-by-one forgiveness)
    "Easy": 6,
    "Normal": 7,
    "Hard": 8,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    # FIXME: Logic breaks here — secret is generated once and cached; changing
    # difficulty recomputes low/high but never regenerates the secret.
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# FIX: AI identified that changing difficulty never regenerated the secret. Track the
# active difficulty in session state; when it changes, reset the round with a new secret
# in the correct range.
if "difficulty" not in st.session_state:
    st.session_state.difficulty = difficulty
elif st.session_state.difficulty != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.rerun()

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # FIXME: Logic breaks here — incomplete reset: score/status/history are NOT
    # cleared, so after a win the status guard stops the new game. Also uses
    # hardcoded randint(1, 100) instead of the difficulty's low/high.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    # FIXME: Logic breaks here — attempts incremented BEFORE validation, so an
    # empty/invalid guess still consumes an attempt and is appended to history.
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        # FIX: AI removed the spurious even-attempt str(secret) cast — always compare ints.
        # outcome is now a plain string; message is looked up from MESSAGES.
        outcome = check_guess(guess_int, st.session_state.secret)
        message = MESSAGES[outcome]

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    # FIXME: Logic breaks here — submit branch never calls st.rerun(), and the
    # info/debug/history panels above render BEFORE this handler, so the UI shows
    # stale state ("guesses populate after a delay").

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
