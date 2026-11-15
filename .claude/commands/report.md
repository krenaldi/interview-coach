Read `data/results.json` using the Read tool.

If the file is empty or contains an empty array `[]`, reply:
"No practice rounds recorded yet. Run a mock round first with /interview-coach or by asking to practise."
Then stop.

Otherwise, calculate and display the following report — do all arithmetic yourself, do not call any external tool or the app:

---

**FDE Practice Report**

**Rounds practised:** <count of entries in results.json>

**Average total score:** <mean of all `total` fields, rounded to one decimal place> / 20

**Scores by category** (average across all rounds):
- Problem Clarity: <avg> / 5
- Solution Quality: <avg> / 5
- Communication: <avg> / 5
- Trade-off Awareness: <avg> / 5

**Weakest category:** <the category with the lowest average — if tied, list all that tie>

**Focus for next session:** One concrete, specific suggestion based on the weakest category and any patterns visible in the results (e.g. consistently low trade-off scores → "practise explicitly stating what you are NOT doing and why before wrapping up your answer").

---

Keep the tone direct and coaching-focused. Do not repeat raw JSON back to the user.
