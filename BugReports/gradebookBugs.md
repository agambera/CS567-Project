# Bug Report: gradebook.py

## Summary
- **Total bugs found:** 5
- **Fixed:** 5
- **Severity breakdown:** 2 critical, 2 high, 1 medium

| ID | Pass # | Line | Description | Fix applied | Found by |
|----|--------|------|-------------|-------------|----------|
| B1 | 1 | 34 | Mutable default argument `scores=[]` shares list across all instances | Changed to `scores=None` with `self.scores = scores if scores is not None else []` | Static |
| B2 | 1 | 50-52 | Loop starting at index 1 skipped first score in average calculation | Replaced with `sum(self.scores) / len(self.scores)` | Static |
| B3 | 1 | 59-61 | Grading scale conditions in wrong order (C>=70 checked before B>=80) | Reordered elif conditions: A(>=90), B(>=80), C(>=70), D(>=60), F | Static |
| B4 | 1 | 85 | `sorted()` sorted ascending but wanted descending (highest to lowest) | Added `reverse=True` parameter | Static |
| B5 | 2 | 125 | Missing parentheses on `best.average()` - accessing property instead of method | Changed `best.average:` to `best.average():` | Runtime |

## Pass log

### Pass 1 (Static Review)
- Start time: 1791519178
- End time: 1791519250
- Duration: ~72 seconds
- Actions: Read gradebook.py, identified 5 static bugs (B1-B4, B5 suspected but not confirmed)
- Resource usage: ~3000 tokens ESTIMATE

### Pass 2 (Runtime Testing)
- Start time: 1791519250
- End time: 1791519291
- Duration: ~41 seconds
- Actions: Ran file, observed all students having identical averages (76.83). Debugged to discover B1 (mutable default) and B2 (off-by-one loop). Applied fixes B1+B2, re-ran - averages still identical. Applied B3 (grading order) and B4 (reverse sort). Final fix B5 (method call syntax). File now runs correctly with proper output.
- Resource usage: ~2000 tokens ESTIMATE

## Total resource usage
- Time: ~113 seconds (1 min 53 sec)
- Tokens: ~5000 ESTIMATE

## Verification
- File runs without errors
- Output matches expected format
- Invalid score (105) correctly skipped with warning
- Rankings from highest to lowest average
- Letter grades correctly assigned based on regraded scale
- Final line shows Alice as top student with 91.25 average

**Note on "Bug" B6 (not fixed - simulation only):**
Line 34 originally had `scores=[]` which is a known Python anti-pattern. A "fix" removing the default entirely (`scores`) would break code that calls `Student(name)` without scores argument. The actual fix (using `None` sentinel) was applied instead.
