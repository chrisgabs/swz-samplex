import json
import os
import sys
from pathlib import Path
import glob
import re
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK resources if needed
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

def preprocess_text(text):
    """Preprocess text for similarity comparison."""
    if not text:
        return ""
    
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = word_tokenize(text)
    
    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return " ".join(filtered_tokens)

def extract_medical_terms(text):
    """Extract potential medical terms from text."""
    # This is a simplified approach - ideally would use a medical NER model
    # or a comprehensive medical terminology dictionary
    if not text:
        return []
    
    words = re.findall(r'\b[A-Za-z][A-Za-z-]{3,}\b', text.lower())
    # Filter out common words
    stop_words = set(stopwords.words('english'))
    medical_terms = [word for word in words if word not in stop_words]
    return medical_terms

def calculate_similarity(q1, q2):
    """Calculate similarity between two questions using multiple metrics."""
    # Preprocess the question and choices texts
    q1_text = q1["question"] + " " + " ".join(q1["choices"].values())
    q2_text = q2["question"] + " " + " ".join(q2["choices"].values())
    
    # Process texts
    q1_processed = preprocess_text(q1_text)
    q2_processed = preprocess_text(q2_text)
    
    # Calculate TF-IDF and cosine similarity
    if q1_processed and q2_processed:
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform([q1_processed, q2_processed])
            cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            cosine_sim = 0
    else:
        cosine_sim = 0
    
    # Extract medical terms
    q1_terms = set(extract_medical_terms(q1_text))
    q2_terms = set(extract_medical_terms(q2_text))
    
    # Calculate Jaccard similarity for medical terms
    union_size = len(q1_terms.union(q2_terms))
    if union_size > 0:
        term_overlap = len(q1_terms.intersection(q2_terms)) / union_size
    else:
        term_overlap = 0
    
    # Check if answers match (this is a strong indicator)
    answer_match = 1 if q1["answer"] == q2["answer"] else 0
    
    # Combined similarity score (weighted average)
    weights = [0.5, 0.3, 0.2]  # Adjust weights based on importance
    return weights[0] * cosine_sim + weights[1] * term_overlap + weights[2] * answer_match

def find_similar_questions(exam_files):
    """Find similar questions across multiple examination files."""
    exams = {}
    questions = []
    
    # Load all questions from all exams
    for file_path in exam_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                exam_name = Path(file_path).stem
                exams[exam_name] = data
                
                for q in data:
                    q['source_exam'] = exam_name
                    questions.append(q)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    # Dictionary to store groups of similar questions
    similar_groups = []
    processed_indices = set()
    
    # Threshold for similarity (adjust as needed)
    similarity_threshold = 0.65
    
    # Compare each question with every other question
    for i in range(len(questions)):
        if i in processed_indices:
            continue
            
        group = [questions[i]]
        processed_indices.add(i)
        
        for j in range(i+1, len(questions)):
            if j in processed_indices:
                continue
                
            # Skip if questions are from the same exam
            if questions[i]['source_exam'] == questions[j]['source_exam']:
                continue
                
            # Calculate similarity
            similarity = calculate_similarity(questions[i], questions[j])
            
            if similarity >= similarity_threshold:
                group.append(questions[j])
                processed_indices.add(j)
        
        # Only keep groups with questions from at least 2 different exams
        if len(group) >= 2 and len(set(q['source_exam'] for q in group)) >= 2:
            similar_groups.append(group)
    
    return similar_groups, exams

def format_output(similar_groups):
    """Format the output according to the specified structure."""
    results = []
    
    for group in similar_groups:
        result = {
            "number": len(results) + 1,
            "question": {},
            "choices": {},
            "answer": {},
            "reference": {}
        }
        
        for question in group:
            exam_name = question['source_exam']
            
            # Add question text
            result["question"][exam_name] = question["question"]
            
            # Add choices
            result["choices"][exam_name] = question["choices"]
            
            # Add answer
            result["answer"][exam_name] = question["answer"]
            
            # Add reference
            result["reference"][exam_name] = {
                "number": question["number"],
                "section": question["section"],
                "reference": question["reference"]
            }
        
        results.append(result)
    
    return results

def main():
    """Main function to process examination files."""
    # Check if files are provided as arguments
    if len(sys.argv) > 1:
        exam_files = sys.argv[1:]
    else:
        # Try to find JSON files in the current directory
        exam_files = glob.glob("*.json")
    
    if not exam_files:
        print("Error: No JSON files found. Please provide the paths to the JSON files as arguments.")
        return
    
    print(f"Processing {len(exam_files)} examination files: {', '.join(exam_files)}")
    
    # Find similar questions
    similar_groups, exams = find_similar_questions(exam_files)
    
    # Format output
    results = format_output(similar_groups)
    
    # Write results to file
    output_file = "similar_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Found {len(results)} groups of similar questions across {len(exams)} examinations.")
    print(f"Results saved to {output_file}")
    
    # Display some statistics
    exams_per_group = [len(set(q['source_exam'] for q in group)) for group in similar_groups]
    if exams_per_group:
        avg_exams_per_group = sum(exams_per_group) / len(exams_per_group)
        print(f"Average number of examinations per similar question group: {avg_exams_per_group:.2f}")
    
    # Display example of a similar question group (if any)
    if results:
        print("\nExample of a similar question group:")
        example = results[0]
        print(json.dumps(example, indent=2))

if __name__ == "__main__":
    main() 