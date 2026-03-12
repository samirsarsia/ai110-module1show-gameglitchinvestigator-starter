# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
- What did the game look like the first time you ran it?

  It looked fine when I first opened it, but when I ran the game I noticed some problems. The higher/lower hints were reversed, so the messages didn’t match the guesses. When I clicked New Game, it didn’t actually start a new game and only worked if I refreshed the page. The range was supposed to be 1–100, but it still allowed numbers outside that range. I also noticed that the easy, normal, and hard difficulty levels were set up incorrectly.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

  I used Claude to help me understand what might be causing bugs and how to fix them. One suggestion that worked was checking the comparison logic for the higher/lower messages. Claude suggested verifying whether the conditions for > and < were reversed, and after testing it I realized the logic needed to be swapped, which fixed the hint issue. One suggestion that didn’t work well was when AI recommended changing part of the reset function for the new game button, but after testing it the game still didn’t restart properly.



---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

  I checked if the bugs were fixed by playing the game again after making changes. I tried guessing numbers that were higher and lower than the secret number to see if the hints were correct. I also tested numbers outside the 1–100 range to make sure the game didn’t accept them. AI suggested testing edge cases like numbers below 1 or above 100, which helped me confirm the fix worked.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit reruns the whole program every time you click something or enter a number. At first I didn’t understand why things kept resetting. Session state helps save information so the app can remember things like the secret number or guesses. Without it, the game would restart every time you interact with it.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

  One habit I want to reuse is testing my code after every small change instead of waiting until the end. It made it easier to find where the bug was coming from. Next time I work with AI on a coding task, I would double-check the suggestions more carefully and test them instead of assuming they are correct. This project showed me that AI can be helpful for ideas and guidance, but you still need to understand and verify the code yourself.