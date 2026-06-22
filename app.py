import random
import streamlit as st

# FIX: pure game logic refactored into logic_utils.py; imported here.
from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score

# FIX: hint messages live in the UI layer since check_guess now returns outcome only.
MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

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
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "last_message" not in st.session_state:
    st.session_state.last_message = ""

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
    st.session_state.last_message = ""
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

# FIX: hint rendered from state here so it survives the st.rerun() in the submit handler.
if show_hint and st.session_state.get("last_message"):
    st.warning(st.session_state.last_message)

if new_game:
    # FIX: AI identified incomplete reset — score/status/history were not cleared so
    # a won game would immediately stop again. Also replaced hardcoded randint(1, 100)
    # with the current difficulty's range.
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.last_message = ""
    st.session_state.secret = random.randint(low, high)
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.error(err)
    else:
        # FIX: AI moved attempts increment to after validation — invalid guesses no
        # longer consume an attempt or get recorded in history.
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: AI removed the spurious even-attempt str(secret) cast — always compare ints.
        # outcome is now a plain string; message is looked up from MESSAGES.
        outcome = check_guess(guess_int, st.session_state.secret)
        st.session_state.last_message = MESSAGES[outcome]

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

        # FIX: AI explained Streamlit reruns — panels above render before this handler
        # runs, so state updates lag a click. st.rerun() triggers a fresh top-to-bottom
        # pass so the info/debug/history panels reflect the updated state immediately.
        st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
