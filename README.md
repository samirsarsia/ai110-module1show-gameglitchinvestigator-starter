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

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

**Game's purpose.** Glitchy Guesser is a number guessing game built with Streamlit. The app picks a secret number inside a range that depends on the chosen difficulty (Easy, Normal, or Hard), and the player tries to guess it within a limited number of attempts. After each guess the game says whether the guess is too high or too low and updates a score, and it announces a win or a loss when the game ends.

**Bugs I found.**

1. **The secret was corrupted on even attempts.** On every even-numbered attempt the code compared the integer guess against `str(secret)`, so `42 == "42"` was `False` and a correct guess never registered as a win.
2. **The hints were backwards.** In the broken string-comparison branch, "Too High" told the player to go HIGHER and "Too Low" told them to go LOWER.
3. **"Hard" was easier than "Normal."** The difficulty range for Hard was `1-50`, narrower than Normal's `1-100`.
4. **Score changes were arbitrary.** Wrong guesses added or subtracted points based on attempt parity instead of leaving the score alone.
5. **Win points were off by one.** The win bonus used `attempt_number + 1`, which double-counted the already-incremented attempt and underpaid first-try wins.
6. **Inconsistent attempt setup.** Attempts initialized to `1` but New Game reset them to `0`, so "Attempts left" was wrong on a fresh load.
7. **New Game did not fully reset.** It reset the secret and attempts but left `score`, `status`, and `history` alone, so a finished game could stay stuck on "won"/"lost".
8. **Hardcoded range text.** The info box always said "between 1 and 100" regardless of difficulty.

**Fixes I applied.**

- Refactored `get_range_for_difficulty`, `parse_guess`, `check_guess`, and `update_score` out of `app.py` into `logic_utils.py`, and imported them back into the app.
- Compared the guess against the integer secret directly, removing the `str(secret)` conversion so wins always register.
- Moved hint text into a `message_for_outcome` helper with the correct directions (too high -> go LOWER, too low -> go HIGHER).
- Widened Hard to `1-200` so harder difficulties have a wider range.
- Made wrong guesses leave the score unchanged and fixed the win bonus to use `attempt_number - 1` with a 10-point floor.
- Initialized attempts to `0` to match New Game, and made New Game reset `score`, `status`, and `history` while using the active difficulty range.
- Updated the info box to show the real `{low}`-`{high}` range.
- Added `# FIX` comments at each change and expanded the pytest suite from 3 to 19 tests so every fix is covered.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Start the app with `python -m streamlit run app.py` and open it in the browser.
2. In the sidebar, choose a difficulty. Notice the range updates correctly: Easy is 1-20, Normal is 1-100, and Hard is now the widest at 1-200. The sidebar also shows how many attempts are allowed.
3. Open the "Developer Debug Info" panel to see the current secret number, attempts, score, and history (useful for demonstrating that the game works).
4. Type a guess and click "Submit Guess". The hint now points the correct way: a too-high guess says "Go LOWER" and a too-low guess says "Go HIGHER". The score stays unchanged on wrong guesses.
5. Keep guessing using the hints. When you enter the secret number, the game registers a win on any attempt (including even-numbered ones, which used to fail), shows balloons, and reports your final score.
6. Click "New Game" to fully reset the game: a new secret in the current range, score back to 0, status back to playing, and a cleared history, so you can immediately play again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python -m pytest tests/
collected 19 items

tests/test_game_logic.py ...................                             [100%]

============================== 19 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
