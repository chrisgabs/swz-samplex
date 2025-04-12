# Medical Examination Question Analyzer - Python Scripts

This directory contains Python scripts for analyzing medical examination questions and identifying similar questions across different exams.

## Scripts

- `question_analyzer.py` - The main, more feature-rich script
- `question_analyzer_simple.py` - A simplified version with core functionality

## Requirements

- Python 3.6+
- No external packages required (standard library only)

## Usage

1. Place your JSON examination files in this directory
2. Run the script:

```bash
python question_analyzer_simple.py sample_exam1.json sample_exam2.json sample_exam3.json
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

The script generates a file named `similar_questions.json` containing groups of similar questions found across the examinations. The output follows this structure:

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

1. **Key Concept Extraction**: Identifies domain-specific terms that appear frequently
2. **Text Preprocessing**: Converts to lowercase, removes special characters, filters out common words
3. **Similarity Calculation**: Combines multiple metrics (sequence similarity, term overlap, key concept overlap)
4. **Adaptive Weighting**: Applies similarity discounts/boosts based on key concepts

The system dynamically adapts to any set of medical questions without requiring hard-coded specialty terms or manual configuration. 