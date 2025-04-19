from parser import remove_trailing_object, preprocess_text

sample = """
{
"number": 63,
"question": "What radiographic characteristics do the corona radiata and internal capsule exhibit in a CT scan?",
"choices": {
"a": "Hyp\nodense",
"b": "Hyperdense",
"c": "Hypoechoic",
"d": "Hyperechoic"
},
"answer": "A",
"section": "Introduction to Radiology",
"reference": "12"
},
{
"number": 64,
"question": "A 68-year old male hypertensive and diabetic patient was brought to the emergency room for sudden onset right-sided weakness and slurring of speech. What is the initial imaging modality of choice for this patient?",
"choices": {
"a": "Cranial ultrasound",
"b": "Plain and contrast\ncranial MRI",
"c": "Plain```json
"d": "Plain and contrast\ncranial MRI"
},
"answer": "A",
"section": "Introduction to Radiol
"""

want = """
{"number": 63,"question": "What radiographic characteristics do the corona radiata and internal capsule exhibit in a CT scan?","choices": {"a": "Hypodense","b": "Hyperdense","c": "Hypoechoic","d": "Hyperechoic"},"answer": "A","section": "Introduction to Radiology","reference": "12"},
"""

print(remove_trailing_object(preprocess_text(sample)))