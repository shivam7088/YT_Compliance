import re

# Offline fallback. This does not replace legal advice; it is a demo classifier.
PATTERNS = [
    {
        "category": "Advertisement / Disclosure",
        "severity": "HIGH",
        "patterns": [
            r"\bpaid promotion\b",
            r"\bsponsored\b",
            r"\bpaid partnership\b",
            r"\badvertisement\b",
            r"\bad\b"
        ],
        "message": "The content appears promotional. Check that a clear and conspicuous disclosure is present."
    },
    {
        "category": "Unsupported Claim",
        "severity": "MEDIUM",
        "patterns": [
            r"\bguaranteed\b",
            r"\b100%\s*(effective|safe|guaranteed)\b",
            r"\bcures?\b",
            r"\bmiracle\b",
            r"\bno side effects\b"
        ],
        "message": "The transcript contains a strong claim that may require evidence or qualification."
    },
    {
        "category": "Misleading / Absolute Language",
        "severity": "LOW",
        "patterns": [
            r"\bbest in the world\b",
            r"\bnumber one\b",
            r"\bnever fails\b",
            r"\bzero risk\b"
        ],
        "message": "Absolute marketing language may need supporting evidence."
    }
]

def rule_based_audit(transcript):
    violations = []
    lower = transcript.lower()

    for rule in PATTERNS:
        matched = None
        for pattern in rule["patterns"]:
            match = re.search(pattern, lower)
            if match:
                start = max(0, match.start() - 80)
                end = min(len(transcript), match.end() + 120)
                matched = transcript[start:end].strip()
                break

        if matched:
            violations.append({
                "category": rule["category"],
                "severity": rule["severity"],
                "description": rule["message"],
                "evidence": matched,
                "recommendation": "Review the statement against your official compliance policy."
            })

    return {
        "status": "FAIL" if violations else "PASS",
        "summary": (
            f"{len(violations)} possible compliance issue(s) found."
            if violations
            else "No obvious issues were detected by the offline rules."
        ),
        "violations": violations
    }
