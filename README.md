# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!
   
## 📝 Document Your Experience

**Game's purpose:**
A number-guessing game where the player tries to guess a secret number within a limited number of attempts. After each guess, the game returns a "Too High" or "Too Low" hint to help narrow it down. The difficulty setting controls the range and attempt limit.

**Bugs found:**
- Hints were inverted ("Too High" said "Go HIGHER!" and vice versa)
- Hard difficulty had a smaller range than Normal (1–50 vs 1–100), making it easier
- Out-of-range guesses like 200 were accepted instead of rejected
- The secret number didn't regenerate when switching difficulty
- Invalid guesses consumed an attempt before being validated
- New Game only reset attempts, leaving score/status/history stale — so a won game couldn't restart
- Scoring had two bugs: wins underpaid points due to a double off-by-one, and "Too High" rewarded points on even attempts
- The UI lagged a click behind because panels rendered before the submit handler ran

**Fixes applied:**
- Corrected the difficulty ranges and attempt limits
- Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` into `logic_utils.py`
- Added range validation to `parse_guess`
- Simplified `check_guess` to return an outcome string only, removing the broken string-comparison fallback
- Fixed scoring in `update_score`
- Added session state tracking to regenerate the secret on difficulty change
- Moved attempt counting to after validation
- Fixed New Game to do a full reset using the correct range
- Added `st.rerun()` and stored the hint in session state to fix the stale UI


## 📸 Demo Walkthrough

1. User enters a guess of 40
2. Game returns "Too Low"
3. User enters a guess of 70 → "Too High"
4. Score updates correctly after each guess
5. Game ends after the correct guess


## 🧪 Test Results

```
collected 5 items                                                                                                                             

tests/test_game_logic.py::test_winning_guess PASSED                                                                                     [ 20%]
tests/test_game_logic.py::test_guess_too_high PASSED                                                                                    [ 40%]
tests/test_game_logic.py::test_guess_too_low PASSED                                                                                     [ 60%]
tests/test_game_logic.py::test_parse_guess_too_high_out_of_range PASSED                                                                 [ 80%]
tests/test_game_logic.py::test_parse_guess_too_low_out_of_range PASSED                                                                  [100%]

============================================================= 5 passed in 0.03s ==============================================================
```

## 🚀 Stretch Features

**Challenge 1: Advanced Edge-Case Testing**

Added two additional pytest cases in `tests/test_game_logic.py` targeting out-of-range inputs to verify that `parse_guess` correctly rejects values outside the difficulty's valid range:

- `test_parse_guess_too_high_out_of_range` — guessing `"200"` against a 1–100 range is rejected
- `test_parse_guess_too_low_out_of_range` — guessing `"0"` against a 1–100 range is rejected

These edge cases were identified during the debugging process when the original `parse_guess` had no range validation at all, allowing any integer to pass through. Both new tests pass alongside the three original tests — see Test Results above for the full pytest output.
