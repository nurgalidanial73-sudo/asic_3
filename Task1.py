import os
import csv
import json


class FileChecker:
    def __init__(self, path):
        self.path = path

    def verify(self):
        print("Checking file...")

        if not os.path.exists(self.path):
            print(f"Error: {self.path} not found.")
            return False
        else:
            print(f"File found: {self.path}")
            return True

    def ensure_output_dir(self, dir_name="output"):
        print("Checking output folder...")

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print("Output folder created: output/")
        else:
            print("Output folder already exists: output/")


class CSVReader:
    def __init__(self, path):
        self.path = path
        self.records = []

    def read_data(self):
        print("Loading data...")

        try:
            with open(self.path, encoding="utf-8") as f:
                csv_reader = csv.DictReader(f)
                for item in csv_reader:
                    self.records.append(item)

            print("Data loaded successfully:", len(self.records), "students")
            return self.records

        except FileNotFoundError:
            print(f"Error: File '{self.path}' not found.")
            return []

    def show_preview(self, count=5):
        print("First", count, "rows:")
        print("------------------------------")

        for rec in self.records[:count]:
            print(rec["student_id"], "|", rec["age"], "|", rec["gender"], "|", rec["country"], "| GPA:", rec["GPA"])

        print("------------------------------")


class StatsProcessor:
    def __init__(self, data):
        self.data = data
        self.summary = {}

    def compute(self):
        short_sleep = []
        long_sleep = []

        for rec in self.data:
            try:
                hours = float(rec["sleep_hours"])
                score = float(rec["GPA"])
            except:
                continue

            if hours < 6:
                short_sleep.append(score)
            else:
                long_sleep.append(score)

        avg_short = round(sum(short_sleep) / len(short_sleep), 2)
        avg_long = round(sum(long_sleep) / len(long_sleep), 2)
        gap = round(avg_long - avg_short, 2)

        self.summary = {
            "total_students": len(self.data),
            "low_sleep": {
                "students": len(short_sleep),
                "avg_gpa": avg_short
            },
            "high_sleep": {
                "students": len(long_sleep),
                "avg_gpa": avg_long
            },
            "gpa_difference": gap
        }

        return self.summary

    def display(self):
        print("------------------------------")
        print("Sleep vs GPA Analysis")
        print("------------------------------")

        print("Students sleeping < 6 hours :", self.summary["low_sleep"]["students"])
        print("Average GPA (< 6 hours) :", self.summary["low_sleep"]["avg_gpa"])

        print("Students sleeping >= 6 hours :", self.summary["high_sleep"]["students"])
        print("Average GPA (>= 6 hours) :", self.summary["high_sleep"]["avg_gpa"])

        print("GPA difference :", self.summary["gpa_difference"])
        print("------------------------------")


class JSONWriter:
    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path

    def write(self):
        try:
            with open(self.file_path, "w") as f:
                json.dump(self.data, f, indent=4)

            print("Result saved to output/result.json")

        except Exception as err:
            print("Error saving file:", err)


file_tool = FileChecker("students.csv")

if not file_tool.verify():
    print("Stopping program.")
    exit()

file_tool.ensure_output_dir()

reader = CSVReader("students.csv")
reader.read_data()
reader.show_preview()

processor = StatsProcessor(reader.records)
processor.compute()
processor.display()

writer = JSONWriter(processor.summary, "output/result.json")
writer.write()

reader.read_data = CSVReader("wrong_file.csv").read_data
reader.read_data()