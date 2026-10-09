"""
Gradebook Manager

This program keeps track of students and their exam scores. For each
student it calculates the average score and the letter grade, then prints
a class report ranked from the highest average to the lowest. It finishes
by printing the class-wide average and the name of the top student.

Any score outside the range 0-100 is invalid and should be skipped
(with a warning printed).

Grading scale:
    A: 90 and above
    B: 80 - 89.99
    C: 70 - 79.99
    D: 60 - 69.99
    F: below 60
"""


RECORDS = [
    ("Alice", [92, 88, 95, 90]),
    ("Ben", [75, 82, 79, 85]),
    ("Carmen", [65, 70, 58, 72]),
    ("Dmitri", [88, 91, 84, 105]),
    ("Elena", [55, 61, 48, 59]),
    ("Farah", [81, 85, 80, 84]),
]


class Student:
    """Represents a single student and their list of exam scores."""

    def __init__(self, name, scores=None):
        self.name = name
        self.scores = scores if scores is not None else []

    def add_score(self, score):
        """Add a score to the student's record if it is between 0 and 100."""
        if 0 <= score <= 100:
            self.scores.append(score)
        else:
            print(f"Warning: invalid score {score} for {self.name}, skipping.")

    def average(self):
        """Return the average of the student's scores (0.0 if no scores)."""
        if len(self.scores) == 0:
            return 0.0
        return sum(self.scores) / len(self.scores)

    def letter_grade(self):
        """Return the letter grade that matches the student's average."""
        avg = self.average()
        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.name:<12}{self.average():>8.2f}{self.letter_grade():>8}"


def build_gradebook(records):
    """Create a list of Student objects from (name, scores) records."""
    students = []
    for name, scores in records:
        student = Student(name)
        for score in scores:
            student.add_score(score)
        students.append(student)
    return students


def rank_students(students):
    """Return a new list of students sorted from highest to lowest average."""
    return sorted(students, key=lambda s: s.average(), reverse=True)


def class_average(students):
    """Return the average of all the student averages."""
    if len(students) == 0:
        return 0.0
    total = 0
    for student in students:
        total += student.average()
    return total / len(students)


def top_student(students):
    """Return the student with the highest average."""
    best = students[0]
    for student in students:
        if student.average() > best.average():
            best = student
    return best


def print_report(ranked):
    """Print a formatted table of ranked students."""
    print(f"{'Rank':<6}{'Name':<12}{'Average':>8}{'Grade':>8}")
    print("-" * 34)
    for rank, student in enumerate(ranked, start=1):
        print(f"{rank:<6}{student}")


def main():
    students = build_gradebook(RECORDS)
    ranked = rank_students(students)

    print()
    print_report(ranked)
    print()
    print(f"Class average: {class_average(students):.2f}")

    best = top_student(students)
    print(f"Top student:   {best.name} ({best.average():.2f})")


if __name__ == "__main__":
    main()
