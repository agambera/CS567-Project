BUG REPORT - gradebook.py
=========================

The file gradebook.py contains 5 bugs that prevent correct operation.

BUG 1 - Line 34: Mutable default argument
-----------------------------------------
The default `scores=[]` parameter creates a single list shared across all 
Student instances. This causes all students to share the same scores list.

Fix: Use `scores=None` and initialize with `self.scores = scores if scores is not None else []`

BUG 2 - Line 50: Off-by-one loop error
--------------------------------------
The loop `range(1, len(self.scores))` skips the first score (index 0), 
causing averages to be calculated incorrectly.

Fix: Use `range(len(self.scores))` or `total = sum(self.scores)`

BUG 3 - Lines 59-62: Incorrect conditional order
------------------------------------------------
The letter_grade() function checks 80 after 70, so averages >= 80 return "C" 
instead of "B" since the first matching condition is used.

Fix: Reorder to check 80 before 70:
    elif avg >= 80: return "B"
    elif avg >= 70: return "C"

BUG 4 - Line 85: Wrong sort order
---------------------------------
The rank_students() function sorts in ascending order (lowest first) instead 
of descending (highest first) due to missing `reverse=True`.

Fix: Add `reverse=True` to the sorted() call.

BUG 5 - Line 125: Method referenced as attribute
------------------------------------------------
`best.average` refers to the method object, not its return value. This causes:
TypeError: unsupported format string passed to method.__format__

Fix: Change `best.average` to `best.average()`

TEST RESULTS - gradedbook.py
============================
After applying all 5 fixes, gradedbook.py runs correctly:

Warning: invalid score 105 for Dmitri, skipping.

Rank  Name         Average   Grade
----------------------------------
1     Alice          91.25       A
2     Dmitri         87.67       B
3     Farah          82.50       B
4     Ben            80.25       B
5     Carmen         66.25       D
6     Elena          55.75       F

Class average: 77.28
Top student:   Alice (91.25)

All bugs have been fixed and the program produces the expected output.
