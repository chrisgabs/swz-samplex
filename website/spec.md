# API Specification — Similar Questions Data

## Overview

API for subject batches and similar questions across multiple sources (e.g. exam years). Each question can have variant text, choices, answers, rationales, and references per source.

---

## Data Model

### Root: `Subject[]`

Array of subjects. Each subject contains batches of similar questions.

| Field | Type | Description |
|-------|------|-------------|
| `subject_name` | `string` | Name of the subject (e.g. `"Medicine"`). |
| `batches` | `Batch[]` | List of batches for this subject. |

---

### `Batch`

| Field | Type | Description |
|-------|------|-------------|
| `batch_name` | `string` | Name of the batch. |
| `similar_questions` | `SimilarQuestion[]` | List of similar questions in this batch. |

---

### `SimilarQuestion`

A single logical question with variants keyed by source (e.g. year or source id like `"2021"`, `"2024"`, `"Old"`, `"dough"`).

| Field | Type | Description |
|-------|------|-------------|
| `number` | `integer` | Question number within the batch. |
| `unique` | `boolean` | Whether this question is unique (no variants). |
| `question` | `Record<string, string>` | Question text per source. Keys are source identifiers (e.g. `"2021"`, `"2024"`, `"Old"`). |
| `choices` | `Record<string, ChoiceSet>` | Answer choices per source. Keys are source identifiers. |
| `answer` | `Record<string, string>` | Correct answer letter per source (e.g. `"A"`, `"C"`, `"d"`). |
| `rationale` | `Record<string, string>` | Explanation text per source. |
| `reference` | `Record<string, Reference>` | Citation/source info per source. |

---

### `ChoiceSet`

Multiple-choice options for one source. Keys are option letters.

| Key | Type | Description |
|-----|------|-------------|
| `a` | `string` | Option A text. |
| `b` | `string` | Option B text. |
| `c` | `string` | Option C text. |
| `d` | `string` | Option D text. |

*(Other letters may be used if the API allows more than 4 options.)*

---

### `Reference`

| Field | Type | Description |
|-------|------|-------------|
| `number` | `integer` | Reference or question number in source material. |
| `section` | `string` | Section or topic name (e.g. `"Basic Electrocardiography"`). |
| `reference` | `string` | Page, slide, or location (e.g. `"Page 8"`, `"2 of 2"`). |

---

## Source keys

All per-source objects (`question`, `choices`, `answer`, `rationale`, `reference`) use the same set of keys. Typical keys in the sample:

- `"2020"`, `"2021"`, `"2024"` — exam years
- `"Old"` — legacy/old version
- `"dough"` — another source id

Keys are arbitrary strings; the client should treat them as opaque source identifiers and use them consistently across fields.

---

## Example (minimal)

```json
[
  {
    "subject_name": "Medicine",
    "batches": [
      {
        "batch_name": "Batcheu",
        "similar_questions": [
          {
            "number": 1,
            "unique": false,
            "question": {
              "2021": "What does the pointed arrow represent?",
              "2024": "What does the pointed arrow represent?"
            },
            "choices": {
              "2021": { "a": "...", "b": "...", "c": "...", "d": "..." },
              "2024": { "a": "...", "b": "...", "c": "...", "d": "..." }
            },
            "answer": { "2021": "C", "2024": "A" },
            "rationale": { "2021": "...", "2024": "..." },
            "reference": {
              "2021": { "number": 1, "section": "Basic Electrocardiography", "reference": "Page 8" },
              "2024": { "number": 3, "section": "4.01 Basic Electrocardiology", "reference": "2 of 2" }
            }
          }
        ]
      }
    ]
  }
]
```

---

## Endpoints (suggested)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/subjects` | Return full list of subjects with batches and similar questions (root structure above). |
| `GET` | `/api/subjects?subject={name}` | Return subjects filtered by `subject_name`. |
| `GET` | `/api/subjects/{subjectId}/batches` | Return batches for one subject (if subjects are identified by id). |

Response body for the main listing: `Subject[]` as defined above (JSON).

---

## Notes

- **Answer casing**: Sample data has both `"C"` and `"c"`; clients should compare case-insensitively.
- **Optional fields**: If a source has no variant for a question, that source key may be omitted from `question`, `choices`, `answer`, `rationale`, or `reference`.
- **Placeholders**: Question text may include placeholders like `<image>` for embedded assets.
