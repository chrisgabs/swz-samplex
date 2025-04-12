# Medical Examination Question Analyzer

This script analyzes multiple JSON files containing medical examination questions and identifies similar questions that appear across different examinations.

## Requirements

- Python 3.6+
- No external packages required (standard library only)

## Usage

1. Place your JSON examination files in the same directory as the script.
2. Run the script:

```bash
python question_analyzer_simple.py exam1.json exam2.json exam3.json
```

Alternatively, if no arguments are provided, the script will automatically look for all JSON files in the current directory.

## Input Format

Each JSON file should contain an array of question objects with the following structure:

```json
{
  "number": 1,
  "question": "Text of the question",
  "choices": {
    "a": "Choice A",
    "b": "Choice B",
    "c": "Choice C",
    "d": "Choice D"
  },
  "answer": "a",
  "section": "Title of the section",
  "reference": "Page number and short note"
}
```

## Output

The script will generate a file named `similar_questions.json` containing groups of similar questions found across the examinations. The output follows this structure:

```json
[
  {
    "number": 1,
    "question": {
      "exam1": "Question from exam1",
      "exam2": "Similar question from exam2"
    },
    "choices": {
      "exam1": {
        "a": "Choice A",
        "b": "Choice B",
        "c": "Choice C",
        "d": "Choice D"
      },
      "exam2": {
        "a": "Choice A",
        "b": "Choice B",
        "c": "Choice C",
        "d": "Choice D"
      }
    },
    "answer": {
      "exam1": "a",
      "exam2": "a"
    },
    "reference": {
      "exam1": {
        "number": 10,
        "section": "Section title",
        "reference": "Page reference"
      },
      "exam2": {
        "number": 15,
        "section": "Section title",
        "reference": "Page reference"
      }
    }
  }
]
```

## How the Similarity Algorithm Works

The script uses a dynamic, multi-faceted approach to determine question similarity, adaptable to any medical specialty or domain:

1. **Key Concept Extraction**: The algorithm first analyzes all questions to identify domain-specific terms that appear frequently. These terms are more likely to represent important concepts in the particular medical specialty.

2. **Text Preprocessing**: Questions and choices are preprocessed by:
   - Converting to lowercase
   - Removing special characters
   - Filtering out common English words

3. **Similarity Calculation**: The algorithm combines multiple similarity metrics:
   - **Sequence Similarity**: Uses Python's `difflib` to measure overall text similarity
   - **Term Overlap**: Computes Jaccard similarity between domain-specific terms
   - **Key Concept Overlap**: Gives additional weight when questions share important domain concepts
   - **Answer Matching**: Questions with the same answer receive a similarity boost
   - **Section Relatedness**: Questions from related sections receive a boost

4. **Adaptive Weighting**: The algorithm applies:
   - Similarity discounts when questions contain different key concepts
   - Similarity boosts when questions share significant key concepts

The system dynamically adapts to any set of medical questions without requiring hard-coded specialty terms or manual configuration. The threshold can be adjusted to control the sensitivity of similarity detection.

## Notes

This script is designed to handle examination questions from any medical specialty or domain. It doesn't rely on hard-coded lists of medical terms, but instead dynamically identifies domain-specific terminology based on the actual contents of your question sets. 