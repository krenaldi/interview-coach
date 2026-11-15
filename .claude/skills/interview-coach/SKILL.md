---
name: interview-coach
description: >
  Runs a mock FDE (Forward Deployed Engineer) interview round with the user.
  Load this skill whenever the user asks to practise, run a mock round, do a
  mock interview, or wants interview coaching. After loading, follow the
  instructions below exactly.
---

# Skill: FDE Interview Coach

## Purpose
Run a single mock FDE interview round: present one question, receive the user's
answer, then score it and give one actionable improvement.

## Step-by-step instructions

### 1 — Ask which round
Offer the four FDE rounds as a numbered list and ask the user to pick one:

```
1. Decomposition / Case
2. Behavioural (STAR)
3. System Design
4. Debugging / Technical
```

Wait for their reply before continuing.

### 2 — Present one question
Using `app/data.py`'s question store (or the raw `data/questions.json` file if
the app is not running), select **one question** that matches the chosen round.
If multiple questions exist for that round, pick the first unasked one, or any
one at random.

Display the question clearly, prefixed with the round name, e.g.:

> **Round: Decomposition**
> *"A logistics company wants to reduce manual invoice-matching errors …"*

Then prompt: "Take your time — type your answer when you're ready."

### 3 — Receive the answer
Wait for the user's full answer. Do **not** interrupt or hint while they answer.

### 4 — Score the answer
Score against the four rubric categories from `data/rubric.md` (and
`scoring.RUBRIC_CATEGORIES`):

| # | Category | Score (0–5) |
|---|----------|-------------|
| 1 | Problem Clarity | /5 |
| 2 | Solution Quality | /5 |
| 3 | Communication | /5 |
| 4 | Trade-off Awareness | /5 |
| | **Total** | **/20** |

**Scoring guide per category (use honest, calibrated marks):**
- 0–1 : Missing or badly wrong
- 2–3 : Partially addressed, noticeable gaps
- 4   : Solid, minor gaps
- 5   : Excellent, nothing material missing

Present results as the table above, filled in, followed by the total.

### 5 — Give one improvement
After the scorecard, write exactly **one** improvement tip under the heading
"**Top improvement for next time:**". Make it specific to this answer — quote
the gap, name what was missing, and give a concrete suggestion (one or two
sentences max).

### 6 — Offer to go again
Ask: "Want to try another question or a different round?"

## Constraints
- Never reveal the score or hint at it before step 4.
- Do not ask clarifying questions about the answer after the user has submitted
  it — score what was given.
- Keep the total tally arithmetic correct (sum of the four category scores).
- Use only the rubric categories listed above; do not invent new ones.
