from analyzer.question_analyzer_simple import find_similar_questions, Exam
from parser.parser import Parser
from dotenv import load_dotenv
import os
import json
from pathlib import Path

def get_questions_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
    

def clean_filenames(dir: str):
    for file in os.listdir(dir):
        if file.endswith(".json"):
            if file == "similar_questions.json":
                os.remove(os.path.join(dir, file))
                continue
            new_name = file.split("_")[0]
            os.rename(os.path.join(dir, file), os.path.join(dir, new_name + ".json"))


def main():
    # for dir in os.listdir("./in/Neurology I"):
    #     clean_filenames("./in/Neurology I/" + dir)
    # return
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    parser = Parser(api_key=gemini_api_key)

    batch_name = input("Enter batch name: ")
    get_from_file = input("Get questions from file? (y/n): ")
    get_from_file = get_from_file == "y"

    IN_DIR = "in/" + batch_name + "/"
    OUT_DIR = "out/" + batch_name + "/"
    if not os.path.exists(IN_DIR):
        print(f"Error: Directory {IN_DIR} does not exist.")
        return
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)
        
    exams: list[Exam] = []
    for file in os.listdir(IN_DIR):
        exam = Exam(
            name=Path(file).stem,
            questions=""
        )
        exams.append(exam)

    print(f"Found {len(exams)} exams")
    for exam in exams:
        print(f"- {exam.name}")

    for exam in exams:
        if get_from_file:
            print(f"Processing {exam.name} ... ", end="")
            questions = get_questions_from_file(IN_DIR + exam.name + ".json")
            print(f"DONE")
        else:
            print(f"Processing {exam.name} ... ")
            questions = parser.parse_pdf(
                pdf_path=IN_DIR + exam.name + ".pdf",
                temp_out_dir=OUT_DIR
            )
            print(f"Done parsing {exam.name}")
        exam.questions = questions

    print("Finding similar questions ...")
    similar_questions = find_similar_questions(exams)
    print(f"Found {len(similar_questions)} similar questions")

    with open(OUT_DIR + "similar_questions.json", 'w', encoding='utf-8') as f:
        json.dump(similar_questions, f, indent=2)

    print(f"Analysis complete. Results saved to {OUT_DIR}similar_questions.json")

if __name__ == "__main__":
    main()