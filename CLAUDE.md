# Game Glitch Investigator — Working Context

A Streamlit number-guessing game (`app.py`) seeded with intentional bugs. Mission: fix the
logic, refactor the pure functions into `logic_utils.py`, and make `pytest` pass.

## How we're working (important)
This is a learning project. **The student writes the code.** Claude's role is tutor +
pair: explain the bug, point to the spot, suggest an approach, optionally sketch a fix —
then stop and let the student make the edit and run the tests. Go **one bug at a time**;
don't run ahead through the whole list.

A full reference solution exists on the **`claude-answer-key`** branch (do not merge).
`git diff main claude-answer-key` to compare; only peek if genuinely stuck.

## Decisions already agreed
- **Sequencing:** fix in `app.py` first (visible/playable), then move the 4 pure functions
  into `logic_utils.py`, then run pytest.
- **`check_guess` should return the outcome STRING only** (`"Win"`/`"Too High"`/`"Too Low"`)
  — that's what the provided tests assert. Map the hint message in the UI layer.
- **Ranges:** Easy `1–20`, Normal `1–50`, Hard `1–100`.
- **Attempt limits:** keep each `> ceil(log2(range))` so games stay winnable.

## Bug checklist (student to fix)
- ✅ Inverted hints (fixed in an earlier commit)
- ✅ First-load pre-guessed attempt (earlier commit)
- ✅ Hardcoded range message (earlier commit)
- ⬜ `get_range_for_difficulty`: make Hard's range larger than Normal's
- ⬜ `parse_guess`: validate the guess is within range
- ⬜ `check_guess`: remove the string-comparison fallback; return outcome only
- ⬜ `update_score`: Win double off-by-one; Too High even-attempt scoring
- ⬜ `attempt_limit_map`: align attempts with the new ranges
- ⬜ Remove the even-attempt `str(secret)` branch in the submit handler
- ⬜ Regenerate the secret when difficulty changes
- ⬜ Count an attempt only after the guess validates
- ⬜ Full reset in New Game (score/status/history + use difficulty range)
- ⬜ Stale UI after submit (panels render before the handler)
- ⬜ Refactor the 4 functions into `logic_utils.py` + import in `app.py`
- ⬜ Add ≥1 new pytest case; `pytest` green
- ⬜ Reflection §2/§3, `#FIX:` comments, commit, `git push origin main`  (student-owned)

## Next up
Pick one bug to tackle first.

## Commands
- Tests: `.\.venv\Scripts\python.exe -m pytest tests/`
- Run app: `.\.venv\Scripts\python.exe -m streamlit run app.py`
