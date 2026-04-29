import os
import csv

def check_files():
    print("Checking file...")
    if not os.path.exists("students.csv"):
        print("Error: students.csv not found.")
        return False
    print("File found: students.csv")

    print("Checking output folder...")
    if not os.path.exists("output"):
        os.makedirs("output")
        print("Output folder created: output/")
    else:
        print("Output folder already exists: output/")
    return True


def load_data(filename):
    print("Loading data...")
    try:
        students = []
        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(row)
        print(f"Data loaded successfully: {len(students)} students")
        return students
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Please check the filename.")
        return []
    except Exception as e:
        print("Error:", e)
        return []


def preview_data(students, n=5):
    print(f"\nFirst {n} rows:")
    print("------------------------------")
    for i in range(n):
        s = students[i]
        print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
    print("------------------------------")


def get_top_students(students, n=10):
    valid_students = []
    for s in students:
        try:
            float(s["final_exam_score"])
            valid_students.append(s)
        except ValueError:
            print(f"Warning: could not convert value for student {s['student_id']} — skipping row.")
            continue

    sorted_students = sorted(
        valid_students,
        key=lambda x: float(x["final_exam_score"]),
        reverse=True
    )
    return sorted_students[:n]


def print_top(students, title):
    print("\n------------------------------")
    print(title)
    print("------------------------------")
    for i in range(len(students)):
        s = students[i]
        print(
            f"{i+1}. {s['student_id']} | {s['country']} | {s['major']} | "
            f"Score: {s['final_exam_score']} | GPA: {s['GPA']}"
        )
    print("------------------------------")


def lambda_map_filter(students):
    print("\n------------------------------")
    print("Lambda / Map / Filter")
    print("------------------------------")

    top_scorers = list(filter(lambda s: float(s['final_exam_score']) > 95, students))
    print("Students with score > 95 :", len(top_scorers))

    gpa_values = list(map(lambda s: float(s['GPA']), students))
    print("GPA values (first 5) :", gpa_values[:5])

    good_assignments = list(filter(lambda s: float(s['assignment_score']) > 90, students))
    print("Students assignment > 90 :", len(good_assignments))

    print("------------------------------")


if check_files():
    students = load_data("students.csv")

    if students:
        preview_data(students)

        top10 = get_top_students(students)
        print_top(top10, "Top 10 Students by Exam Score")

        top5 = get_top_students(students, 5)
        print_top(top5, "Top 5 Students by Exam Score")

        lambda_map_filter(students)

        load_data("wrong_file.csv")