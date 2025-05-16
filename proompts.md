I uploaded a PDF file containing multiple choice questions. Please give me all questions structured in the following format:

```
{
  "number": <question number>,
  "question": "<text of the question>",
  "choices": {
    "a": "<choice A>",
    "b": "<choice B>",
    "c": "<choice C>",
    "d": "<choice D>"
  },
  "answer": "<correct choice letter>",
  "section": "<title of the section the question is based on>",
  "reference": "<page number and short note of where in the PDF the answer is found>"
}
```

For cases where the PDF file contains a question with no contents, ignore the question and proceed to the next one.
If there are questions with missing information such as choices, answer, or section, please output the question with the missing information as an empty string.

DO NOT STOP generating until all questions are encoded.
First check how many questions in total there are in the PDF then DO NOT STOP generating until all questions are encoded. ENCODE ALL QUESTIONS IN ONE OUTPUT

After you have encoded all questions, please output "<%DONE%>". Please output only the JSON object. Do not include any other text or comments except for the "<%DONE%>" string.

----------------------------

I have three JSON file containing a list of multiple choice questions following this format:

```
{
  "number": <question number>,
  "question": "<text of the question>",
  "choices": {
    "a": "<choice A>",
    "b": "<choice B>",
    "c": "<choice C>",
    "d": "<choice D>"
  },
  "answer": "<correct choice letter>",
  "section": "<title of the section the question is based on>",
  "reference": "<page number and short note of where in the PDF the answer is found>"
}
```

Each JSON file contains questions to the same examination but from different years. Since these were manually written by different people, the questions are not worded the same 1:1. I want you to create a python script that will process these three sets of questions then check which questions appear on at least two different examinations. Please intelligently determine if the question is similar enough to be considered the same. For context, these questions are from a medical student's examination.

Please evaluate thoroughly your though process in determining how to create the algoirthm to determining the question's similarities.

The output of the program should follow the following structure:

```
{
  "number": <question number>,
  "question": {
    "Examination_A": "<question from examination A>",
    "Examination_B": "<question from examination B>"
  },
  "choices": {
    "Examination_A": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
    "Examination_B": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
  },
  "answer": {
    "Examination_A": "<answer from examination A>",
    "Examination_B": "<answer from examination B>"
  },
  "reference" {
    "Examination_A": {
        "number": <question number of the question from Examination_A>
        "section": "<jtitle of the section the question is based on for Examination_A>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
    "Examination_B": {
        "number": <question number of the question from Examination_B>
        "section": "<title of the section the question is based on for Examination_B>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
  }
}
```

Where the keys of question, choices, answer, and reference attribute refer to the examinations in which the given question was found. If there are cases where the question shows up in all three examinations, there will be another entry Examination_C.

Please note that Examination_C, Examination_B, and Examination_A. Are just placeholders, please use the actual file name of the three examinations as keys.

---------------------- GEMINI 2.0 FLASH-LITE IS TOO DUMB FOR THIS JOB ----------------------

I have multiple PDF files provided all of which contains multiple choice questions. For context these are from a medical student's examination taken by different batches of students. I want to get the questions that are similar across different examinations. Similar in a way that the question may be worded differently but the underlying concept is the same.

The output will be used as a guide for students to study such that they can focus on the most important questions.

The output should be a JSON file with the following structure:

```
{
  "number": <question number>,
  "question": {
    "Examination_A": "<question from examination A>",
    "Examination_B": "<question from examination B>"
  },
  "choices": {
    "Examination_A": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
    "Examination_B": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
  },
  "answer": {
    "Examination_A": "<answer from examination A>",
  },
    "Examination_B": "<answer from examination B>"
  "reference" {
    "Examination_A": {
        "number": <question number of the question from Examination_A>
        "section": "<title of the section the question is based on for Examination_A>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
    "Examination_B": {
        "number": <question number of the question from Examination_B>
        "section": "<title of the section the question is based on for Examination_B>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
  }
}
```

Where the keys of question, choices, answer, and reference attribute refer to the file names in which the given question was found. If there are cases where the question shows up in three examinations, there will be another entry Examination_C. The number of files provided will be arbitrary but will be at least 2. 

Examination_A, Examination_B, and Examination_C are just placeholders, please use the actual file names of the files provided as keys.

Please evaluate thoroughly your though process in determining which questions are similar and which are not, take into consideration the context of the question, choices, and answer.

For cases where there are missing questions, please set the values of "choices" to an empty dictionary. The same goes for the "answer" and "reference" keys.

Compare all questions across all examinations. When you are done, please output "DONE".

--------------------------------

Make me a python script that will take scan through all directories in a given directory and find all files named "similar_questions.json". Get the content of each file and merge them into a single JSON file.

The output should be a JSON file with the following structure:

```
[
  {
    "batch_name": "<name of directory from which the similar_questions.json file was found>",
    "similar_questions": <content of the similar_questions.json file>
  },
  {
    "batch_name": "<name of directory from which the similar_questions.json file was found>",
    "similar_questions": <content of the similar_questions.json file>
  }
  ...
]
```

Please output the JSON file in the same directory as the script with the name "merged_similar_questions_MM:DD:HH:MM.json".

--------------------------------

The current website takes in JSON data that contains a list of objects that follows the following structure:

```
{
  "number": <question number>,
  "question": {
    "Examination_A": "<question from examination A>",
    "Examination_B": "<question from examination B>"
  },
  "choices": {
    "Examination_A": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
    "Examination_B": {
        "a": "<choice A>",
        "b": "<choice B>",
        "c": "<choice C>",
        "d": "<choice D>"
    }
  },
  "answer": {
    "Examination_A": "<answer from examination A>",
    "Examination_B": "<answer from examination B>"
  },
  "reference" {
    "Examination_A": {
        "number": <question number of the question from Examination_A>
        "section": "<jtitle of the section the question is based on for Examination_A>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
    "Examination_B": {
        "number": <question number of the question from Examination_B>
        "section": "<title of the section the question is based on for Examination_B>",
        "reference": "<page number and short note of where in the PDF the answer is found for Examination_B>"
    }
  }
}
```

This data is currently being used to populate the website. I want to change the data structure such that multiple lists of questions are groups together and the user can choose among which group of questions to preview in the website.

I want to change the data structure to the following:

```
{
  "batch_name": "<name of the batch>",
  "similar_questions": <list of similar questions>
}
```

Please make the necessary changes to the website to accommodate the new data structure. The user should be able to choose which batch of questions to preview from the dashboard. Do not change any existing functionality.

--------------------------------

The website at the moment supports filtering questions by examination where the user can select which questions to show depending on the examination selected. So if for example there are three examinations A B and C, the user can select C and it will only show questions that are available in C.

I want you to change the behavior of the website such that by default all examinations are selected and when the user unselects an examination, the questions that are shown are those that are not in the selected examinations. For example, if there are three examinations A B and C, and the user unselects C, then all questions will be shown except for those that are only in C.

Please make the necessary changes to the website to accommodate the new behavior. If there are no examinations selected, appropriately prompt the user to select at least one examination.

--------------------------------

The website currently accepts a JSON file with the following structure:

{
  "batch_name": "<name of the batch>",
  "similar_questions": <list of similar questions>
}

I want to change the website such that the user can upload a JSON file with the following structure:

[
  "subject_name": "<name of the subject>",
  "batches": [
    {
      "batch_name": "<name of the batch>",
      "similar_questions": <list of similar questions>
    },
    ...
  ]
  ...
]

Please adjust the user interface to accommodate the new data structure. Do not change any existing functionality. The user should be able to select which subject to preview from the dashboard, and then select which batch to preview from the subject.

--------------------------------

Can you modify merge_similar_questions.py such that it outputs the following structure:

```
[
  {
    "subject_name": "<name of subject_directory>",
    "batches": [
      {
        "batch_name": "name of batch_directory",
        "similar_questions": [
          // Question objects from the first similar_questions.json file
        ]
      },
      {
        "batch_name": "name of batch_directory2",
        "similar_questions": [
          // Question objects from the second similar_questions.json file
        ]
      }
      ...
    ]
  },
  ...
]
```

The inputted root directory is expected to have such file structure:

```
- root_directory
  - subject_directory
    - batch_directory
      - similar_questions.json
    - batch_directory2
      - similar_questions.json
    ...
  - subject_directory2
    - batch_directory
      - similar_questions.json
    - batch_directory2
      - similar_questions.json
    ...
  ...
```

-----------------------------

The current implementation of main.py asks for a batch name and retrieves all of the pds in the given directory. The exected file structure is the following:

```
- batch_directory
  - exam.pdf
  - exam2.pdf
  ...
```

After processing, the code outputs the same file structure but with the processed exam files as json and with an additional file similar_questions.json inside the batch directory.

Please modify main.py such that instead of taking in a batch directory, it should take in a root directory that follows the following file structure:

```
- root_directory
  - subject_directory
    - batch_directory
      - exam.pdf
      - exam2.pdf
      ...
    - batch_directory2
      - exam.pdf
      - exam2.pdf
      ...
    ...
  - subject_directory2
    - batch_directory
      - exam.pdf
      - exam2.pdf
      ...
    - batch_directory2
      - exam.pdf
      - exam2.pdf
      ...
    ...
  ...
```

The program should first ask the user if it will be processing a root directory or a batch directory. If the indicates a batch directory, then proceed with the existing functionality. But if the user wants to process a root directory then process all subdirectories inside the root directory. The output should follow the root directory's file structure and file names.