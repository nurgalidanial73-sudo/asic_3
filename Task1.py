import os
import csv
import json

print("Checking file...")

if not os.path.exists("students.csv"):
    print("Error: students.csv not found. Please download the file from LMS.")
    exit()

print("File found: students.csv")

print("Checking output folder...")

if not os.path.exists("output"):
    os.makedirs("output")
    print("Output folder created: output/")
else:
    print("Output folder exists")

students = []

with open("students.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        students.append(row)

print("\nTotal students:", len(students))

print("\nFirst 5 rows:")
print("------------------------------")

for i in range(5):
    s = students[i]
    print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")

print("------------------------------")

top10 = sorted(
    students,
    key=lambda x: float(x["final_exam_score"]),
    reverse=True
)[:10]

print("\n------------------------------")
print("Top 10 Students by Exam Score")
print("------------------------------")

for i in range(len(top10)):
    s = top10[i]
    print(
        f"{i+1}. {s['student_id']} | {s['country']} | {s['major']} | "
        f"Score: {s['final_exam_score']} | GPA: {s['GPA']}"
    )

print("------------------------------")

result = {
    "analysis": "Top 10 Students by Exam Score",
    "total_students": len(students),
    "top_10": []
}

for i in range(len(top10)):
    s = top10[i]
    result["top_10"].append({
        "rank": i + 1,
        "student_id": s["student_id"],
        "country": s["country"],
        "major": s["major"],
        "final_exam_score": float(s["final_exam_score"]),
        "GPA": float(s["GPA"])
    })

with open("output/result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4)

print("\n==============================")
print("ANALYSIS RESULT")
print("==============================")
print("Analysis : Top 10 Students by Exam Score")
print("Total students :", len(students))
print("Top 10 saved to output/result.json")
print("==============================")

print("\nResult saved to output/result.json")