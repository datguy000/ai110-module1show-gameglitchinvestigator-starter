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
  - Claude Code
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - Backwards hint (guessed 50, secret 59 → "Go LOWER")

    app.py:37-40 — the messages are inverted: "Too High" says "Go HIGHER!" and "Too Low" says "Go LOWER!". That's the direct cause.

    This was correct and something I noticed while just looking at app.py in the github repository before having my environment fully setup.

  - After in Phase 2, when implementing these changes, I was able to manually test and see if the changes worked as well as in the pytest default tests.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - Two things that are correct (don't touch them)

    The ranges (app.py:4-11) and attempt limits (app.py:80-84) already match your spec (Easy 1–20/6, Normal 1–100/8, Hard 1–50/5). The trouble is the message (#2) and secret (#3) ignore them — not the values themselves.

    I think this is actually incorrect. The ranges I noted weren't the specs for the project, it was a note of what the ranges and attempts were set to. So I expect them to be accurate to the hardcoded values, but I think that Hard should probably have a larger range than Normal, and though I inititally though that the number of guesses should go down, technically, if we go by the optimal strategy of splitting the range in half; if the ranges essentially double based on difficulty, one added guess per difficulty would suffice, and anything less would mean there is a chance it is impossible to win without luck, even if you use the optimal strategy.

  - When implementing these changes, thought they were arbitrary, I reasoned with the assistant to make it feel balanced, changing attempts to be kind and give one more than optimal, so it isn't impossible and can be played around with.

  - One other hiccup I experienced was the AI assistant suggesting to use st.rerun() to make sure there weren't any inconsistancies being displayed, but this removed the hints from display, so we decided to add the messages to the session so it could be shown again.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I tested things manually to ensure they were being fixed and used pytest towards the end for added validation.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - As described above, after adding the st.rerun() line, I lost the hints which required further debugging and refactoring to bring back.
- Did AI help you design or understand any tests? How?
  - Yes, I asked for it to break things down for me as I went, and I had a few tries before getting a sense of what st.rerun() actually did. But some analogies later, I think I get it better now.

  - I also had a crazy moment towards the beginning because I was planning a gameplan for how I was approaching the project and my assistant went off the rails trying to do the whole project for me. I had to reset it so I could actually do the project.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
  -  Streamlit reruns from top to bottom, it was explained to me like a printer running top down, line by line, but if something changes earlier, it can lead to desync issues, and starting from top it may "forget" certain things. So session states opperate as a form of outside memory so it can remember important information, and ensures things stay consistant. This rerun occurs everytime a user interacts with something from the page.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git. -- Honestly all of these. I'd like to make sure I run tests as I go rather than at the end. I want to work on my git fluency. I also want more familiarity with assistants so I don't run into issues where it goes rogue and does my whole project for me without me.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would start by ensuring that I lay some guardrails and that planning stays with me in the drivers seat. After my first planning prompt, it took off and did the whole project in a few minutes without any of my say... it didn't help that it was in opus for the beginning portion either, but I know how to switch models now, and that will be one of my first checks moving forward.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - I've used AI as a coding assistant helping me with logic and planning, but this is my first experience with a true agent going and taking charge. And that first expereince, seeing it do the project in 5 minutes was absolutely crazy and reshaped how I see it entirely!
