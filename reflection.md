# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

The game loaded and looked normal: a title, a difficulty selector, a guess box, and a debug panel showing the secret. But playing it quickly felt "off." Guessing the correct number sometimes failed to count as a win, the hints occasionally pointed the wrong direction, my score went down on wrong guesses in ways that didn't make sense, and selecting "Hard" actually gave a smaller (easier) number range than "Normal."

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. **Correct guesses didn't always win.** On even-numbered attempts the code compares my integer guess to the secret cast to a *string* (`str(secret)`), so `42 == "42"` is `False` and the win never registers — instead it falls into a buggy string-comparison branch.
2. **Hints were backwards in the fallback branch.** In the `TypeError`/string branch of `check_guess`, "Too High" tells you to go HIGHER and "Too Low" tells you to go LOWER — both reversed.
3. **"Hard" was easier than "Normal."** `get_range_for_difficulty` returns `1–50` for Hard but `1–100` for Normal, so Hard has the narrower range.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess the exact secret on an even-numbered attempt (e.g. secret is 42, guess 42 on attempt 2) | Game registers a Win | Not counted as a win; falls through to a high/low hint instead, because guess (int) is compared to `str(secret)` | No error; silently wrong |
| Any guess that lands in the string-comparison fallback (even attempt, not equal) | Hint points toward the secret correctly | Hint direction is reversed ("Too High" → "Go HIGHER!", "Too Low" → "Go LOWER!") | No error |
| Select "Hard" difficulty and read the range | Hard has the widest range (hardest) | Range shown is 1–50, narrower/easier than Normal's 1–100 | No error |
| Make a wrong "Too High" guess on different attempts | Score behaves consistently for a wrong guess | Score sometimes +5, sometimes −5 depending on attempt parity | No error |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude (Claude Code) as my main teammate, mostly to read through `app.py`, point out suspicious logic, and explain *why* certain lines behaved oddly. I treated it like a pair programmer: it suggested where to look, and I confirmed each claim by actually running the game and reading the code myself.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

The AI suggested that correct guesses were failing because, on even-numbered attempts, the code compares my integer guess to the secret converted to a string (`secret = str(st.session_state.secret)`), so `42 == "42"` is `False`. I verified this by opening the Developer Debug panel, noting the secret, and guessing it exactly on a second (even) attempt — it did not register a win, which matched the AI's explanation. Removing the `str()` conversion so both sides stay integers fixed it.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

At one point the AI implied the score logic was simply "subtract 5 for any wrong guess," which made it sound consistent. When I traced the `update_score` function, that was misleading: a "Too High" guess actually adds 5 on even attempts and subtracts 5 on odd ones, while "Too Low" always subtracts 5 — so the behavior is parity-dependent, not a flat penalty. I verified by making several wrong guesses and watching the score jump up and down, which contradicted the simpler explanation.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I decided a bug was fixed only when I could reproduce the original failure and then see the corrected behavior on the exact same input. For the win bug, I guessed the secret on an even-numbered attempt, which was the case that used to fail, and confirmed it now registers as a win every time instead of only on odd attempts. I also re-ran the pytest suite after each change so a fix in one place couldn't silently break another, and I refactored the logic into `logic_utils.py` so the tests were exercising the same code the app actually uses.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

I ran `python -m pytest tests/` against `test_game_logic.py`, which calls `check_guess(50, 50)`, `check_guess(60, 50)`, and `check_guess(40, 50)` and expects `"Win"`, `"Too High"`, and `"Too Low"`. This immediately showed a design problem: the original `check_guess` returned a `(outcome, message)` tuple, so the tests would never have matched a plain string. Fixing `check_guess` to return just the outcome string, and moving the hint text into a separate `message_for_outcome` helper, made all 3 tests pass and kept the app and tests in agreement.

- Did AI help you design or understand any tests? How?

Yes. The AI pointed out the mismatch between what the tests asserted (a single string) and what the function returned (a tuple), which I hadn't noticed. It explained that the assertion `result == "Win"` could never be true against a tuple, so the cleanest fix was to change the function's return shape rather than the tests. That helped me understand the tests as a contract: they describe the API the rest of the code is supposed to rely on, not just example inputs.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

I would tell them that every time you click a button or type something, Streamlit runs the whole program again from the start. That means normal variables forget everything between clicks, because they get created fresh each time. Session state is just a special box where you can keep the things you want to remember, like the secret number and the score, so they survive when the program runs again. In this project the New Game button stayed buggy until I cleared everything in that box, not just part of it.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

The habit I want to keep is reproducing a bug before I try to fix it, and then running the tests again after the fix. On this project I would guess the secret on the exact attempt that used to fail, confirm it was broken, make the change, and only trust it once both the manual check and `pytest` passed. That loop kept me from assuming a fix worked just because the code looked right.

- What is one thing you would do differently next time you work with AI on a coding task?

Next time I would check the AI's claims against the actual code sooner instead of taking its summary at face value. In this project the AI described the score logic in a simpler way than it really worked, and I only caught it once I traced the function myself. Verifying earlier would have saved time.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I now treat AI generated code as a confident first draft rather than a finished answer, since it can look polished and still hide real bugs. My job is to read it, test it, and prove it works before I rely on it.
