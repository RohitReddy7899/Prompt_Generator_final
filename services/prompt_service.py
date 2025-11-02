def compose_prompt(data):
    purpose = data.get('purpose', 'General')
    audience = data.get('audience', 'unspecified audience')
    tone = data.get('tone_label', 'Neutral')
    keywords = data.get('keywords', '')
    freeform = data.get('freeform', '')
    base = f"Purpose: {purpose}. Audience: {audience}. Tone: {tone}."
    if keywords: base += f" Keywords: {keywords}."
    base += " Please generate a clear, high-quality text."
    if freeform: base += f" {freeform}"
    return base

def calculate_score(prompt):
    clarity = 30 if 'Purpose:' in prompt else 0
    specificity = 30 if 'Keywords:' in prompt else 0
    tone_match = 30 if 'Tone:' in prompt else 0
    length_bonus = min(10, len(prompt)//100)
    total = clarity + specificity + tone_match + length_bonus
    return {
        'total': total,
        'details': {
            'clarity': clarity,
            'specificity': specificity,
            'tone_match': tone_match,
            'length_bonus': length_bonus
        }
    }

def simulate_preview(prompt, tone_value):
    if tone_value < 25:
        t = "Formal"
        body = f"This message adopts a structured and professional tone based on: {prompt[:60]}..."
    elif tone_value < 60:
        t = "Friendly"
        body = f"Here's a friendly, reader-focused version of your prompt: {prompt[:60]}..."
    else:
        t = "Witty"
        body = f"Imagine a clever spin on your idea: {prompt[:60]}..."
    return {'tone': t, 'text': body}
