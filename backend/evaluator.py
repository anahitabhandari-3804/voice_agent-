
def evaluate_transcription(transcript: str, expected_keywords: list) -> dict:
    transcript = transcript.lower()
    score = 0
    matched = []

    for keyword in expected_keywords:
        if keyword.lower() in transcript:
            score += 1
            matched.append(keyword)

    result = "Pass" if score >= len(expected_keywords) * 0.6 else "Fail"
    return {
        "score": score,
        "matched_keywords": matched,
        "total": len(expected_keywords),
        "result": result
    }
