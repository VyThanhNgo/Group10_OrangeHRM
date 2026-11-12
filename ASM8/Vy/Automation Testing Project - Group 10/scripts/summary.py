"""In bảng PASSED / FAILED / SKIPPED theo từng thành viên từ reports/results.xml.

Chạy:  python scripts/summary.py   (sau khi đã chạy pytest)
"""
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict
from pathlib import Path

FILE = Path(__file__).resolve().parent.parent / "reports" / "results.xml"

if not FILE.exists():
    print("Chưa có kết quả. Hãy chạy: pytest")
    sys.exit(0)

by_member = OrderedDict()
failed = []
for case in ET.parse(FILE).getroot().iter("testcase"):
    parts = case.get("classname", "").split(".")
    if len(parts) < 2 or parts[0] != "tests":
        continue
    member = parts[1]
    if case.find("failure") is not None or case.find("error") is not None:
        status = "FAILED"
        failed.append(case.get("name"))
    elif case.find("skipped") is not None:
        status = "SKIPPED"
    else:
        status = "PASSED"
    by_member.setdefault(member, {"PASSED": 0, "FAILED": 0, "SKIPPED": 0})[status] += 1

print(f"{'Thành viên':<40}{'PASSED':>8}{'FAILED':>8}{'SKIPPED':>9}")
for member, c in sorted(by_member.items()):
    print(f"{member:<40}{c['PASSED']:>8}{c['FAILED']:>8}{c['SKIPPED']:>9}")

print("\nTest FAILED:")
for name in failed:
    print(" -", name)
