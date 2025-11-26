"""
Prompt composition + simple scoring utilities.

Keep this logic very lightweight and transparent so
Vu can easily tweak the rating rules later.
"""

def compose_prompt(data: dict) -> str:
    """Build a structured prompt string from form fields."""
    purpose = (data.get("purpose") or "General message").strip()
    audience = (data.get("audience") or "a broad audience").strip()
    tone = (data.get("tone_label") or "Neutral").strip()
    keywords = (data.get("keywords") or "").strip()
    freeform = (data.get("freeform") or "").strip()

    parts = [
        f"Purpose: {purpose}.",
        f"Audience: {audience}.",
        f"Tone: {tone}."
    ]

    if keywords:
        parts.append(f"Keywords: {keywords}.")

    # Short, friendly instruction for the LLM
    parts.append("Please generate a clear, well-structured response.")

    if freeform:
        parts.append(freeform)

    return " ".join(parts)


def calculate_score(prompt: str) -> dict:
    """
    Very simple scoring rule (0–100) based on:
    - Clarity: has Purpose + Audience
    - Specificity: has Keywords
    - Tone match: has Tone
    - Length bonus: a little extra if not super short
    """
    has_purpose = "Purpose:" in prompt
    has_audience = "Audience:" in prompt
    has_keywords = "Keywords:" in prompt
    has_tone = "Tone:" in prompt

    clarity = 0
    if has_purpose:
        clarity += 20
    if has_audience:
        clarity += 20

    specificity = 30 if has_keywords else 0
    tone_match = 30 if has_tone else 0

    # Reward prompts that are not tiny, but cap the bonus
    length_bonus = min(10, max(0, len(prompt) // 120))

    total = clarity + specificity + tone_match + length_bonus

    return {
        "total": total,
        "details": {
            "clarity": clarity,
            "specificity": specificity,
            "tone_match": tone_match,
            "length_bonus": length_bonus,
        },
    }


def simulate_preview(prompt: str, tone_value: int) -> dict:
    """
    Optional helper if you ever want separate tone preview.
    Not currently used by composer.js but kept for future use.
    """
    if tone_value < 25:
        tone_name = "Formal"
        text = (
            f"This version keeps a professional, structured tone based on: "
            f"{prompt[:80]}..."
        )
    elif tone_value < 60:
        tone_name = "Friendly"
        text = (
            f"Here's a friendly, accessible version of your idea: "
            f"{prompt[:80]}..."
        )
    else:
        tone_name = "Witty"
        text = (
            f"Here's a more playful take on your idea: "
            f"{prompt[:80]}..."
        )

    return {"tone": tone_name, "text": text}
