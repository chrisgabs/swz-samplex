from analyzer.question_analyzer_simple import find_similar_questions, Exam
from parser.parser import Parser
from dotenv import load_dotenv
import os
import json
from pathlib import Path


def main():
    load_dotenv()
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    parser = Parser(api_key=gemini_api_key)

    batch_name = input("Enter the batch name: ")

    IN_DIR = "in/"
    OUT_DIR = "out/"

    exams: list[Exam] = []
    for file in os.listdir(IN_DIR):
        exam = Exam(
            name=Path(file).stem,
            questions=""
        )
        exams.append(exam)

    print(f"---- Found {len(exams)} exams ----")
    for exam in exams:
        print(f"--- {exam.name} ---")
    print("--------------------------------")

    for exam in exams:
        print(f"---- Parsing {exam.name} ----")
        questions = parser.parse_pdf(
            pdf_path=IN_DIR + exam.name + ".pdf",
            temp_out_dir=OUT_DIR
        )
        exam.questions = questions

    # TODO: fix find_similar_questions, currently returning []
    similar_questions = find_similar_questions(exams)

    print(f"---- Found {len(similar_questions)} similar questions ----")

    with open(OUT_DIR + batch_name + "_similar_questions.json", 'w', encoding='utf-8') as f:
        json.dump(similar_questions, f, indent=2)

    print("similar_questions.json saved")

if __name__ == "__main__":
    main()