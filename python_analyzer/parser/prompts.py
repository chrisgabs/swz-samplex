STRUCTURED_OUTPUT_PROMPT = """
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
return response in JSON format [{}] and do not respond in md format.
"""

CONTINUE_PROMPT = """
Please proceed with the remaining questions.
"""

STOP_WORD = "<%DONE%>"