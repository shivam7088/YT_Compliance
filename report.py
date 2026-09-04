from datetime import datetime
import json
from pathlib import Path

def print_report(result):
    print("\n" + "=" * 60)
    print("              COMPLIANCE REPORT")
    print("=" * 60)
    print(f"Status : {result.get('status', 'UNKNOWN')}")
    print(f"Summary: {result.get('summary', '')}")

    violations = result.get("violations", [])
    print(f"\nPossible violations: {len(violations)}")

    for i, item in enumerate(violations, 1):
        print(f"\n{i}. [{item.get('severity')}] {item.get('category')}")
        print(f"   Problem : {item.get('description')}")
        print(f"   Evidence: {item.get('evidence')}")
        print(f"   Fix     : {item.get('recommendation')}")

def save_report(result):
    Path("reports").mkdir(exist_ok=True)
    filename = datetime.now().strftime("reports/report_%Y%m%d_%H%M%S.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return filename
