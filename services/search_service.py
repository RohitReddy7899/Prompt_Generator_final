def search_prompts(prompts, keyword):
    sorted_prompts = sorted(prompts, key=lambda x: x.get('score', {}).get('total', 0))
    results = []
    left, right = 0, len(sorted_prompts) - 1
    while left <= right:
        mid = (left + right) // 2
        text = sorted_prompts[mid].get('keywords', '') + sorted_prompts[mid].get('prompt', '')
        if keyword.lower() in text.lower():
            results.append(sorted_prompts[mid])
            i = mid - 1
            while i >= 0 and keyword.lower() in (sorted_prompts[i].get('prompt', '')).lower():
                results.append(sorted_prompts[i]); i -= 1
            i = mid + 1
            while i < len(sorted_prompts) and keyword.lower() in (sorted_prompts[i].get('prompt', '')).lower():
                results.append(sorted_prompts[i]); i += 1
            break
        elif keyword.lower() < text.lower():
            right = mid - 1
        else:
            left = mid + 1
    return sorted(results, key=lambda x: x.get('score', {}).get('total', 0), reverse=True)
