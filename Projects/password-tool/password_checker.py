#!/usr/bin/env python3
"""
Password Strength Checker (educational)
- Scores password 0–100
- Gives actionable feedback
- Estimates brute-force time (very rough)
"""

import math
import re
from typing import List, Tuple

# A tiny sample of common passwords to flag (expand later)
COMMON = {
    "123456","password","qwerty","111111","123123","abc123","letmein","admin",
    "iloveyou","welcome","monkey","dragon","football","shadow","princess",
    "password1","123456789","12345","12345678"
}

# Basic keyboard sequences to catch (extend as you like)
SEQUENCES = ["qwerty", "asdf", "zxcv", "1234", "password", "admin"]

SPECIALS = r"!@#$%^&*()\-_=+\[\]{};:'\",.<>/?\\|`~"

def character_sets(pw: str) -> Tuple[bool,bool,bool,bool]:
    lower = any(c.islower() for c in pw)
    upper = any(c.isupper() for c in pw)
    digit = any(c.isdigit() for c in pw)
    special = any(c in SPECIALS for c in pw)
    return lower, upper, digit, special

def has_repeats(pw: str, n: int = 3) -> bool:
    """Detect 3+ of the same char in a row."""
    return re.search(r"(.)\1{" + str(n-1) + r",}", pw) is not None

def has_sequence(pw: str) -> bool:
    pw_low = pw.lower()
    return any(seq in pw_low for seq in SEQUENCES)

def entropy_bits(pw: str) -> float:
    """Very rough entropy estimate based on charset size."""
    lower, upper, digit, special = character_sets(pw)
    charset = 0
    if lower: charset += 26
    if upper: charset += 26
    if digit: charset += 10
    if special: charset += len(SPECIALS)
    if charset == 0:
        return 0.0
    return len(pw) * math.log2(charset)

def crack_time_guess(bits: float) -> str:
    """Assume 1e10 guesses/sec (modern GPU cluster, highly variable!)."""
    guesses = 2 ** bits
    seconds = guesses / 1e10
    # Convert to readable duration
    units = [("yr", 31557600), ("day", 86400), ("hr", 3600), ("min", 60), ("sec", 1)]
    for name, size in units:
        if seconds >= size:
            value = seconds / size
            return f"~{value:.2f} {name}"
    return "<1 sec"

def score_password(pw: str) -> Tuple[int, List[str]]:
    feedback = []
    if not pw:
        return 0, ["Password is empty."]

    # Base score from length (up to 40 pts)
    length_pts = min(len(pw) * 3, 40)

    # Variety (up to 40 pts)
    lower, upper, digit, special = character_sets(pw)
    variety_count = sum([lower, upper, digit, special])
    variety_pts = [0, 8, 18, 30, 40][variety_count]

    # Entropy bonus (up to 20 pts)
    bits = entropy_bits(pw)
    entropy_pts = min(int(bits / 4), 20)

    score = length_pts + variety_pts + entropy_pts
    score = min(score, 100)

    # Deductions & feedback
    if pw.lower() in COMMON:
        score = max(score - 35, 0)
        feedback.append("Password appears in a common-password list.")
    if has_sequence(pw):
        score -= 10
        feedback.append("Avoid keyboard sequences (e.g., 'qwerty', '1234').")
    if has_repeats(pw):
        score -= 5
        feedback.append("Avoid repeating characters (e.g., 'aaa', '1111').")

    # Advice based on present features
    if len(pw) < 12:
        feedback.append("Use at least 12–16 characters.")
    if not lower or not upper:
        feedback.append("Mix UPPER and lower case letters.")
    if not digit:
        feedback.append("Include at least one digit.
