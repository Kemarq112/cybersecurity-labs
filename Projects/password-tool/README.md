# Password Strength Checker

A simple, educational tool that scores a password (0–100), estimates entropy, gives a rough crack-time guess, and provides actionable feedback.

> ⚠️ For learning only. Do not collect real user passwords. Run locally.

---

## Features
- Scores passwords on length, character variety, and entropy  
- Detects common passwords, keyboard sequences, and repeated characters  
- Estimates entropy & brute-force crack-time (rough guess)  
- Gives feedback on how to improve  

---

## Usage
From the project root, run:

```bash
python Projects/password-tool/password_checker.py

Score: 28/100  →  Weak
Estimated entropy: 36.4 bits
Rough crack-time (1e10 guesses/sec): ~1.11 hr

Feedback:
 - Use at least 12–16 characters.
 - Mix UPPER and lower case letters.
 - Include at least one digit.
 - Include special characters (!@#$%^&*()…).


