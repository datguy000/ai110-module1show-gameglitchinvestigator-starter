# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

### Some bugs before I even started guessing:
 - On open, Normal states 8 attempts allowed, message states 7, and debug info states 1. 
    - Pressing new game sets message to correct value but brings debug to zero
 - Switching difficulty changes the difficulty in debug info, but doesn't change the secret number, or the range in the top message.
    - Also ranges and attempts probably need some adjustments:
      - Easy: 1-20; 6 attempts
      - Normal: 1-100; 8 attempts
      - Hard: 1-50; 5 attempts
    - Note: using optimal strategy of cutting in half and using higher or lower range, attempts should be greater than ceiling[log2(range)] 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| No guess and press submit twice| Neither accepted | Seems to do nothing first, then accepts empty string | N/a |
| 50 | Hint should say to go higher (secret was 59) | says "Go LOWER!" | N/a |
| 200 | Should be rejected since out of range | says "Go HIGHER!" | N/a |

 *Note : guesses seem to poulate after a delay*

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
