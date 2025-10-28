#!/usr/bin/env python3
"""
Test score extraction from Gemini responses
"""

import re

# Sample responses that Gemini might return
test_responses = [
    "**4. Performance Score (0-100):**\n\n60/100",
    "**4. Performance Score (0-100):**\n\n**60/100**",
    "**4. Performance Score (0-100):**\n\n85",
    "**4. Performance Score (0-100):**\n\nScore: 75/100",
    "**4. Performance Score (0-100):**\n\nI would give this project a score of 82 out of 100.",
    "**4. Performance Score (0-100):**\n\n**Justification:** The score reflects...\n\n**60/100**",
]

def extract_score(score_text):
    """Extract score using the improved logic"""
    # First try to find X/100 pattern
    score_match = re.search(r'(\d+)\s*/\s*100', score_text)
    if score_match:
        return int(score_match.group(1)), "X/100 pattern"
    else:
        # Look for standalone number (2-3 digits)
        score_match = re.search(r'\b(\d{2,3})\b', score_text)
        if score_match:
            score_value = int(score_match.group(1))
            # Validate it's in reasonable range
            if 0 <= score_value <= 100:
                return score_value, "standalone number"
    return None, "no match"

print("Testing Score Extraction:")
print("=" * 60)

for i, response in enumerate(test_responses, 1):
    sections = response.split("**")
    for j, section in enumerate(sections):
        if "score" in section.lower() and "performance" in section.lower() and j + 1 < len(sections):
            score_text = sections[j + 1].strip()
            score, method = extract_score(score_text)
            print(f"\nTest {i}:")
            print(f"  Input: {score_text[:80]}")
            print(f"  Extracted Score: {score}")
            print(f"  Method: {method}")

print("\n" + "=" * 60)
print("Testing complete!")
