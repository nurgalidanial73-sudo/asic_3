import os
import csv
import json


class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if not os.path.exists(self.filename):
            print(f"Error: {self.filename} not found.")
            return False
        print(f"File found: {self.filename}")
        return True

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")


class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        try:
            with open(self.filename, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.students.append(row)
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

    def preview(self, n=5):
        print("\nFirst 5 rows:")
        print("------------------------------")
        for i in range(n):
            s = self.students[i]
            print(f"{s['student_id']} | {s['age']} | {s['gender']} | {s['country']} | GPA: {s['GPA']}")
        print("------------------------------")


class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        valid = []
        for s in self.students:
            try:
                float(s["final_exam_score"])
                valid.append(s)
            except:
                continue

        top10 = sorted(
            valid,
            key=lambda x: float(x["final_exam_score"]),
            reverse=True
        )[:10]

        self.result = {
            "analysis": "Top 10 Students by Exam Score",
            "total_students": len(self.students),
            "top_10": []
        }

        for i in range(len(top10)):
            s = top10[i]
            self.result["top_10"].append({
                "rank": i + 1,
                "student_id": s["student_id"],
                "country": s["country"],
                "major": s["major"],
                "final_exam_score": float(s["final_exam_score"]),
                "GPA": float(s["GPA"])
            })

        return self.result

    def print_results(self):
        print("\n------------------------------")
        print("Top 10 Students by Exam Score")
        print("------------------------------")

        for s in self.result["top_10"]:
            print(
                f"{s['rank']}. {s['student_id']} | {s['country']} | {s['major']} | "
                f"Score: {s['final_exam_score']} | GPA: {s['GPA']}"
            )

        print("------------------------------")


class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, "w", encoding="utf-8") as f:
                json.dump(self.result, f, indent=4)
            print("Result saved to output/result.json")
        except Exception as e:
            print("Error saving file:", e)


fm = FileManager('students.csv')

if not fm.check_file():
    print("Stopping program.")
    exit()

fm.create_output_folder()

dl = DataLoader('students.csv')
dl.load()
dl.preview()

analyser = DataAnalyser(dl.students)
analyser.analyse()
analyser.print_results()

saver = ResultSaver(analyser.result, 'output/result.json')
saver.save_json()