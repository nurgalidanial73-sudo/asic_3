import os
import csv
import json


class FileTool:
    def __init__(self, path):
        self.path = path

    def exists(self):
        if os.path.exists(self.path):
            print(f"Found: {self.path}")
            return True
        print(f"Missing file: {self.path}")
        return False

    def make_dir(self, folder="output"):
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        else:
            print(f"Folder exists: {folder}")


class Loader:
    def __init__(self, path):
        self.path = path

    def read(self):
        try:
            with open(self.path, encoding="utf-8") as f:
                data = list(csv.DictReader(f))
            print(f"Loaded: {len(data)} rows")
            return data
        except Exception as e:
            print(f"Load error: {e}")
            return []

    def show(self, data, n=5):
        print("-" * 30)
        for row in data[:n]:
            print(row)
        print("-" * 30)


class Analyzer:
    def __init__(self, data):
        self.data = data

    def top_students(self):
        clean = []

        for x in self.data:
            try:
                x["final_exam_score"] = float(x["final_exam_score"])
                x["GPA"] = float(x["GPA"])
                clean.append(x)
            except:
                continue

        best = sorted(clean, key=lambda x: x["final_exam_score"], reverse=True)[:10]

        result = []
        for i, x in enumerate(best, 1):
            result.append({
                "rank": i,
                "id": x["student_id"],
                "score": x["final_exam_score"],
                "GPA": x["GPA"]
            })

        return {
            "total": len(self.data),
            "top": result
        }

    def extra(self):
        try:
            high = list(filter(lambda x: float(x["final_exam_score"]) > 95, self.data))
            gpas = list(map(lambda x: float(x["GPA"]), self.data))
            print(f">95 score: {len(high)}")
            print(f"GPA sample: {gpas[:5]}")
        except:
            print("Data error")


def save(data, path):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"Saved: {path}")
    except Exception as e:
        print(f"Save error: {e}")


def run():
    file_path = "students.csv"
    out_path = "output/result.json"

    tool = FileTool(file_path)

    if not tool.exists():
        return

    tool.make_dir()

    loader = Loader(file_path)
    students = loader.read()
    loader.show(students)

    analyzer = Analyzer(students)
    res = analyzer.top_students()
    print(res)

    analyzer.extra()
    save(res, out_path)


run()