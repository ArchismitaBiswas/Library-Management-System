import sqlite3
import pandas as pd
import random
from datetime import datetime, timedelta
import os

os.makedirs("database", exist_ok=True)
os.makedirs("reports", exist_ok=True)

conn = sqlite3.connect("database/library.db")
cursor = conn.cursor()

# =========================
# CREATE TABLES
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books(
    BookID INTEGER PRIMARY KEY,
    Title TEXT,
    Author TEXT,
    Category TEXT,
    AvailableCopies INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students(
    StudentID INTEGER PRIMARY KEY,
    StudentName TEXT,
    Course TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS IssueRecords(
    IssueID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    BookID INTEGER,
    IssueDate TEXT,
    ReturnDate TEXT,
    Status TEXT
)
""")

# =========================
# INSERT BOOKS
# =========================

categories = [
    "Programming",
    "Science",
    "Mathematics",
    "History",
    "Literature"
]

books = []

for i in range(1, 101):
    books.append(
        (
            i,
            f"Book {i}",
            f"Author {i}",
            random.choice(categories),
            random.randint(1, 10)
        )
    )

cursor.executemany("""
INSERT OR IGNORE INTO Books
VALUES (?, ?, ?, ?, ?)
""", books)

# =========================
# INSERT STUDENTS
# =========================

courses = [
    "BCA",
    "BTech",
    "BSc",
    "MCA"
]

students = []

for i in range(1, 51):
    students.append(
        (
            i,
            f"Student {i}",
            random.choice(courses)
        )
    )

cursor.executemany("""
INSERT OR IGNORE INTO Students
VALUES (?, ?, ?)
""", students)

# =========================
# ISSUE RECORDS
# =========================

records = []

for i in range(1, 201):

    issue_date = datetime(2025, 1, 1) + timedelta(
        days=random.randint(0, 180)
    )

    status = random.choice(
        ["Issued", "Returned"]
    )

    return_date = ""

    if status == "Returned":
        return_date = (
            issue_date +
            timedelta(days=random.randint(1, 15))
        ).strftime("%Y-%m-%d")

    records.append(
        (
            i,
            random.randint(1, 50),
            random.randint(1, 100),
            issue_date.strftime("%Y-%m-%d"),
            return_date,
            status
        )
    )

cursor.executemany("""
INSERT OR IGNORE INTO IssueRecords
VALUES (?, ?, ?, ?, ?, ?)
""", records)

conn.commit()

# =========================
# ANALYSIS
# =========================

books_df = pd.read_sql(
    "SELECT * FROM Books",
    conn
)

students_df = pd.read_sql(
    "SELECT * FROM Students",
    conn
)

issue_df = pd.read_sql(
    "SELECT * FROM IssueRecords",
    conn
)

print("\n===== LIBRARY MANAGEMENT SYSTEM =====\n")

print("Total Books:", len(books_df))

print("Total Students:", len(students_df))

print("Total Issue Records:", len(issue_df))

print("\nBOOK SEARCH EXAMPLE")

search_book = pd.read_sql("""
SELECT * FROM Books
WHERE Title = 'Book 10'
""", conn)

print(search_book.to_string(index=False))



issued_books = issue_df[
    issue_df["Status"] == "Issued"
]

returned_books = issue_df[
    issue_df["Status"] == "Returned"
]

print("Currently Issued Books:", len(issued_books))

print("Returned Books:", len(returned_books))

print("\nISSUED BOOKS SAMPLE")

print(
    issue_df[
        issue_df["Status"] == "Issued"
    ].head().to_string(index=False)
)

# =========================
# REPORT
# =========================

with open(
    "reports/library_report.txt",
    "w",
    encoding="utf-8"
) as report:

    report.write(
        "LIBRARY MANAGEMENT REPORT\n\n"
    )

    report.write(
        f"Total Books: {len(books_df)}\n"
    )

    report.write(
        f"Total Students: {len(students_df)}\n"
    )

    report.write(
        f"Total Issue Records: {len(issue_df)}\n"
    )

    report.write(
        f"Currently Issued Books: {len(issued_books)}\n"
    )

    report.write(
        f"Returned Books: {len(returned_books)}\n"
    )

print("\nReport Generated Successfully!")

conn.close()


books_df.to_csv(
    "reports/books_table.csv",
    index=False
)

students_df.to_csv(
    "reports/students_table.csv",
    index=False
)

issue_df.to_csv(
    "reports/issue_records_table.csv",
    index=False
)