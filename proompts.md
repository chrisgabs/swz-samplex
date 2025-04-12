I uploaded a PDF file containing multiple choice questions. Please give me the first 5 questions structured in the following format:

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

Where the keys of question, choices, answer, and reference attribute refer to the examinations in which the given question was found. If there are cases where the question shows up in all three examinations, there will be another entry Examination_C.

Please note that Examination_C, Examination_B, and Examination_A. Are just placeholders, please use the actual file name of the three examinations as keys.