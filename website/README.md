# Medical Examination Question Analyzer - Web Interface

This is a web interface for visualizing and exploring similar questions identified across different medical examinations.

## Features

- **Interactive Dashboard**: Shows statistics and provides filtering options
- **Question Comparison**: Easily compare similar questions from different exams side by side
- **Search Functionality**: Search across all questions and answers
- **Exam Filters**: Filter questions by specific exams
- **Similarity Analysis**: View automatic analysis of how questions are similar or different
- **Import JSON Data**: Paste your own similar questions JSON data directly in the browser

## Getting Started

### Option 1: Using Python's Built-in HTTP Server

1. Make sure Python 3 is installed on your system
2. Open a terminal/command prompt in this directory
3. Run one of the following commands:
   ```
   python -m http.server 8080
   ```
   or
   ```
   py -3 -m http.server 8080
   ```
4. Open your browser and navigate to [http://localhost:8080](http://localhost:8080)

### Option 2: Using Any Other Web Server

You can use any web server of your choice to serve these static files. Just make sure all the following files are in the same directory:

- `index.html`
- `styles.css`
- `script.js`
- `similar_questions.json`

### Option 3: Direct Opening

You can open `index.html` directly in your browser. However, some browsers may block the JSON loading due to security restrictions. Using a web server (Option 1 or 2) is recommended.

## Usage Guide

### Navigation

- **Dashboard**: View statistics about the similar questions dataset
- **Filters**: Click on an exam button to show only questions from that exam
- **Search**: Use the search box to find specific questions by keyword
- **Question Cards**: Click on a question card to expand it and see full details
- **Similar Questions**: Compare how questions appear across different exams

### Importing Your Own Data

1. Click the "Import JSON Data" button in the dashboard
2. Paste your JSON data in the provided textarea
3. Click "Import Data" to load your data into the application
4. Your imported data will be saved in your browser's localStorage and will persist between sessions

The imported JSON data must follow the same structure as the default similar_questions.json file. The basic structure is:

```json
[
  {
    "number": 1,
    "question": {
      "exam1": "Question from exam1",
      "exam2": "Similar question from exam2"
    },
    "choices": {
      "exam1": { "a": "Choice A", "b": "Choice B", ... },
      "exam2": { "a": "Choice A", "b": "Choice B", ... }
    },
    "answer": {
      "exam1": "a",
      "exam2": "b"
    },
    "reference": {
      "exam1": { "number": 10, "section": "Section title", "reference": "Ref" },
      "exam2": { "number": 15, "section": "Section title", "reference": "Ref" }
    }
  },
  // More question groups...
]
```

To reset to the default data, click "Reset to Default Data" in the import modal.

### Understanding the Interface

- **Question Cards**: Each card represents a group of similar questions across exams
- **Exam Pills**: Colored badges showing which exams the question appears in
- **Correct Answers**: Highlighted in green for easy identification
- **Similarity Analysis**: Shows an automatic analysis of the similarities and differences

## Troubleshooting

If you encounter issues:

1. **JSON Not Loading**: Make sure `similar_questions.json` is in the same directory as the HTML file
2. **Browser Security Blocking**: Use a web server instead of opening the HTML file directly
3. **Display Issues**: Try using a modern browser like Chrome, Firefox, or Edge
4. **Import Errors**: Check that your JSON data follows the correct structure

## Technology Stack

- HTML5
- CSS3 with Tailwind CSS
- Vanilla JavaScript
- LocalStorage for persistence of imported data 