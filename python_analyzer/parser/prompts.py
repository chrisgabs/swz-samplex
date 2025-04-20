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

MOCK_RESPONSE_SHORT = """
```json
[
  {
    "number": 64,
    "question": "A 68-year old male hypertensive and diabetic patient was brought to the emergency room for sudden onset right-sided weakness and slurring of speech. What is the initial imaging modality of choice for this patient?",
    "choices": {
      "a": "Cranial ultrasound",
      "b": "Plain and contrast cranial MRI",
      "c": "Plain cranial MRI",
      "d": "Plain cranial CT scan"
    },
    "answer": "D",
    "section": "",
    "reference": "12"
  },
  {
    "number": 65,
    "question": "A 68-year old male hypertensive and diabetic patient was brought to the emergency room for sudden onset right-sided weakness and slurring of speech. What is the initial imaging modality of choice for this patient?",
    "choices": {
      "a": "Cranial ultrasound",
      "b": "Plain and contrast cranial MRI",
      "c": "Plain cranial MRI",
      "d": "Plain cranial CT scan"
    },
    "answer": "D",
    "section": "",
    "hatdog": "12"
  },
  {
    "n
"""

MOCK_RESPONSE = """
```json
[
  {
    "number": 1,
    "question": "What is the normal extracellular H concentration in nanomol/L",
    "choices": {
      "a": "10",
      "b": "20",
      "c": "30",
      "d": "40"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "1"
  },
  {
    "number": 2,
    "question": "What is the most important extracellular buffer?",
    "choices": {
      "a": "HPO4 + Η H2PO4",
      "b": "H + H HHb",
      "c": "H + HCO3. H2CO3",
      "d": "NaOH + NaH2PO4 Na2HPO4 + H20"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "1"
  },
  {
    "number": 3,
    "question": "The measured HCO3 is 28 and computed HCO3 is 20. What is the next step in the evaluation of ABG with these HCO3 values?",
    "choices": {
      "a": "Repeat ABG analysis",
      "b": "Get serum Na and K",
      "c": "Compute for anion gap",
      "d": "Compute for delta gap"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "1"
  },
  {
    "number": 4,
    "question": "What is the computed HCO3 (in meqs) with the following values? pH = 7.2 PCO2 = 30 mmHg",
    "choices": {
      "a": "8",
      "b": "10",
      "c": "12",
      "d": "14"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "1"
  },
  {
    "number": 5,
    "question": "What is the primary acid base disturbance given the following ABG values? pH: 7.30 paCO2: 40mmHg HCO3: 18 mEq/L PO2: 92mmHg O2 Saturation: 95%",
    "choices": {
      "a": "Metabolic Acidosis",
      "b": "Metabolic Alkalosis",
      "c": "Respiratory Acidosis",
      "d": "Respiratory Alkalosis"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "1"
  },
  {
    "number": 6,
    "question": "What is the primary acid base disturbance given the following ABG values? pH: 7.48 paCO2: 35 mmHg HCO3: 32 mEq/L PO2: 92 mmHg O2 Saturation: 98%",
    "choices": {
      "a": "Metabolic Acidosis",
      "b": "Metabolic Alkalosis",
      "c": "Respiratory Acidosis",
      "d": "Respiratory Alkalosis"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 7,
    "question": "Provide the primary disturbance based on the given values: pH: 7.30 paCO2: 55 mmHg HCO3: 27 mEq/L PO2: 92 mmHg O2 Saturation: 98%",
    "choices": {
      "a": "Metabolic Acidosis",
      "b": "Metabolic Alkalosis",
      "c": "Respiratory Acidosis",
      "d": "Respiratory Alkalosis"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 8,
    "question": "Compute for the anion gap (mEq/L) given the following laboratory values: pH: 7.38 paCO2: 50 mmHg HCO3: 30 mEq/L Na: 140 mEq/L PO2: 88 mmhg Albumin: 4.0 g/dL K: 4.5 mEq/L CI: 100 mEq/L",
    "choices": {
      "a": "8",
      "b": "10",
      "c": "12",
      "d": "14"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 9,
    "question": "What is the primary acid base disturbance? For numbers 9 – 11, refer to the following ABG result: pH  7.38 PaCO2  50 mmHg HCO3  30 mEqs/L Na  140mEq/L PO2  88 mmHg Albumin 4.6 g/dL K 3.5 mEq/L CI 100 mEq/L",
    "choices": {
      "a": "Metabolic acidosis",
      "b": "Metabolic alkalosis",
      "c": "Respiratory alkalosis",
      "d": "Respiratory acidosis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 10,
    "question": "What is the expected compensation?",
    "choices": {
      "a": "HCO3 = 26",
      "b": "HCO3 = 20",
      "c": "HCO3 = 45",
      "d": "HCO3 = 50"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 11,
    "question": "What is the correct ABG interpretation?",
    "choices": {
      "a": "Metabolic alkalosis with respiratory alkalosis",
      "b": "Respiratory acidosis with metabolic alkalosis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "2"
  },
  {
    "number": 12,
    "question": "What is the primary acid base disturbance? For numbers 12 – 17, refer to the following ABG and laboratory values: pH 7.50 PaCO2 30 mmHg HCO3 25 meqs/L Na 142 mEq/L PO2 94 mmHg Albumin 4.6 g/dL K 5.0 mEq/L Cl 100 mEq/L",
    "choices": {
      "a": "Metabolic acidosis",
      "b": "Metabolic alkalosis",
      "c": "Respiratory alkalosis",
      "d": "Respiratory acidosis"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 13,
    "question": "What is the expected compensation if the presented disease is acute?",
    "choices": {
      "a": "HCO3 = 22",
      "b": "HCO3 = 19",
      "c": "PACO2 = 39",
      "d": "PACO2 = 25"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 14,
    "question": "Compute the anion gap (mEq/L)",
    "choices": {
      "a": "10",
      "b": "12",
      "c": "15",
      "d": "17"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 15,
    "question": "What is the correct ABG interpretation",
    "choices": {
      "a": "Metabolic Acidosis with Respiratory Alkalosis with High Anion Gap Acidosis (HAGMA)",
      "b": "Metabolic Alkalosis withRespiratory Alkalosis with Non Gap acidosis",
      "c": "Respiratory Acidosis with Metabolic Alkalosis with non gap acidosis",
      "d": "Respiratory Alkalosis with Metabolic Alkalosis with HAGMA"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 16,
    "question": "What is the delta gap?",
    "choices": {
      "a": "3",
      "b": "7",
      "c": "13",
      "d": "18"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 17,
    "question": "What is delta HCO3?",
    "choices": {
      "a": "1",
      "b": "5",
      "c": "7",
      "d": "9"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "3"
  },
  {
    "number": 18,
    "question": "What is the primary disturbance?  For numbers 18-20, refer to the ABG and laboratory results below: pH 7.28 PaCO2 35 mmHg HCO3 16 meqs/L Na 138 mEq/L PO2 95 mmHg Albumin 2.5 g/dL K 4.5 mEq/L Cl 108 mEq/L",
    "choices": {
      "a": "Metabolic Acidosis",
      "b": "Metabolic Alkalosis",
      "c": "Respiratory Acidosis",
      "d": "Respiratory Alkalosis"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "4"
  },
  {
    "number": 19,
    "question": "What is the computed anion gap?",
    "choices": {
      "a": "9",
      "b": "12",
      "c": "14",
      "d": "16"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "4"
  },
  {
    "number": 20,
    "question": "What is the correct ABG interpretation?",
    "choices": {
      "a": "Metabolic Acidosis with Respiratory Acidosis",
      "b": "Respiratory Acidosis with metabolic alkalosis",
      "c": "Simple metabolic acidosis",
      "d": "Respiratory Alkalosis with Metabolic Alkalosis"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "4"
  },
  {
    "number": 21,
    "question": "Which of the following is an accurate description of GALS screening tool?",
    "choices": {
      "a": "Has a good specificity in detecting musculoskeletal abnormalities",
      "b": "Movements include those that become painful last",
      "c": "Not specific for muscles and joints",
      "d": "Subjective method to screen for functional disability"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "4"
  },
  {
    "number": 22,
    "question": "A baseball player consulted due to pain and limitation of the right shoulder after an intense game. On PE, he was unable to bring his abducted arm down slowly from a 90° position. What structure is likely injured?",
    "choices": {
      "a": "Acromioclavicular joint",
      "b": "Bicipital tendon",
      "c": "Coracoacromial ligament",
      "d": "Rotator cuff"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "4"
  },
  {
    "number": 23,
    "question": "Applying resistance to what patient motion will support a diagnosis of bicipital tendinitis?",
    "choices": {
      "a": "Abduction of the shoulder",
      "b": "Extension of the shoulder",
      "c": "Pronation of the forearm",
      "d": "Supination of the forearm"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "5"
  },
  {
    "number": 24,
    "question": "With the patient supine and hips and knees flexed to 90 degrees, the examiner draws the tibia forward with note of significant forward movement from under the femur. Which ligament is most likely injured?",
    "choices": {
      "a": "Medial Collateral Ligament",
      "b": "Anterior Cruciate Ligament",
      "c": "Posterior Cruciate Ligament",
      "d": "Lateral Collateral Ligament"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "5"
  },
  {
    "number": 25,
    "question": "Where should the tape measure be placed from the anterior superior iliac spine to measure the patient's leg length?",
    "choices": {
      "a": "Cross the knee on the lateral side to the lateral malleolus",
      "b": "Cross the knee on the lateral side to the medial malleolus",
      "c": "Cross the knee on the lateral side to the medial malleolus",
      "d": "Cross the knee on the medial side to the medial malleolus"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "5"
  },
  {
    "number": 26,
    "question": "A young woman slips and lands on an everted ankle, resulting in pain and swelling. Ankle radiographs shows only soft tissue swelling but no fracture. Which structure was most likely injured?",
    "choices": {
      "a": "Anterior talofibular ligament",
      "b": "Calcaneofibular ligament",
      "c": "Deltoid ligament",
      "d": "Posterior talofibular ligament"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "5"
  },
  {
    "number": 27,
    "question": "Which motion is tested in the final 30° when a patient is asked to abduct the arms to a vertical position above the head with palms facing each other?",
    "choices": {
      "a": "Pure axioscapular",
      "b": "Pure glenohumeral",
      "c": "Pure scapulothoracic",
      "d": "Combined glenohumeral and scapulothoracic"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "5"
  },
  {
    "number": 28,
    "question": "A patient complains of pain and stiffness of the hand and knee joints in the morning, at rest and with use. What kind of pain is she most likely suffering from?",
    "choices": {
      "a": "Inflammatory joint pain",
      "b": "Mechanical joint pain",
      "c": "Referred pain joint pain",
      "d": "Neuropathic"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "6"
  },
  {
    "number": 29,
    "question": "A security guard consults for severe foot pain with the first steps upon arising in the morning which improves as he continues to bear weight. On PE, there are no signs of inflammation. What is the most likely condition?",
    "choices": {
      "a": "Ankle sprain",
      "b": "Gouty arthritis",
      "c": "Osteoarthritis",
      "d": "Plantar fasciitis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "6"
  },
  {
    "number": 30,
    "question": "On inspection, a patient's hands had bony deformities on the distal and proximal interphalangeal joints. What is the likely diagnosis in this case?",
    "choices": {
      "a": "Ganglion cyst",
      "b": "Osteoarthritis",
      "c": "Rheumatoid arthritis",
      "d": "Synovitis"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "6"
  },
  {
    "number": 31,
    "question": "Which arthritis is LEAST likely to affect the distal interphalangeal (DIP) joint of the hands?",
    "choices": {
      "a": "Osteoarthritis",
      "b": "Pseudogout",
      "c": "Psoriatic arthritis",
      "d": "Rheumatoid arthritis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "6"
  },
  {
    "number": 32,
    "question": "A middle-aged lady tends to her garden almost daily. She consults for elbow pain that is worst on repetitive wrist flexion and pronation. What is she most likely suffering from?",
    "choices": {
      "a": "Golfer's elbow",
      "b": "Olecranon bursitis",
      "c": "Tennis elbow",
      "d": "Ulnar nerve impingement"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "6"
  },
  {
    "number": 33,
    "question": "On inspection, a patient's hand had prominent hypothenar atrophy. What is the most likely diagnosis?",
    "choices": {
      "a": "Carpal Tunnel Syndrome",
      "b": "Colles' Fracture",
      "c": "Dupuytren's contracture",
      "d": "Ulnar Nerve Compression"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "7"
  },
  {
    "number": 34,
    "question": "Which maneuver involves \"milking\" the suprapatellar pouch downward and can best detect the presence of minor knee effusions?",
    "choices": {
      "a": "Balloon sign",
      "b": "Balloting the patella",
      "c": "Bulge sign",
      "d": "Patellar sign"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "7"
  },
  {
    "number": 35,
    "question": "An elderly patient complains of back pain and rest at night. What kind of pain is she most likely suffering from?",
    "choices": {
      "a": "Bone",
      "b": "Osteoarthritic",
      "c": "Mechanical",
      "d": "Neuropathic"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "7"
  },
  {
    "number": 36,
    "question": "In the background of median nerve hypalgesia, which special maneuver correlates best with a nerve conduction diagnosis of Carpal Tunnel Syndrome?",
    "choices": {
      "a": "Phalen's sign",
      "b": "Tinel's sign",
      "c": "Thumb adduction",
      "d": "Thumb abduction"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "7"
  },
  {
    "number": 37,
    "question": "A patient complains of elbow pain on repetitive extension of the wrist and supination against resistance. Which structure is most likely affected?",
    "choices": {
      "a": "Medial epicondyle",
      "b": "Lateral epicondyle",
      "c": "Olecranon bursa",
      "d": "Synovial cavity"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "8"
  },
  {
    "number": 38,
    "question": "What joint is tested when an examiner asks the patient to \"Point your foot toward the floor then toward the ceiling\"?",
    "choices": {
      "a": "Calcaneofibular",
      "b": "Talocalcaneal",
      "c": "Tibiofibular",
      "d": "Tibiotalar"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "8"
  },
  {
    "number": 39,
    "question": "With the patient supine and knees slightly flexed, an examiner pulls laterally against his knee while pushing medially at the ankle to apply varus stress on the knee joint. Which ligament is the examiner checking for laxity and partial tear?",
    "choices": {
      "a": "ACL",
      "b": "PCL",
      "c": "MCL",
      "d": "LCL"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "8"
  },
  {
    "number": 40,
    "question": "What test is performed to check for inflammation or arthritis of the acromioclavicular joint?",
    "choices": {
      "a": "Apley scratch",
      "b": "Crossover test",
      "c": "Drop-Arm Sign",
      "d": "Empty can"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 41,
    "question": "A patient that complains of difficulty in standing from sitting position and difficulty climbing the stairs most likely has which of the following condition?",
    "choices": {
      "a": "Distal muscle weakness",
      "b": "Knee osteoarthritis",
      "c": "Polio",
      "d": "Proximal muscle weakness"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 42,
    "question": "Which of the following cardinal PE technique is NOT performed in the musculoskeletal examination?",
    "choices": {
      "a": "Inspection",
      "b": "Palpation",
      "c": "Percussion",
      "d": "Range of motion"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 43,
    "question": "In a patient with knee osteoarthritis, pain in which activity is considered mechanical in nature?",
    "choices": {
      "a": "Climbing Stairs",
      "b": "Crossing the leg",
      "c": "Prolonged sitting",
      "d": "Standing after prolonged sitting"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 44,
    "question": "Impingement syndrome is associated with?",
    "choices": {
      "a": "Bone",
      "b": "Joint",
      "c": "Bursae",
      "d": "Tendon"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 45,
    "question": "What type of arthritis affects 4 or fewer joints?",
    "choices": {
      "a": "Endarticular",
      "b": "Monoarticular",
      "c": "Oligoarticular",
      "d": "Polyarticular"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 46,
    "question": "In assessing musculoskeletal disorders, what should be the first consideration?",
    "choices": {
      "a": "The most common",
      "b": "The most mild",
      "c": "The most severe",
      "d": "The least common"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "9"
  },
  {
    "number": 47,
    "question": "In evaluation of musculoskeletal condition, determining if it is articular or non-articular is knowing which of the flowing aspect?",
    "choices": {
      "a": "Anatomic localization",
      "b": "Extent of involvement",
      "c": "Pathologic process",
      "d": "Pathogenesis"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 48,
    "question": "What is the best diagnostic procedure to determine if the articular condition is inflammatory or non-inflammatory?",
    "choices": {
      "a": "CBC",
      "b": "ESR",
      "c": "Synovial fluid analysis",
      "d": "Xray"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 49,
    "question": "Which of the following most likely indicates inflammation in a joint?",
    "choices": {
      "a": "Limitation of motion",
      "b": "Pain",
      "c": "Stiffness",
      "d": "Tenderness"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 50,
    "question": "Which of the following has articular involvement?",
    "choices": {
      "a": "Cellulitis",
      "b": "Bursitis",
      "c": "Fasciitis",
      "d": "Synovitis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 51,
    "question": "What is the best patient position to examine the spine?",
    "choices": {
      "a": "Sitting",
      "b": "Standing",
      "c": "Supine",
      "d": "Walking"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 52,
    "question": "A young female is diagnosed with rheumatoid arthritis as she presented with chronic synovitis of more than 4 joint areas. What is the usual manner of joint involvement in her disease?",
    "choices": {
      "a": "Additive",
      "b": "Migratory",
      "c": "Monoarticular",
      "d": "Oligoarticular"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 53,
    "question": "A 30/M has a monoarticular type of",
    "choices": {
      "a": "Crystal-induced",
      "b": "Immune-related"
    },
    "answer": "A",
    "section": "LONG EXAM 6",
    "reference": "10"
  },
  {
    "number": 54,
    "question": "Which of the following symptoms is not considered a systemic manifestation in musculoskeletal disorders?",
    "choices": {
      "a": "Easy fatigability",
      "b": "Elevated ESR",
      "c": "Limitation of motion",
      "d": "Weight loss"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 55,
    "question": "Which of the following is nonarticular?",
    "choices": {
      "a": "Ankylosing spondylitis",
      "b": "Carpal tunnel syndrome",
      "c": "Rheumatoid arthritis",
      "d": "Pseudogout"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 56,
    "question": "Which of the following is a chronic inflammatory, articular musculoskeletal condition?",
    "choices": {
      "a": "Adhesive capsulitis",
      "b": "Gout",
      "c": "Rheumatic fever",
      "d": "Rheumatoid arthritis"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 57,
    "question": "Which among the following is a red flag of musculoskeletal complaints?",
    "choices": {
      "a": "Arthralgia",
      "b": "Easy fatigability",
      "c": "Pain at night",
      "d": "Swelling"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 58,
    "question": "Which of the following articular conditions will NOT have systemic manifestations?",
    "choices": {
      "a": "Gout",
      "b": "Osteoarthritis",
      "c": "Rheumatic fever",
      "d": "Septic arthritis"
    },
    "answer": "B",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 59,
    "question": "Which of the following will most likely determine severity in musculoskeletal diseases?",
    "choices": {
      "a": "Chronicity of disease",
      "b": "Pathologic etiology",
      "c": "Structures involved",
      "d": "Systemic and extra-articular involvement"
    },
    "answer": "D",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 60,
    "question": "Where is the primary pathology in a 65/F diagnosed with knee OA?",
    "choices": {
      "a": "Bone",
      "b": "Bursae",
      "c": "Cartilage",
      "d": "Synovium"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 61,
    "question": "In what position is the best for Teleroentgenogram?",
    "choices": {
      "a": "Lateral decubitus",
      "b": "Sitting",
      "c": "Upright",
      "d": "Supine"
    },
    "answer": "C",
    "section": "LONG EXAM 6",
    "reference": "11"
  },
  {
    "number": 62,
    "question": "Which imaging modality DOES NOT use ionizing radiation?",
    "choices": {
      "a": "Digital radiography of the chest",
      "b": "Conventional/ four-vessel cerebral angiogram",
      "c": "Computed tomography (CT) scan of the abdomen",
      "d": "Magnetic resonance imaging (MRI) of knee"
    },
    "answer": "D",
    "section": "",
    "reference": "12"
  },
  {
    "number": 63,
    "question": "What radiographic characteristics do the corona radiata and internal capsule exhibit in a CT scan?",
    "choices": {
      "a": "Hypodense",
      "b": "Hyperdense",
      "c": "Hypoechoic",
      "d": "Hyperechoic"
    },
    "answer": "A",
    "section": "",
    "reference": "12"
  },
  {
    "number": 64,
    "question": "A 68-year old male hypertensive and diabetic patient was brought to the emergency room for sudden onset right-sided weakness and slurring of speech. What is the initial imaging modality of choice for this patient?",
    "choices": {
      "a": "Cranial ultrasound",
      "b": "Plain and contrast cranial MRI",
      "c": "Plain cranial MRI",
      "d": "Plain cranial CT scan"
    },
    "answer": "D",
    "section": "",
    "reference": "12"
  },
  {
    "number": 65,
    "question": "In a lumbar spine radiograph, the \"neck\" of \"Scotty dog\" corresponds to which particular part of the lumbar vertebra?",
    "choices": {
      "a": "Lamina",
      "b": "Pars interarticularis",
      "c": "
"""

MOCK_RESPONSE_2 = """
```json
[
  {
    "number": 65,
    "question": "In a lumbar spine radiograph, the \"neck\" of \"Scotty dog\" corresponds to which particular part of the lumbar vertebra?",
    "choices": {
      "a": "Lamina",
      "b": "Pars interarticularis",
      "c": "Pedicles",
      "d": "Transverse process"
    },
    "answer": "B",
    "section": "",
    "reference": "12"
  },
  {
    "number": 66,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Aortic bulb",
      "b": "Left atrium",
      "c": "Left ventricle",
      "d": "Main pulmonary artery"
    },
    "answer": "D",
    "section": "",
    "reference": "12"
  },
  {
    "number": 67,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Main pulmonary artery",
      "b": "Left main bronchus",
      "c": "Right main bronchus",
      "d": "Let atrial appendage"
    },
    "answer": "B",
    "section": "",
    "reference": "13"
  },
  {
    "number": 68,
    "question": "Identify the encircled structure.",
    "choices": {
      "a": "2nd metacarpo-phalangeal joint",
      "b": "4th metacarpo-phalangeal joint",
      "c": "base of the 2nd metacarpal",
      "d": "distal end of the proximal phalanx of the 2nd digit"
    },
    "answer": "A",
    "section": "",
    "reference": "13"
  },
  {
    "number": 69,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Cuboid",
      "b": "Lateral Malleolus",
      "c": "Medial Malleolus",
      "d": "Talus"
    },
    "answer": "B",
    "section": "",
    "reference": "13"
  },
  {
    "number": 70,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Sacroiliac joint",
      "b": "Ilium",
      "c": "Ischium",
      "d": "Iliac Wing"
    },
    "answer": "A",
    "section": "",
    "reference": "14"
  },
  {
    "number": 71,
    "question": "Identify the following radiologic procedure.",
    "choices": {
      "a": "Barium enema",
      "b": "Small bowel series",
      "c": "Esophagogram/ Barium swallow",
      "d": "Upper gastrointestinal series"
    },
    "answer": "B",
    "section": "",
    "reference": "14"
  },
  {
    "number": 72,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Appendix",
      "b": "Ascending colon",
      "c": "Cecum",
      "d": "Descending colon"
    },
    "answer": "B",
    "section": "",
    "reference": "14"
  },
  {
    "number": 73,
    "question": "Identify the pointed structure",
    "choices": {
      "a": "Posterior cerebral artery",
      "b": "Posterior inferior cerebellar artery",
      "c": "Superior cerebellar artery",
      "d": "Vertebral artery"
    },
    "answer": "D",
    "section": "",
    "reference": "14"
  },
  {
    "number": 74,
    "question": "Identify the following radiologic procedure",
    "choices": {
      "a": "Intravenous pyelogram",
      "b": "Plain KUB radiograph",
      "c": "Retrograde urogram",
      "d": "Voiding cystogram"
    },
    "answer": "A",
    "section": "",
    "reference": "14"
  },
  {
    "number": 75,
    "question": "Identify the marked 'X' paranasal sinus.",
    "choices": {
      "a": "Ethmoid",
      "b": "Maxillary",
      "c": "Frontal",
      "d": "Sphenoid"
    },
    "answer": "B",
    "section": "",
    "reference": "15"
  },
  {
    "number": 76,
    "question": "Identify what imaging modality is used",
    "choices": {
      "a": "X-ray",
      "b": "Plain CT",
      "c": "MRI",
      "d": "Plain CT & CT w/ contrast"
    },
    "answer": "C",
    "section": "",
    "reference": "15"
  },
  {
    "number": 77,
    "question": "What structure is being pointed at in this CT scan?",
    "choices": {
      "a": "Fourth ventricle",
      "b": "Right lateral ventricle",
      "c": "Left lateral ventricle",
      "d": "Third ventricle"
    },
    "answer": "B",
    "section": "",
    "reference": "15"
  },
  {
    "number": 78,
    "question": "What organ is imaged in this ultrasound study?",
    "choices": {
      "a": "Ovary",
      "b": "Prostate",
      "c": "Thyroid Gland",
      "d": "Gallbladder"
    },
    "answer": "C",
    "section": "",
    "reference": "15"
  },
  {
    "number": 79,
    "question": "What organ is in this ultrasound?",
    "choices": {
      "a": "Uterus",
      "b": "Pancreas",
      "c": "Gallbladder",
      "d": "Urinary Bladder"
    },
    "answer": "C",
    "section": "",
    "reference": "16"
  },
  {
    "number": 80,
    "question": "Identify the pointed structure.",
    "choices": {
      "a": "Stomach",
      "b": "Liver",
      "c": "Spleen",
      "d": "Pancreas"
    },
    "answer": "B",
    "section": "",
    "reference": "16"
  },
  {
    "number": 81,
    "question": "An internist who is considering a diagnosis of angina pectoris based",
    "choices": {
      "a": "Anchoring",
      "b": "Representative"
    },
    "answer": "A",
    "section": "",
    "reference": "16"
  },
  {
    "number": 82,
    "question": "A surgeon who is considering a diagnosis of acute cholecystitis in a 45 year old female patient with a physical examination finding of a positive Murphy's sign is following which of the following cognitive shortcuts?",
    "choices": {
      "a": "Anchoring",
      "b": "Representative",
      "c": "Availability",
      "d": "None of the above"
    },
    "answer": "B",
    "section": "",
    "reference": "17"
  },
  {
    "number": 83,
    "question": "Which of the following is considered a validation study?",
    "choices": {
      "a": "Ultrasound compared to the CT scan in the diagnosis of acute appendicitis",
      "b": "Chest x-ray compared to the direct smear microscopy in the diagnosis of tuberculosis",
      "c": "CT scan compared to surgical histopath in the diagnosis of thyroid carcinoma",
      "d": "CT scan compared to MRI in the diagnosis of pancreatic cancer"
    },
    "answer": "C",
    "section": "",
    "reference": "17"
  },
  {
    "number": 84,
    "question": "Which of the following is affected by the prevalence of a disease in the study population?",
    "choices": {
      "a": "Negative likelihood ratio",
      "b": "Positive predictive value",
      "c": "Sensitivity",
      "d": "Specificity"
    },
    "answer": "B",
    "section": "",
    "reference": "17"
  },
  {
    "number": 85,
    "question": "Which refers to the probability of a test to incorrectly label as positive those patients who do not have the disease?",
    "choices": {
      "a": "False positive rate",
      "b": "Positive likelihood ratio",
      "c": "Positive predictive value",
      "d": "Sensitivity"
    },
    "answer": "A",
    "section": "",
    "reference": "17"
  },
  {
    "number": 86,
    "question": "If the treatment threshold for giving colchicine to a patient with a clinical impression of acute gouty arthritis is set at 80%, what should be the treatment threshold for septic arthritis?",
    "choices": {
      "a": "Cannot be determined without knowing the testing threshold.",
      "b": "Higher than 80% because septic arthritis would entail the use of expensive"
    },
    "answer": "B",
    "section": "",
    "reference": "17"
  },
  {
    "number": 87,
    "question": "If the sensitivity of a test is 90% and the specificity is 80%, what is the positive likelihood ratio?",
    "choices": {
      "a": "0.125",
      "b": "0.5",
      "c": "1.125",
      "d": "4.5"
    },
    "answer": "D",
    "section": "",
    "reference": "18"
  },
  {
    "number": 88,
    "question": "If the pre-test probability of a disease is 50% and a diagnostic test has a positive likelihood ratio of 2, what would be the odds of the disease if the diagnostic test is positive?",
    "choices": {
      "a": "1:6",
      "b": "1:8",
      "c": "6:1",
      "d": "8:1"
    },
    "answer": "C",
    "section": "",
    "reference": "18"
  },
  {
    "number": 89,
    "question": "If the pre-test probability of a disease is 60% and the first diagnostic test has a positive likelihood ratio of 3 and the second diagnostic test has a positive likelihood ratio of 2, what is the post-test probability of the disease if the first diagnostic test is positive and the second diagnostic test is also positive?",
    "choices": {
      "a": "78.3%",
      "b": "80.0%",
      "c": "87.5%",
      "d": "90.0%"
    },
    "answer": "A",
    "section": "",
    "reference": "18"
  },
  {
    "number": 90,
    "question": "If the post-test odds is 5:1, what is the post-test probability?",
    "choices": {
      "a": "16.7%",
      "b": "20.0%",
      "c": "80.0%",
      "d": "83.3%"
    },
    "answer": "D",
    "section": "",
    "reference": "18"
  },
  {
    "number": 91,
    "question": "If the pre-test odds is 12: 3, what is the pre-test probability?",
    "choices": {
      "a": "20.0%",
      "b": "25%",
      "c": "75%",
      "d": "80%"
    },
    "answer": "D",
    "section": "",
    "reference": "18"
  },
  {
    "number": 92,
    "question": "If in a randomized controlled trial of a new drug the result shows that there was a difference with a p value of 2% at a set alpha error of 5% using a 2-tailed test, what would be your interpretation?",
    "choices": {
      "a": "There is enough evidence to state that there is a difference",
      "b": "There is enough evidence to state that there is no difference",
      "c": "There is not enough evidence to state that there is a difference",
      "d": "There is not enough evidence to state that there is no difference"
    },
    "answer": "A",
    "section": "",
    "reference": "19"
  },
  {
    "number": 93,
    "question": "Which of the following has the highest evidence grade?",
    "choices": {
      "a": "2 meta analysis of 10 cohort studies",
      "b": "Randomized control trial",
      "c": "50 Descriptive studies of pathophysiology",
      "d": "(unrecalled)"
    },
    "answer": "B",
    "section": "",
    "reference": "19"
  },
  {
    "number": 94,
    "question": "Which of the following is true if the 95% confidence interval of the absolute risk reduction in a randomized-controlled trial is between -0.5 to -0.1?",
    "choices": {
      "a": "The experimental therapy is definitely beneficial",
      "b": "The experimental therapy is definitely harmful",
      "c": "The experimental therapy is somewhat harmful",
      "d": "The experimental therapy is neither beneficial or harmful."
    },
    "answer": "B",
    "section": "",
    "reference": "19"
  },
  {
    "number": 95,
    "question": "Which of the following will have a p value more than 5% in a randomized control trial with a set alpha error of 5%?",
    "choices": {
      "a": "95% CI of the RRR is between -0.5 to 0.5",
      "b": "95% CI of the RRR is between 0.5 to 1.2",
      "c": "95% CI of the RR is between 0.5 to 0.9"
    },
    "answer": "A",
    "section": "",
    "reference": "19"
  },
  {
    "number": 96,
    "question": "Which of the following will happen if the sample size reaches infinity?",
    "choices": {
      "a": "P-value will be equal to 0.",
      "b": "P-value will be less than 1%.",
      "c": "The 95% CI will reach infinity",
      "d": "The 95% CI will not cross the unity line."
    },
    "answer": "A",
    "section": "",
    "reference": "20"
  },
  {
    "number": 97,
    "question": "RRR is equal to?",
    "choices": {
      "a": "1-RR",
      "b": "1-ARR",
      "c": "1/RR",
      "d": "1/ARR"
    },
    "answer": "A",
    "section": "",
    "reference": "20"
  },
  {
    "number": 98,
    "question": "Which of the following is true if the null hypothesis is NOT rejected?",
    "choices": {
      "a": "There is enough evidence to say that there is a difference.",
      "b": "There is NOT enough evidence to say that there is a difference.",
      "c": "There is enough evidence to say that there is no difference.",
      "d": "There is NOT enough evidence to say that there is no difference."
    },
    "answer": "B",
    "section": "",
    "reference": "20"
  },
  {
    "number": 99,
    "question": "Alpha errors in randomized-controlled trials may be due to which of the following?",
    "choices": {
      "a": "Inappropriate statistical test",
      "b": "Over-sized sample population",
      "c": "Selection bias",
      "d": "Use of surrogate markers"
    },
    "answer": "A",
    "section": "",
    "reference": "20"
  },
  {
    "number": 100,
    "question": "If the 95% CI of the relative risk reduction is between 0.1 to 0.9, what is the chance that the experimental therapy will have a harmful effect?",
    "choices": {
      "a": "0%",
      "b": "Less than 1%",
      "c": "Less than 5%",
      "d": "Less than 10%"
    },
    "answer": "C",
    "section": "",
    "reference": "20"
  },
  {
    "number": 101,
    "question": "A patient has bronchovesicular breath sounds at the right mid anterior chest. What is the MOST LIKELY underlying lung condition?",
    "choices": {
      "a": "Emphysema",
      "b": "None. The patient's findings are physiologic",
      "c": "Lobar consolidation",
      "d": "Atelectasis"
    },
    "answer": "B",
    "section": "",
    "reference": "21"
  },
  {
    "number": 102,
    "question": "A 62/M, 15-pack year smoker, street vendor, consulted at the OPD complaining of one-month history of cough with scanty phlegm associated with poor appetite and weight loss. His temperature was 37.0C, RR = 20. There are fine and coarse crackles over both apices. What is the most likely underlying lung condition?",
    "choices": {
      "a": "Chronic bronchitis",
      "b": "Pulmonary tuberculosis",
      "c": "Pneumonia",
      "d": "Lung cancer"
    },
    "answer": "B",
    "section": "",
    "reference": "21"
  },
  {
    "number": 103,
    "question": "A 60 y/o male, 30-pack year smoker has progressive difficulty of breathing over the past 2 years with dry cough for the past 12 months. His chest is bilateral hyperresonant with distant breath sounds with occasional expiratory wheezing. What is the most likely diagnosis?",
    "choices": {
      "a": "Asthma",
      "b": "Chronic bronchitis",
      "c": "Emphysema",
      "d": "Pneumothorax"
    },
    "answer": "C",
    "section": "",
    "reference": "21"
  },
  {
    "number": 104,
    "question": "The appearance of intercostal retractions in a dyspneic patient indicates which of the following?",
    "choices": {
      "a": "Bilateral phrenic nerve paralysis",
      "b": "Fatigued intercostal muscles",
      "c": "Diaphragm failure",
      "d": "Laryngeal angioedema"
    },
    "answer": "B",
    "section": "",
    "reference": "22"
  },
  {
    "number": 105,
    "question": "Which of the following is the single most important factor that predisposes unacclimatized Mt. Everest climbers to succumb to high altitude pulmonary edema?",
    "choices": {
      "a": "Diffuse peripheral vasoconstriction",
      "b": "Low atmospheric pressure",
      "c": "Low FiO2",
      "d": "Pulmonary hypoxia"
    },
    "answer": "D",
    "section": "",
    "reference": "22"
  },
  {
    "number": 106,
    "question": "A 28/F presents with 3 days of moderate amount of non-bloody diarrhea associated with loss of appetite, nausea and vomiting. Temperature 39C, hyperactive bowel sounds, non-tender abdomen. What is the next best management of choice?",
    "choices": {
      "a": "Do stool microbiology studies",
      "b": "Fluid and electrolyte replacement",
      "c": "Give antibiotic therapy",
      "d": "Start antidiarrheal agents"
    },
    "answer": "B",
    "section": "",
    "reference": "22"
  },
  {
    "number": 107,
    "question": "Which among the initial tests allows the physician to both diagnose and treat a bleeding peptic ulcer",
    "choices": {
      "a": "CT scan of the abdomen",
      "b": "Laparoscopy",
      "c": "Upper GI Endoscopy",
      "d": "Upper GI Series"
    },
    "answer": "C",
    "section": "",
    "reference": "22"
  },
  {
    "number": 108,
    "question": "Which of the following conditions can manifest with right upper quadrant pain?",
    "choices": {
      "a": "Calculous cholecystitis",
      "b": "Descending colon diverticulitis",
      "c": "Sigmoid colon volvulus",
      "d": "Splenic necrosis"
    },
    "answer": "A",
    "section": "",
    "reference": "22"
  },
  {
    "number": 109,
    "question": "In cases of suspected colonic obstruction without perforation, which of the following imaging examinations may be diagnostic?",
    "choices": {
      "a": "Contrast enema",
      "b": "Small intestinal series using barium sulfate"
    },
    "answer": "A",
    "section": "",
    "reference": "22"
  },
  {
    "number": 110,
    "question": "A 32-year old male consults with voluminous diarrhea with mild abdominal pain after eating seafood. Which of the following is the most likely etiology of diarrhea?",
    "choices": {
      "a": "Campylobacter",
      "b": "Entamoeba histolytica",
      "c": "Salmonella",
      "d": "Vibrio cholera"
    },
    "answer": "D",
    "section": "",
    "reference": "23"
  },
  {
    "number": 111,
    "question": "Which clinical manifestation is suggestive of upper gastrointestinal bleeding rather than lower gastrointestinal bleeding?",
    "choices": {
      "a": "Normal BUN levels",
      "b": "Passage of fresh blood per rectum",
      "c": "Presence of bilious aspirate on NGT",
      "d": "Presence of black, tarry stool"
    },
    "answer": "D",
    "section": "",
    "reference": "23"
  },
  {
    "number": 112,
    "question": "A 34/M presented with intermittent episodes of blood-streaked stools. He denied abdominal pain, changes in bowel habits, and weight loss. His father was diagnosed with colon cancer 5 years ago. Which diagnostic procedure is most appropriate?",
    "choices": {
      "a": "CT scan of the whole abdomen",
      "b": "Colonoscopy",
      "c": "Flexible sigmoidoscopy",
      "d": "Upper endoscopy"
    },
    "answer": "B",
    "section": "",
    "reference": "23"
  },
  {
    "number": 113,
    "question": "A 22 year old male comes to the emergency room because of generalized weakness associated with mild jaundice noted after taking co-trimoxazole for urinary tract infection. He denies pruritus or tea colored urine. Laboratory studies done shows a hemoglobin of 9 g/L, total bilirubin of 6 mg/dL with direct bilirubin of 1 mg/dL, ALT of 25, AST of 24, alkaline phosphatase of 90. What is the most likely cause of his icterus?",
    "choices": {
      "a": "Autoimmune hemolytic hepatitis",
      "b": "Drug-induced hepatitis",
      "c": "Hemolysis due to G6PD deficiency",
      "d": "Gilbert's Syndrome"
    },
    "answer": "C",
    "section": "",
    "reference": "24"
  },
  {
    "number": 114,
    "question": "A 23/M presents with fatigue and tea colored urine. On physical examination reveals icteric sclerae and tender hepatomegaly. Laboratory studies showed ALT of 2680 U/L, AST of 2500 U/L, alkaline phosphatase at 100 IU/L and total bilirubin at 7 mg/dL. Which of the following is the most likely diagnosis?",
    "choices": {
      "a": "Acute viral hepatitis",
      "b": "Alcoholic hepatitis",
      "c": "Drug induced hepatitis",
      "d": "Ischemic hepatitis"
    },
    "answer": "A",
    "section": "",
    "reference": "24"
  },
  {
    "number": 115,
    "question": "What is the estimated K deficit in a patient with a drop of potassium from 4 meq/L to 2 meq/L?",
    "choices": {
      "a": "200",
      "b": "400",
      "c": "600",
      "d": "800"
    },
    "answer": "B",
    "section": "",
    "reference": "24"
  },
  {
    "number": 116,
    "question": "What is the plasma volume of a 60 kg female?",
    "choices": {
      "a": "2",
      "b": "4",
      "c": "6",
      "d": "8"
    },
    "answer": "A",
    "section": "",
    "reference": "24"
  },
  {
    "number": 117,
    "question": "Which is a glomerular disease with acute renal failure and with low complement 3 (C3)?",
    "choices": {
      "a": "ANCA",
      "b": "Good Pasture's Disease",
      "c": "IgA Nephropathy",
      "d": "Lupus Nephritis"
    },
    "answer": "D",
    "section": "",
    "reference": "25"
  },
  {
    "number": 118,
    "question": "A 67/M, diabetic and hypertensive for 20 years develop massive proteinuria of 4.5 grams/day. His creatinine is rising over the past 2 years from 1.0 mg/dL to 2.5 mg/dL (NV: 0.7 - 1.3 mg/dL). What type of proteinuria does this patient have?",
    "choices": {
      "a": "Glomerular",
      "b": "Overflow",
      "c": "Tubular",
      "d": "Physiologic"
    },
    "answer": "A",
    "section": "",
    "reference": "25"
  },
  {
    "number": 119,
    "question": "What vitamin deficiency should be considered if a patient has Wernicke-Korsakoff syndrome?",
    "choices": {
      "a": "Thiamine",
      "b": "Riboflavin",
      "c": "Niacin",
      "d": "Cobalamin"
    },
    "answer": "A",
    "section": "",
    "reference": "25"
  },
  {
    "number": 120,
    "question": "What equipment can measure body composition?",
    "choices": {
      "a": "Weighing scale",
      "b": "Bioimpedance analysis",
      "c": "Air plethysmography",
      "d": "Indirect calorimetry"
    },
    "answer": "B",
    "section": "",
    "reference": "25"
  }
]
<%DONE%>
```
"""